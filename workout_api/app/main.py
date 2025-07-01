from fastapi import FastAPI # type: ignore
from app import models
from app.database import engine
from app.routers import atletas
from fastapi_pagination import add_pagination # type: ignore

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Workout API")

app.include_router(atletas.router)

add_pagination(app)
