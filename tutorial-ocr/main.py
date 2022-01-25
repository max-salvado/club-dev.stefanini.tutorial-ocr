from fastapi import FastAPI, File, UploadFile
from PIL import Image, ImageFilter
import base64
import pytesseract
from pydantic import BaseModel


class ImageToProcess(BaseModel):
    base64: str


app = FastAPI()


@app.post("/image/")
async def upload_test_file(file: UploadFile = File(...)):
    """
    Permite fazer o upload de imagem para leitura com OCR.
    """
    return write_text_by_image({"base64": str(base64.b64encode(await file.read()).decode("utf-8"))})


def write_text_by_image(image: ImageToProcess):
    """
    Passagem do base64 pelo Pytesseract.
    """
    img_data = ""
    try:
        img_data = bytes(image["base64"], 'utf-8')
    except AttributeError:
        img_data = bytes(image.base64, 'utf-8')

    with open("image.png", "wb") as fh:
        fh.write(base64.decodebytes(img_data))

    img = Image.open('image.png')

    threshold = 130
    # Grayscale
    img = img.convert('L')
    # Threshold
    img = img.point(lambda p: 255 if p > threshold else 0)
    # To mono
    img = img.convert('1')
    img = img.filter(ImageFilter.MedianFilter())

    text = pytesseract.image_to_string(img, lang='por')
    text = text.replace("\f", "")
    text = [x for x in text.split("\n") if x]

    return text
