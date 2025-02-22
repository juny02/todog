from fastapi import FastAPI

from app.dog.adapter.input.router import router as dog_router
from app.user.adapter.input.router import router as user_router
from app.dog_family.adapter.input.router import router as dog_fam_router
from app.treat.adapter.input.router import router as treat_router

app = FastAPI(title="ToDOG API")

@app.get("/health") 
def check_health(): 
    return {}  

app.include_router(dog_router)
app.include_router(user_router)
app.include_router(dog_fam_router)
app.include_router(treat_router)