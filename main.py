#http://127.0.0.1:8000 
#uvicorn main:app --reload

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, fund

from dotenv import load_dotenv

app = FastAPI()

load_dotenv()
 
origins = ["http://localhost:4321/","http://localhost:4321"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(users.router, prefix="/user", tags=["user"])
app.include_router(fund.router, prefix="/fund", tags=["fund"])

@app.get("/")
async def root():
    return {"message": "Hello Juanito"}