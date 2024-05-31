from fastapi import FastAPI
from My_project.routers import contact
import uvicorn

app = FastAPI()

app.include_router(contact.router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)