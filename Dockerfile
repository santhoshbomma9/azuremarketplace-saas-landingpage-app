# docker build -t image-name .
# docker run -p 80:80 -it image-name
# docker stop $(docker ps -a -q) -> stops all containers
# docker rm $(docker ps -a -q)   -> removes all containers
# docker rmi $(docker images -q) -> removes all images
# docker tag test santhosh2netdocker/test:1 -> tag docker
# docker container rm --force bb -> remove one container
# docker run -d -t -i -e REDIS_NAMESPACE='staging' -> loading env variables
# docker run  -e TENANT_ID=123 -e CLIENT_ID=123 -e CLIENT_SECRET=123 -e MARKETPLACEAPI_TENANTID=123 -e MARKETPLACEAPI_CLIENT_ID=123 -e MARKETPLACEAPI_CLIENT_SECRET=123  -p 5000:5000 -it amp:latest
# docker push yourhubusername/dockerimage

FROM python:3.6
ADD . /amp_app
WORKDIR /amp_app
ENV STATIC_URL static
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "startup:app"]


# Pull a pre-built alpine docker image with nginx and python3 installed
# FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7

# Set the port on which the app runs; make both values the same.
#
# IMPORTANT: When deploying to Azure App Service, go to the App Service on the Azure 
# portal, navigate to the Applications Settings blade, and create a setting named
# WEBSITES_PORT with a value that matches the port here (the Azure default is 80).
# You can also create a setting through the App Service Extension in VS Code.
# ENV LISTEN_PORT=5000
# EXPOSE 5000

# Indicate where uwsgi.ini lives
# ENV UWSGI_INI uwsgi.ini

# Tell nginx where static files live. Typically, developers place static files for
# multiple apps in a shared folder, but for the purposes here we can use the one
# app's folder. Note that when multiple apps share a folder, you should create subfolders
# with the same name as the app underneath "static" so there aren't any collisions
# when all those static files are collected together.
# ENV STATIC_URL /amp_app/static

# Set the folder where uwsgi looks for the app
# WORKDIR /amp_app

# Copy the app contents to the image
# COPY . /amp_app

# If you have additional requirements beyond Flask (which is included in the
# base image), generate a requirements.txt file with pip freeze and uncomment
# the next three lines.
#COPY requirements.txt /
#RUN pip install --no-cache-dir -U pip
#RUN pip install --no-cache-dir -r /requirements.txt
