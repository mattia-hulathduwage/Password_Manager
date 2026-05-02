from fastapi import FastAPI
from routes.user_route import router as user_router
from fastapi.middleware.cors import CORSMiddleware
from routes.passwords_route import router as passwords_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
)

app.include_router(user_router)
app.include_router(passwords_router)