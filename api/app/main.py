from fastapi import FastAPI

from app.dog.adapter.input.api.router import router as dog_router
from app.user.adapter.input.api.router import router as user_router
from app.user.adapter.input.api.error_handlers import error_handlers as user_error_handlers
from app.dog_family.adapter.input.api.router import router as dog_fam_router
from app.treat.adapter.input.api.router import router as treat_router
from app.treat.adapter.input.api.error_handlers import error_handlers as treat_error_handlers

from app.treat_record.adapter.input.api.router import router as treat_record_router
from app.treat_record.adapter.input.api.error_handlers import error_handlers as treat_records_error_handlers

from app.walk_record.adapter.input.api.router import router as walk_record_router
from app.walk_record.adapter.input.api.error_handlers import error_handlers as walk_records_error_handlers

from app.meal_record.adapter.input.api.router import router as meal_record_router
from app.meal_record.adapter.input.api.error_handlers import error_handlers as meal_records_error_handlers

from app.memo.adapter.input.api.router import router as memo_router
from app.memo.adapter.input.api.error_handlers import error_handlers as memo_error_handlers

from app.schedule.adapter.input.api.router import router as schedule_router
from app.schedule.adapter.input.api.error_handlers import error_handlers as schedule_error_handlers

from app.medicine_schedule.adapter.input.api.router import router as med_schedule_router
from app.medicine_schedule.adapter.input.api.error_handlers import error_handlers as med_schedule_error_handlers

from app.medicine_record.adapter.input.api.router import router as med_record_router
from app.medicine_record.adapter.input.api.error_handlers import error_handlers as med_record_error_handlers



app = FastAPI(title="ToDOG API")

for exc, handler in user_error_handlers.items():
    app.add_exception_handler(exc, handler)

for exc, handler in treat_error_handlers.items():
    app.add_exception_handler(exc, handler)
    
for exc, handler in treat_records_error_handlers.items():
    app.add_exception_handler(exc, handler)
    
for exc, handler in walk_records_error_handlers.items():
    app.add_exception_handler(exc, handler)

for exc, handler in meal_records_error_handlers.items():
    app.add_exception_handler(exc, handler)
    
for exc, handler in memo_error_handlers.items():
    app.add_exception_handler(exc, handler)

for exc, handler in schedule_error_handlers.items():
    app.add_exception_handler(exc, handler)
    
for exc, handler in med_schedule_error_handlers.items():
    app.add_exception_handler(exc, handler)
    
for exc, handler in med_record_error_handlers.items():
    app.add_exception_handler(exc, handler)



@app.get("/health") 
def check_health(): 
    return {}  

app.include_router(dog_router)
app.include_router(user_router)
app.include_router(dog_fam_router)
app.include_router(treat_router)
app.include_router(treat_record_router)
app.include_router(walk_record_router)
app.include_router(meal_record_router)
app.include_router(memo_router)
app.include_router(schedule_router)
app.include_router(med_schedule_router)
app.include_router(med_record_router)