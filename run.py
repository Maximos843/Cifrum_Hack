import uvicorn
from fastapi import FastAPI


app = FastAPI()

#include routers


def start_service():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    start_service()
