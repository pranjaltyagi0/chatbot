import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def add_cors_middleware(app: FastAPI):
    origins = os.getenv("ORIGINS")

    origin_list = [origin.strip() for origin in origins.split(",") if origin.strip()]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
