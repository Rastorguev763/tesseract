import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse

from src.api.v1 import file_view
from src.core.settings import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/tesseract/api/openapi" if settings.MODE == "DEV" else None,
    openapi_url="/tesseract/api/openapi.json" if settings.MODE == "DEV" else None,
    default_response_class=ORJSONResponse,
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return ORJSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


app.include_router(file_view.router, prefix="/tesseract/api/v1/orc", tags=["tesseract"])


if __name__ == "__main__":
    uvicorn.run("main:app", port=5050, host="localhost", reload=True)
