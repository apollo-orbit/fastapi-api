from fastapi import FastAPI

app = FastAPI(
    title="API Chida",
    description="API simple con FastAPI",
    version="0.1.0"
)

@app.get("/")
def root():
    return {"message": "¡Que onda, mundo!"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/items/{item_id}")
def get_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
