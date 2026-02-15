import re

class APIRouter():
    
    def __init__(self,prefix='',tags=None):

        self.routes=[] # [(method, regex, handler)]
        self.tags=tags
        self.prefix=prefix
        self.middlewares_for_routes={}
    

    def add_route(self, method, path,middlewares):
        def wrapper(func):
            full_path=self.prefix+path
            pattern = self.path_to_regex(full_path)
            self.routes.append((method, pattern, func))
            self.middlewares_for_routes[(path,method)]=middlewares
            return func
        return wrapper
    
    def path_to_regex(self, path):
        # /user/{id} → ^/user/(?P<id>[^/]+)$
        path = re.sub(r"{(\w+)}", r"(?P<\1>[^/]+)", path)
        return re.compile(f"^{path}$")
    
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