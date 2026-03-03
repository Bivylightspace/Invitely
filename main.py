from fastapi import FastAPI
from api.utils.config import settings
from api.db.db import engine 
from api.db.base import Base

def create_tables():         
	Base.metadata.create_all(bind=engine)
        

def start_application():
    app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
    create_tables()
    return app


app = start_application()


@app.get("/")
def home():
    return {"msg":"Hello FastAPI"}


