from fastapi import FastAPI
import uvicorn
from fastapi.routing import APIRouter

# create instance of the app
from api.handlers import user_router

app = FastAPI(title="fast-api-first")

# create the instance for the router
main_api_router = APIRouter()

# set router to the app instance
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(main_api_router)

if __name__ == "__main__":
    # run app on the host and port
    uvicorn.run(app, host="0.0.0.0", port=8000)