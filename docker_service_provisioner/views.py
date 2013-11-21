from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from docker_service_provisioner.service_pool import pool


def dockerfile(request, service, version):
    plugin = pool.get_plugin_class_from_params(service, version)
    return HttpResponse(plugin.dockerfile)