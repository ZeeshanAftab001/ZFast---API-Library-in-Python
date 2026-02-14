from response import Response, JsonResponse, HtmlResponse, PlainTextResponse
import inspect

class ZeeFast:
    def __init__(self):
        self.routes = {}  # ("GET", "/path") : handler

    def get(self, path):
        def wrapper(func):
            self.routes[("GET", path)] = func
            return func
        return wrapper

    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http':
            return

        method = scope['method']
        path = scope['path']
        handler = self.routes.get((method, path))

        if not handler:
            # 404 Response
            res = HtmlResponse("<h1 style='color:red;'>Route Not Found</h1>", status=404)
            await res.as_asgi(send)
            return

        # Call handler
        if inspect.iscoroutinefunction(handler):
            result = await handler()
        else:
            result = handler()

            
        if isinstance(result, Response):
            res = result
        elif isinstance(result, dict):
            res = JsonResponse(result)
        elif isinstance(result, str):
            res = HtmlResponse(result)
        else:
            res = PlainTextResponse(str(result))

        await res.as_asgi(send)
