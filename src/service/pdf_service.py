from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError
from src.core.custom_logging import logger


async def recognize_text_dpf(pdf_file_stream):
    result = {
        "text": None,
        "metadata": None,
        "error": None,
    }

    try:
        # Создаем объект PDF reader
        reader = PdfReader(pdf_file_stream)

        # Получаем метаданные
        result["metadata"] = reader.metadata

        # Получаем текст из файла
        text = reader.pages[0].extract_text()

        if text is None:
            logger.error("Не удалось извлечь текст")
            result["error"] = (
                "Не удалось извлечь текст. PDF может быть сохранен как изображение."
            )
        else:
            result["text"] = text

    except PdfReadError as e:
        logger.error(f"Ошибка чтения PDF: {str(e)}")
        result["error"] = f"Ошибка чтения PDF: {str(e)}"
    except Exception as e:
        logger.error(f"Произошла ошибка при распознавании текста: {str(e)}")
        result["error"] = f"Произошла ошибка: {str(e)}"

    return result
