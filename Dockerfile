FROM python:3.9
COPY . /searchengine
WORKDIR /searchengine
RUN python --version
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python","app.py"]