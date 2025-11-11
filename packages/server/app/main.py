"""
This module contains the FastAPI application for the server.
"""

import sys

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1 import api_v1_router

origins = [
    "http://localhost:3000",
]

app = FastAPI(
    title="AI-Powered-Notes-App",
    version="1.0.0",
    license_info={
        "name": "MIT License",
        "url": "https://github.com/mohdaman892/AI-Powered-Notes-App/blob/main/LICENSE",
    },
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redocs",
)

app.include_router(api_v1_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    RELOAD_FLAG = True if len(sys.argv) > 1 else False
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=RELOAD_FLAG)