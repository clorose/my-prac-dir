# app/main.py

from .routers import api
from . import app
from fastapi.middleware.cors import CORSMiddleware

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI project!"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/data")
def get_data():
    return {"message": "This is data from the FastAPI backend"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)