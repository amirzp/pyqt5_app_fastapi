from contact import main
from user import main
from database import database
from app_main import app


# ساخت تیبل های دیتابیس با توجه به کلاس های مدل
database.Base.metadata.create_all(bind=database.engine)
