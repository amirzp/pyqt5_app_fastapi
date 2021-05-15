from database import database
from fastapi import FastAPI
from routers import user, contact

app = FastAPI()

# ساخت تیبل های دیتابیس با توجه به کلاس های مدل
database.Base.metadata.create_all(bind=database.engine)

app.include_router(user.router)
app.include_router(contact.router)
