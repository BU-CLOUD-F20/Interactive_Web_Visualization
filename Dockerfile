FROM python:3.8
WORKDIR /code
# ENV FLASK=run.py
# ENV FLASK_RUN_HOST=0.0.0.0
# RUN apk add --no-cache musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8080
COPY . .

# might need to find a way to do flask run
CMD ["python", "run.py"] 
