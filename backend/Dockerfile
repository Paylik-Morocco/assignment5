FROM python:3.11.4

COPY . /drf_src

WORKDIR /drf_src

RUN ls .

RUN pip install -r requirements.txt

VOLUME /drf_src

EXPOSE 8000

CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
