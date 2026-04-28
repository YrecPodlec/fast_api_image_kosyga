from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import router

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
                   "http://image-kosyga.vercel.app",
                   "https://image-kosyga.vercel.app"
                   ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)
app.include_router(router)