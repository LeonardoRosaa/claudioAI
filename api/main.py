from fastapi import FastAPI
from api.routes import ( conversation_router )
from api.infrastructure.logger import logger

app = FastAPI()

logger.info("Claudio API is starting up")

app.include_router(conversation_router, prefix="/conversations", tags=["conversations"])

@app.get("/healthy")
def root():
    return { "msg": "Hello World" }