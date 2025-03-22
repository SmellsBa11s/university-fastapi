from fastapi import FastAPI
from src.routers import router


app = FastAPI(
    title="University FastAPI",
    description="API для университета",
    version="1.0.0",
)
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
