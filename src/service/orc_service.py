import pytesseract


def recognize_text(image):
    # Используем Tesseract OCR для распознавания текста
    text = pytesseract.image_to_string(image, lang="rus")

    return text
