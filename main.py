from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from endpoints.v1.user import router as user_router
from endpoints.v1.file import router as file_router
from endpoints.v1.tag import router as tag_router
from core.models.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(file_router)
app.include_router(tag_router)

