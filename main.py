#http://127.0.0.1:8000 
#uvicorn main:app --reload

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users

app = FastAPI()
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(users.router, prefix="/user", tags=["user"])

@app.get("/")
async def root():
    return {"message": "Hello Juanito"}