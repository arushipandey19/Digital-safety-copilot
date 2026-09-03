from fastapi import FastAPI
from app.routes.analyze import router as analyze_router

app=FastAPI()

app.include_router(analyze_router)


@app.get("/")
def root():
    return {"message":"Digital Safety Copilot Backend is running!!"}