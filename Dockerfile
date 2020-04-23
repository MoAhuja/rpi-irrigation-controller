FROM python:latest

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "./irrigation_controller/app.py"]

# Expose port 5000 of flask
EXPOSE 5000
