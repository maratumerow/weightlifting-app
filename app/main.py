from fastapi import FastAPI

from api.routes.users import router
from data.models.base import Base
from data.session import engine

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router=router)
