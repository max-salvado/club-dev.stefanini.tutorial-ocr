FROM python:3.8

WORKDIR /tutorial-ocr

COPY ./requirements.txt /tutorial-ocr/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /tutorial-ocr/requirements.txt
RUN apt update -y
RUN apt install tesseract-ocr -y
RUN apt install libtesseract-dev -y
RUN apt-get install tesseract-ocr-por -q -y

COPY ./tutorial-ocr /code/tutorial-ocr

CMD ["uvicorn", "tutorial-ocr.main:app", "--host", "0.0.0.0", "--port", "4040"]