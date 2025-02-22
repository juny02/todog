from fastapi import FastAPI

from app.dog.adapter.input.router import router as dog_router
from app.user.adapter.input.router import router as user_router
from app.dog_family.adapter.input.router import router as dog_fam_router
from app.treat.adapter.input.router import router as treat_router
from app.treat.adapter.input.error_handlers import error_handlers as treat_error_handlers

app = FastAPI(title="ToDOG API")

for exc, handler in treat_error_handlers.items():
    app.add_exception_handler(exc, handler)

@app.get("/health") 
def check_health(): 
    return {}  

app.include_router(dog_router)
app.include_router(user_router)
app.include_router(dog_fam_router)
app.include_router(treat_router)