FROM python:3.8.5
WORKDIR /inside24
COPY requirements.txt /inside24
RUN pip install --upgrade pip -r requirements.txt
COPY . /inside24
EXPOSE 5000
CMD python3 inside24/inside24.py