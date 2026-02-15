import inspect
import re
from zeefast.response import Response, JsonResponse, HtmlResponse, PlainTextResponse
from zeefast.status import status
from zeefast.depends import Depends
from zeefast.api_router import APIRouter

class ZeeFast:
    def __init__(self):
        self.routes = []  # [(method, regex, handler)]

    def add_route(self, method, path):
        def wrapper(func):
            pattern = self.path_to_regex(path)
            self.routes.append((method, pattern, func))
            return func
        return wrapper
    
    def include_router(self, router: APIRouter):
        self.routes.extend(router.routes)

    def path_to_regex(self, path):
        # /user/{id} → ^/user/(?P<id>[^/]+)$
        path = re.sub(r"{(\w+)}", r"(?P<\1>[^/]+)", path)
        return re.compile(f"^{path}$")
    
    def convert_response(self, result):
        if isinstance(result, Response):
            return result
        if isinstance(result, dict):
            return JsonResponse(result)
        if isinstance(result, str):
            return HtmlResponse(result)
        return PlainTextResponse(str(result))
    
    def get(self, path):
        return self.add_route("GET", path)

    def post(self, path):
        return self.add_route("POST", path)

    def put(self, path):
        return self.add_route("PUT", path)

    def delete(self, path):
        return self.add_route("DELETE", path)

    def patch(self, path):
        return self.add_route("PATCH", path)


    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return

        method = scope["method"]
        path = scope["path"]

        for m, pattern, handler in self.routes:
            if m != method:
                continue

            match = pattern.match(path)
            if match:
                path_params = match.groupdict()
                '''
                Inorder to get the parameter of the handler
                we will be using inspect.signature().This 
                will help us getting all the params provided
                in the handler function.In this way we can 
                compare whether the function argument is an
                Instance of Depends Class.If it is then we
                will fetch the function from param.default.
                dependency and call it,then send the response
                back to the handler.

                Another this that must be kept in mind are the 
                default arguments of the handler.we have to 
                first get them in add them into a dict.After
                that the response of the dep_function will be 
                added to that dict and then pass it to the 
                handler(**kwargs)

                '''
                signature=inspect.signature(handler)
                kwargs={}
                # print(signature.parameters.items())
                for name,param in signature.parameters.items():
                    if name in path_params:
                        # print("*"*20)
                        # print(path_params)
                        kwargs[name]=path_params[name]
                    elif isinstance(param.default,Depends):
                        print("*"*20)
                        print(param.default)
                        print("*"*20)
                        dep_func=param.default.dependency
                        if inspect.iscoroutinefunction(dep_func):
                            kwargs[name] = await dep_func()
                        else:
                            kwargs[name]=dep_func()
                            # print(kwargs)
                    else:
                        kwargs[name] = None
                if inspect.iscoroutinefunction(handler):
                    result = await handler(**kwargs)
                else:
                    result = handler(**kwargs)

                res = self.convert_response(result)
                await res.as_asgi(send)
                return 

        res = HtmlResponse("<h1 style='color:red;'>Route Not Found</h1>", status_code=status.HTTP_404_NOT_FOUND)
        await res.as_asgi(send)
