from fastapi import FastAPI, HTTPException
from calculator import add, subtract, multiply, divide

app = FastAPI(title="Calculator API")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/add")
def route_add(a: float, b: float):
    return {"result": add(a, b)}


@app.get("/subtract")
def route_subtract(a: float, b: float):
    return {"result": subtract(a, b)}


@app.get("/multiply")
def route_multiply(a: float, b: float):
    return {"result": multiply(a, b)}


@app.get("/divide")
def route_divide(a: float, b: float):
    try:
        return {"result": divide(a, b)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))