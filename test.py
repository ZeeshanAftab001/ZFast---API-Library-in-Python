from zeefast import ZeeFast
from response import HtmlResponse, JsonResponse

app=ZeeFast()

@app.get("/zeeshan")
async def zeeshan():
  return JsonResponse({"Name":"Zeeshan"},status=200)

@app.get("/about")
def about():
    return HtmlResponse(file="index.html")

@app.get("/home")
def home():
    return "<h1>Hello,World</h1>"