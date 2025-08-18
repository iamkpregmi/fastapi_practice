from fastapi import FastAPI
from routers import test_router

app = FastAPI()

app.include_router(test_router.router)

@app.get("/")
def root():
    return {"message": "FastAPI is working!"}
