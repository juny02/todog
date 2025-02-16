from fastapi import FastAPI

from app.dog.adapter.input.router import router as dog_router

app = FastAPI(title="ToDOG API")

@app.get("/health") 
def check_health(): 
    return {}  

app.include_router(dog_router)