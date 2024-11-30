from fastapi import APIRouter, HTTPException, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

from .lib.utils.database_client import DatabaseClient
from .lib.model.model import model
from .lib.utils.config import Consts


router = APIRouter()
templates = Jinja2Templates(directory="src/lib/template")


def get_db_client():
    return DatabaseClient(Consts.REVIEW_SCHEMA_NAME)

def get_predictions(review_text: str, db_client: DatabaseClient) -> str:
    records = db_client.select_with_condition_query(Consts.REVIEW_TABLE_NAME, "review", data=review_text)

    if records:
        return records[0]["sentiment"]
    else:
        sentiment = model.predict(review_text)[1]
        new_record = {"review": review_text, "sentiment": sentiment}
        db_client.insert_query("reviews", new_record)

        return sentiment


@router.post("/predict")
async def predict(request: Request, 
                  review_text: str = Form(...),
                  db_client: DatabaseClient = Depends(get_db_client)):
    # if not review_text.strip():
    #     raise HTTPException(status_code=400, detail="Review text is empty")
    
    try:
        predictions = {"prediction": get_predictions(review_text, db_client)}
        
        if "text/html" in request.headers.get("Accept", ""):
            return templates.TemplateResponse("index.html", {"request": request, "predictions": predictions, "title": "Predictions"})
        else:
            return JSONResponse(content=predictions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))