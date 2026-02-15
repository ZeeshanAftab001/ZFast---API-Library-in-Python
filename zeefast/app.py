import inspect
import re
from zeefast.response import Response, JsonResponse, HtmlResponse, PlainTextResponse
from zeefast.status import status

class ZeeFast:
    def __init__(self):
        self.routes = [] 

    def add_route(self, method, path):
        def wrapper(func):
            pattern = self.path_to_regex(path)
            self.routes.append((method, pattern, func))
            return func
        return wrapper
    
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

                # call handler
                if inspect.iscoroutinefunction(handler):
                    result = await handler(**path_params)
                else:
                    result = handler(**path_params)

                res = self.convert_response(result)
                await res.as_asgi(send)
                return 

        # 404 if no match found
        res = HtmlResponse("<h1 style='color:red;'>Route Not Found</h1>", status_code=status.HTTP_404_NOT_FOUND)
        await res.as_asgi(send)
