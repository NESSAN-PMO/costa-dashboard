FROM python:latest

COPY manage.py gunicorn-cfg.py requirements.txt .env /django/

RUN pip install -r /django/requirements.txt -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

WORKDIR /django
COPY app /django/app
COPY authentication /django/authentication
COPY core /django/core
#RUN python manage.py makemigrations
#RUN python manage.py migrate

EXPOSE 5005
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]
