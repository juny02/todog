from fastapi import FastAPI

app = FastAPI(title="ToDOG API")

@app.get("/health")
def check_health():
    return {} 