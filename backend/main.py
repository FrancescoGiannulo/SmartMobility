from fastapi import FastAPI

app = FastAPI(title="SmartMobility API")


@app.get("/")
def root():
    return {"status": "ok", "message": "SmartMobility API attiva"}
