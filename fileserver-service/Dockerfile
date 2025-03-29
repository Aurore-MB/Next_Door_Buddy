
FROM python:3.12

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./main.py /app/main.py

# EXPOSE 7004

# CMD ["uvicorn", "app:app", "--port", "7004", "--host", "0.0.0.0", "--reload"]

CMD ["python3", "main.py"]