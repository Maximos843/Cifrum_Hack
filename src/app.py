from pathlib import Path
import uvicorn
from fastapi import FastAPI, APIRouter, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from src.api import router


app = FastAPI()

app.mount("/static", StaticFiles(directory="src/lib/static"), name="static")
templates = Jinja2Templates(directory="src/lib/template")

app.include_router(router)


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Home"})


def start_service():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    start_service()
