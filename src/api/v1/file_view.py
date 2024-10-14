import io
from PIL import Image
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status

from src.core.custom_logging import logger
from src.service.orc_service import recognize_text
from src.utils.authentication import check_internal_service_token

router = APIRouter()


@router.post(
    "",
    status_code=status.HTTP_200_OK,
    summary="Получние запрос на распознавание текста на картинке",
    response_description="Successful Response",
    response_model=None,
)
async def receive_webhook(
    file: UploadFile,
    service_check: bool = Depends(check_internal_service_token),
):
    if not service_check:
        logger.error("Unauthorized request")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        image = Image.open(io.BytesIO(await file.read()))
        text = recognize_text(image)
    except Exception as e:
        logger.error(f"Error create message request: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {e}"
        )

    return {"text": text}
