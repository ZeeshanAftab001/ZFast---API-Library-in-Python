from zeefast.api_router import APIRouter
from zeefast.depends import Depends
router1=APIRouter(
    prefix="/funs",
    tags=["functions router"]
)

async def hello():
    return "hello Zeeshan"


@router1.get("/fun1")
def fun1(text=Depends(hello)):
    print(text)
    print("this is function1")
    return "This is function 1"


@router1.post("/fun2")
def fun2():
    print("this is function2")
    return "This is function 2"