FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

COPY ./app /app
RUN pip3 install --no-cache-dir -U -r /app/requirements.txt
RUN touch /app/server_list.json

# FROM python:3.8-alpine

# COPY ./app /app
# RUN pip3 install --no-cache-dir -U -r /app/requirements.txt
# RUN touch /app/server_list.json
# CMD [ "python", "/app/main.py" ]