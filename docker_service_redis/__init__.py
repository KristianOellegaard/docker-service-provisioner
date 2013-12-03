from docker_service_provisioner.service import DockerService, RandomText
from docker_service_provisioner.service_pool import pool


class RedisService(DockerService):
    dockerfile = """
FROM ubuntu

RUN echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list
RUN apt-get update
RUN apt-get upgrade -y

RUN apt-get install -y redis-server

EXPOSE 6379

RUN mkdir -p /redis-data
VOLUME ["/redis-data"]

RUN echo "#!/bin/bash\\necho \\"requirepass \${PASSWORD}\\n" > /run.sh
RUN echo "dir /redis-data\\" | redis-server -" >> /run.sh
RUN chmod +x /run.sh

CMD ["/run.sh"]
"""
    configuration = {
        'PASSWORD': RandomText
    }

    ports = [6379]

    def return_uri(self, service_instance, ports, env_vars):
        return "redis://:%s@%s:%s" % (env_vars['PASSWORD'], service_instance.host.hostname, ports[6379])

pool.register("redis", RedisService, version=1)