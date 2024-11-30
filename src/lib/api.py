from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from model.model import model


router = APIRouter()
templates = Jinja2Templates(directory="src/lib/template")


@router.post("/predict")
async def predict(request: Request, review_text: str = Form(...)):
    try:
        # TODO: get predictions from model
        predictions = {"prediction": "<placeholder>"}
        
        if "text/html" in request.headers.get("Accept", ""):
            return templates.TemplateResponse("index.html", {"request": request, "predictions": predictions, "title": "Predictions"})
        else:
            return JSONResponse(content=predictions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))