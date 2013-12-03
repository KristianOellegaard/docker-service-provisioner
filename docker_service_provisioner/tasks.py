from docker.client import Client as DockerClient


def get_available_host():
    pass


def deploy_instance(docker_api_endpoint, service_name, env_vars, revision, memory, cpu, ports=None):
    c = DockerClient(docker_api_endpoint)
    res = c.create_container(
        image="docker-service-provisioner/%s:v%s" % (service_name, revision),
        environment=env_vars,
        # TODO: Implement memory and CPU
        #mem_limit=memory,
    )
    container_id = res['Id']
    c.start(container_id, port_bindings={"%s/tcp" % p: [{'HostIp': '', 'HostPort': ''}] for p in ports})

    # Use inspect_container, as c.ports() doesn't seem to work for some reason
    container = c.inspect_container(container_id)
    return container['ID'], {p: container['NetworkSettings']['Ports']["%s/tcp" % p][0]['HostPort'] for p in ports}