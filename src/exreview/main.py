from fastapi import FastAPI

app = FastAPI(
    title="Ex Review",
    description="A platform for sharing relation experiences",
    version="0.1.0",
)

@app.get("/")
async def root():
    return {"message": "Welcome to ExReview API",
            "status": "Application is running"}
