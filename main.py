from fastapi import FastAPI
# from routers import explorer,auth,ezyexplorer
from routers import home
from database import engine
import models
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from decouple import config
models.Base.metadata.create_all(bind=engine)
app=FastAPI()
port = config('PORT')
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="files")

origins = [
    # "http://localhost:4200"
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(home.router)
# app.include_router(auth.router)
# app.include_router(ezyexplorer.router)
if __name__=="__main__":
    uvicorn.run("main:app",host="0.0.0.0",port=port,reload=True)