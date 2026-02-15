
class Request:
    def __init__(self, scope):
        self.method = scope["method"]
        self.path = scope["path"]
        self.headers = {k.decode(): v.decode() for k, v in scope.get("headers", [])}
        qs = scope.get("query_string", b"").decode()
        self.query_params = self.parse_query(qs)

    def parse_query(self, qs: str):
        result = {}
        for pair in qs.split("&"):
            if "=" in pair:
                k, v = pair.split("=")
                result[k] = v
        return result
