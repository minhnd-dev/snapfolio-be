from fastapi import FastAPI
from v1.endpoints.user import router as user_router
from core.models.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)



