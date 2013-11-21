from django.core.management import BaseCommand
from docker_service_provisioner.models import Host
from docker_service_provisioner.service_pool import pool
from docker.client import Client as DockerClient
from urlparse import urljoin
from django.conf import settings

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        hosts = Host.objects.filter(use_for_building_images=True).order_by('?')
        if hosts:
            c = DockerClient(base_url=hosts[0].docker_api_endpoint)
            for plugin_dict in pool.get_all_plugin_dicts():
                result, log = c.build(
                    tag="docker-service-provisioner/%s:v%s" % (plugin_dict['service'], plugin_dict['version']),
                    path=urljoin(settings.DOCKER_PROVISION_URL, "dockerfile/%s/%s/" % (plugin_dict['service'], plugin_dict['version']))
                )
                if result:
                    print "Converted", plugin_dict['service'], plugin_dict['version'], 'to', result
                else:
                    print "Failed converting", plugin_dict['service'], plugin_dict['version'], 'to', result
        else:
            raise Exception("No hosts available for building images!")