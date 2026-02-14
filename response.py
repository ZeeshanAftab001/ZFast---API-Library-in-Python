import json

class Response:
    def __init__(self, content="", status=200, headers=None):
        self.content = content
        self.status = status
        if headers is None:
            self.headers = [(b"content-type", b"text/plain")]
        elif isinstance(headers, dict):
            self.headers = [(k.encode(), v.encode()) for k, v in headers.items()]
        else:
            self.headers = headers

    async def as_asgi(self, send):
        # Convert content to bytes
        if isinstance(self.content, (dict, list)):
            body = json.dumps(self.content).encode()
            # Override headers for JSON
            self.headers = [(b"content-type", b"application/json")]
        elif isinstance(self.content, str):
            body = self.content.encode()
        elif isinstance(self.content, bytes):
            body = self.content
        else:
            body = str(self.content).encode()

        await send({
            "type": "http.response.start",
            "status": self.status,
            "headers": self.headers,
        })
        await send({
            "type": "http.response.body",
            "body": body,
        })


class JsonResponse(Response):
    def __init__(self, content, status=200):
        super().__init__(
            content=json.dumps(content),
            status=status,
            headers={"content-type": "application/json"}
        )


class PlainTextResponse(Response):
    def __init__(self, content, status=200):
        super().__init__(
            content=content,
            status=status,
            headers={"content-type": "text/plain"}
        )


class HtmlResponse(Response):
    def __init__(self, content="", status=200, file=None):
        if file:
            with open(file, "r") as f:
                content = f.read()
        super().__init__(
            content=content,
            status=status,
            headers={"content-type": "text/html"}
        )


class RedirectResponse(Response):
    def __init__(self, location, status=302):
        super().__init__(
            content="",
            status=status,
            headers={"Location": location}
        )
