import json
from zeefast.status import status
from http import HTTPStatus

class Response:

    def __init__(self, content="", status_code=status.HTTP_200_OK, headers=None):

        if isinstance(status_code, HTTPStatus):
            status_code = status_code.value

        self.content = content
        self.status_code = status_code

        if headers is None:
            self.headers = [(b"content-type", b"text/plain")]
        elif isinstance(headers, dict):
            self.headers = [(k.encode(), v.encode()) for k, v in headers.items()]
        else:
            self.headers = headers

    async def as_asgi(self, send):
        if isinstance(self.content, (dict, list)):
            body = json.dumps(self.content).encode()
            self.headers = [(b"content-type", b"application/json")]
        elif isinstance(self.content, str):
            body = self.content.encode()
        else:
            body = str(self.content).encode()

        await send({
            "type": "http.response.start",
            "status": self.status_code,
            "headers": self.headers,
        })
        await send({
            "type": "http.response.body",
            "body": body,
        })


class JsonResponse(Response):
    def __init__(self, content, status_code=status.HTTP_200_OK):
        super().__init__(content, status_code)


class PlainTextResponse(Response):
    def __init__(self, content, status_code=status.HTTP_200_OK):
        super().__init__(
            content=content,
            status_code=status_code,
            headers={"content-type": "text/plain"}
        )


class HtmlResponse(Response):
    def __init__(self, content="", status_code=status.HTTP_200_OK, file=None):
        if file:
            with open(file, "r") as f:
                content = f.read()
        super().__init__(
            content=content,
            status_code=status_code,
            headers={"content-type": "text/html"}
        )


class RedirectResponse(Response):
    def __init__(self, location, status_code=status.HTTP_302_FOUND):
        super().__init__(
            content="",
            status_code=status_code,
            headers={"Location": location}
        )
