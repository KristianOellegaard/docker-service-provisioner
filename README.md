docker-service-provisioner
==========================

This is a regular Django app and you can follow the standard way to bootstrap it:

- python manage.py syncdb --all
- python manage.py migrate --fake
- python manage.py runserver

Build docker images
-------------------

First, go to the admin panel and create a service and a service plan, e.g. the pre-shipped redis service

```bash
export DOCKER_PROVISION_URL=<url to django, e.g. http://10.0.0.1:8000/>
export DOCKER_IMAGE_SERVER=<url to docker image server, e.g. http://10.0.0.2:8000/>
python manage.py build_docker_images
```

**You have to run docker on a TCP socket, remember it must be on a private network or everyone can play around with it!**
E.g. 
```docker -d -H tcp://0.0.0.0:12345```
