import uvicorn
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse


app = FastAPI()

app.mount("/static", StaticFiles(directory="src/lib/static"), name="static")
templates = Jinja2Templates(directory="src/lib/template")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Home"})


@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, review_text: str=Form(...)):
    try:
        # TODO: get predictions from model
        return templates.TemplateResponse("index.html", {"request": request, "predictions": "<placeholder>", "title": "Predictions"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def start_service():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    start_service()
