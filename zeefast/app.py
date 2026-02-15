import inspect
import types
import re
from zeefast.response import Response, JsonResponse, HtmlResponse, PlainTextResponse
from zeefast.status import status
from zeefast.api_router import APIRouter
from zeefast.depends import Depends
from zeefast.request import Request

class ZeeFast:

    def __init__(self):

        self.routes = [] 
        self.middlewares=[]
        self.middlewares_for_routes={}

    def add_route(self, method, path,middlewares):
        def wrapper(func):
            pattern = self.path_to_regex(path)
            self.routes.append((method, pattern, func))
            self.middlewares_for_routes[(path,method)]=middlewares
            return func
        return wrapper
    
    def add_middleware(self,middlewares=[]):
        self.middlewares.extend(middlewares)

    def include_router(self, router: APIRouter):
        self.routes.extend(router.routes)
        self.middlewares_for_routes.update(router.middlewares_for_routes)

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
    
    def get(self, path,middlewares=[]):
        return self.add_route("GET", path,middlewares)

    def post(self, path,middlewares=[]):
        return self.add_route("POST", path,middlewares)

    def put(self, path,middlewares=[]):
        return self.add_route("PUT", path,middlewares)

    def delete(self, path,middlewares=[]):
        return self.add_route("DELETE", path,middlewares)

    def patch(self, path,middlewares=[]):
        return self.add_route("PATCH", path,middlewares)


    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return
       
        for middleware in self.middlewares:
            if isinstance(middleware,types.FunctionType):
                if inspect.iscoroutinefunction(middleware()):
                    await middleware
                else:
                    middleware
            else:
                raise TypeError("Middleware must be a python function.")
        method = scope["method"]
        path = scope["path"]

        for m, pattern, handler in self.routes:
            if m != method:
                continue

            match = pattern.match(path)
            if match:
            
                path_params = match.groupdict()

                original_pattern = None
                for (route_path, route_method), _ in self.middlewares_for_routes.items():
                    if route_method == method:
                        route_pattern = self.path_to_regex(route_path)
                        if route_pattern.match(path):
                            original_pattern = route_path
                            break
                
                key = (original_pattern or path, method)
                route_middlewares = self.middlewares_for_routes.get(key, [])
                for r_middleware in route_middlewares:
                    if inspect.iscoroutinefunction(r_middleware):
                        await r_middleware()
                    else:
                        r_middleware()

                signature=inspect.signature(handler)
                kwargs={}
                request=Request(scope)

                for name,param in signature.parameters.items():
                    if name in path_params:
                        kwargs[name]=path_params[name]


                    # Query Param
                    elif name in request.query_params:
                        value = request.query_params[name]
                        if param.annotation != inspect.Parameter.empty:
                            try:
                                value = param.annotation(value)
                            except Exception:
                                pass
                        kwargs[name] = value

                    # Dependency Param
                    elif isinstance(param.default,Depends):
                    
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
