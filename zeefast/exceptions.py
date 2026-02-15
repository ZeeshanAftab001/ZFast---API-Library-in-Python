from zeefast.status import status


class HttpException(Exception):

    def __init__(self,status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error",headers=None):

        self.status_code=status_code
        self.detail = detail
        self.headers = headers or {}

        super().__init__(detail)
