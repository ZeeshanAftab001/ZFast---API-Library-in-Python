from zeefast.app import ZeeFast
from zeefast.response import HtmlResponse, JsonResponse
from zeefast.status import status

app=ZeeFast()

@app.get("/zeeshan/{id}/{name}")
async def zeeshan(id,name):
  print(id)
  print(name)
  return JsonResponse({"Name":"Zeeshan"},status_code=status.HTTP_200_OK)

@app.get("/about")
def about():
    return HtmlResponse(file="index.html")

@app.get("/home")
def home():
    return "<h1>Hello,World</h1>"