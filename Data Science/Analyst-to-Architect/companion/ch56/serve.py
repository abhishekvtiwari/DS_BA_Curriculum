#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 56 · the defect model, served.
A small FastAPI service around Chapter 53's model: one health endpoint, one prediction endpoint, and
the three things a production service needs beyond the prediction itself - input validation, the model
version in every response, and a log line per request that monitoring can read.
These are exactly the definitions built cell by cell in section 56.5, without the print lines.
Needs: models/defect_v1.joblib, written by section 56.4's cells.
Run it, from this folder:  uvicorn serve:app --port 8056      (then POST to http://127.0.0.1:8056/predict)
Tested on: Python 3.11.15, FastAPI 0.141.1, pydantic 2.13.5, uvicorn 0.54.0, scikit-learn 1.9.1.
"""
import json
import logging
import time

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


class Part(BaseModel):
    part_id: str = Field(min_length=1, max_length=40)
    features: list[float] = Field(min_length=108, max_length=108)


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
log = logging.getLogger("defect-service")

bundle = joblib.load("models/defect_v1.joblib")          # the model AND its metadata travel together (section 56.4)
model, metadata = bundle["model"], bundle["metadata"]
app = FastAPI(title="Riverstone defect detector", version=metadata["version"])


@app.get("/health")
def health() -> dict:
    """Liveness and readiness in one: the service is up AND the model is loaded."""
    return {"status": "ok", "model_version": metadata["version"], "threshold": metadata["threshold"]}


@app.post("/predict")
def predict(part: Part) -> dict:
    started = time.perf_counter()
    values = np.asarray(part.features, dtype=float)
    if not np.isfinite(values).all():
        raise HTTPException(status_code=422, detail="features contain NaN or infinity")
    probability = float(model.predict_proba(values.reshape(1, -1))[0, 1])
    verdict = "defective" if probability > metadata["threshold"] else "good"
    elapsed_ms = (time.perf_counter() - started) * 1000
    log.info(json.dumps({"part_id": part.part_id, "probability": round(probability, 4),
                         "verdict": verdict, "model_version": metadata["version"],
                         "latency_ms": round(elapsed_ms, 2), "mean_feature": round(float(values.mean()), 4)}))
    return {"part_id": part.part_id, "probability": round(probability, 4), "verdict": verdict,
            "model_version": metadata["version"], "threshold": metadata["threshold"],
            "latency_ms": round(elapsed_ms, 2)}
