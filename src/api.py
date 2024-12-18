from fastapi import APIRouter, HTTPException, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
import asyncio
from typing import List

from src.lib.utils.database_client import DatabaseClient
from src.lib.model.model import model
from src.lib.utils.config import Consts


router = APIRouter()
templates = Jinja2Templates(directory="src/lib/template")


def get_db_client():
    return DatabaseClient(Consts.REVIEW_SCHEMA_NAME)


async def insert_record_in_background(db_client: DatabaseClient, new_record: dict):
    db_client.insert_query("reviews", new_record)


def get_predictions(review_text: str, db_client: DatabaseClient, expanded_form=False):
    records = db_client.select_with_condition_query(
        Consts.REVIEW_TABLE_NAME, "review", data=review_text)

    if records:
        if expanded_form:
            return {"review": records[0]["review"],
                    "sentiment_text": records[0]["sentiment_text"],
                    "sentiment_prob": records[0]["sentiment_prob"]}

        return records[0]["sentiment_text"]
    else:
        predictions, best_prediction = model.predict(review_text)

        new_record = {"review": review_text.strip(
        ), "sentiment_text": best_prediction[0], "sentiment_prob": best_prediction[1]}

        asyncio.create_task(insert_record_in_background(db_client, new_record))

        if expanded_form:
            return new_record

        return best_prediction[0]


@router.post("/predict")
async def predict(request: Request,
                  review_text: str = Form(...),
                  db_client: DatabaseClient = Depends(get_db_client)):
    try:
        if "text/html" in request.headers.get("Accept", ""):
            sentiment_prediction = get_predictions(review_text, db_client)
            return templates.TemplateResponse("index.html", {"request": request, "predictions": sentiment_prediction, "title": "Predictions"})
        else:
            sentiment_prediction = get_predictions(
                review_text, db_client, expanded_form=True)
            return JSONResponse(content={"predictions": sentiment_prediction})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def predict_single_review(review_text: str, db_client: DatabaseClient):
    try:
        return get_predictions(review_text, db_client, expanded_form=True)
    except Exception as e:
        return {"error": str(e), "review_text": review_text}


@router.post("/predict-batch")
async def predict_batch(request: Request,
                        review_texts: List[str],
                        db_client: DatabaseClient = Depends(get_db_client)):
    try:
        tasks = [predict_single_review(text, db_client)
                 for text in review_texts]
        sentiment_predictions = await asyncio.gather(*tasks)

        return JSONResponse(content={"predictions": sentiment_predictions})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
