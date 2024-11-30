from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

from src.lib.utils.database_client import DatabaseClient


router = APIRouter()
templates = Jinja2Templates(directory="src/lib/template")

db_client = DatabaseClient("review_schema")


# TODO: move all names into Consts class

def get_predictions(text: str) -> str:
    # TODO: get predictions from model
    records = db_client.select_with_condition_query('reviews', 'review', data=text)
    
    if records:
        return records[0]["sentiment"]
    else:
        new_record = {'review': text, 'sentiment': 'chill'}
        db_client.insert_query('reviews', new_record)
        
        return 'chill'


@router.post("/predict")
async def predict(request: Request, review_text: str = Form(...)):
    try:
        # TODO: get predictions from model
        predictions = {'prediction': get_predictions(review_text)}
        
        if "text/html" in request.headers.get("Accept", ""):
            return templates.TemplateResponse("index.html", {"request": request, "predictions": predictions, "title": "Predictions"})
        else:
            return JSONResponse(content=predictions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))