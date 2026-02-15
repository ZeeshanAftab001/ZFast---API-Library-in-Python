import re

class APIRouter():
    
    def __init__(self,prefix='',tags=None):

        self.routes=[] # [(method, regex, handler)]
        self.tags=tags
        self.prefix=prefix
    

    def add_route(self, method, path):
        def wrapper(func):
            full_path=self.prefix+path
            pattern = self.path_to_regex(full_path)
            self.routes.append((method, pattern, func))
            return func
        return wrapper
    
    def path_to_regex(self, path):
        # /user/{id} → ^/user/(?P<id>[^/]+)$
        path = re.sub(r"{(\w+)}", r"(?P<\1>[^/]+)", path)
        return re.compile(f"^{path}$")
    
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