from zeefast.app import ZeeFast
from zeefast.response import HtmlResponse, JsonResponse
from zeefast.status import status
from zeefast.depends import Depends


from test2 import router1




app=ZeeFast()

def middleware_1():
   print("Middleware called")


def iam():
   print("="*100)
   print("I am a route middleware")
   print("="*50)

app.add_middleware([middleware_1])

def abc():
  print("+"*10)
  print("Routes of the router 1")
  print(router1.routes)
  print("+"*10)
  return "ABC function is called."

@app.get("/zeeshan/{id}/{name}",middlewares=[iam])
async def zeeshan(id,name,text=Depends(abc)):
  print("-"*20)
  print("Depends Result : ",text)
  print("-"*20)
  print(id)
  print(name)
  return JsonResponse({"Name":"Zeeshan"},status_code=status.HTTP_200_OK)


@app.get("/search")
def search(q: str, page: int = 1):
    return {"query": q, "page": page}


@app.get("/about")
def about(text=Depends(abc)):
   
    return HtmlResponse(file="index.html")

@app.get("/home")
def home():
    return "<h1>Hello,World</h1>"


app.include_router(router=router1)