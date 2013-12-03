import json
import traceback
from django.db import models
from django.db.models.signals import post_save
from docker_service_provisioner.service_pool import pool
from docker_service_provisioner.tasks import deploy_instance, delete_instance
from uuidfield import UUIDField
from django.db import transaction


def get_available_host(service_backend):
    return Host.objects.filter()[0]


class Host(models.Model):
    uuid = UUIDField(auto=True)
    hostname = models.CharField(max_length=256)

    docker_api_endpoint = models.CharField(max_length=128)

    last_update = models.DateTimeField(null=True, blank=True)

    use_for_building_images = models.BooleanField(default=False)
    use_for_running_images = models.BooleanField(default=True)

    def __unicode__(self):
        return self.hostname


class Service(models.Model):
    """
    If multiple versions of a software is supported, those should be separate services
    """
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return u"%s" % self.name


class ServicePlan(models.Model):
    service = models.ForeignKey(Service)
    service_backend = models.CharField(max_length=32, choices=pool.choices)
    name = models.CharField(max_length=64)
    active = models.BooleanField(default=True)

    # Docker specific
    ram = models.IntegerField(default=128)
    cpu_weight = models.DecimalField(max_digits=8, decimal_places=2, default=1)
    disk_space = models.IntegerField(default=128)  # In megabytes

    def __unicode__(self):
        return u"%s: %s" % (self.service, self.name)


class ServiceInstance(models.Model):
    uuid = UUIDField(auto=True)
    host = models.ForeignKey(Host)
    service_plan = models.ForeignKey(ServicePlan)
    uri = models.CharField(max_length=256, editable=False)
    container_id = models.CharField(max_length=128, editable=False)

    def deploy(self):
        env_vars = {
            instance_config.name: instance_config.value
            for instance_config in self.serviceinstanceconfiguration_set.all()
        }
        service_backend_dict = pool.get_dict(self.service_plan.service_backend)
        container_id, ports = deploy_instance(
            self.host.docker_api_endpoint,
            service_backend_dict['service'],
            env_vars,
            service_backend_dict['version'],
            self.service_plan.ram * 1024 * 1024,
            self.service_plan.cpu_weight,
            service_backend_dict['plugin'].ports,
        )
        self.uri = service_backend_dict['plugin']().return_uri(self, ports, env_vars)
        self.container_id = container_id
        self.save()

    def change_plan_to(self, new_plan):
        self.service_plan = new_plan
        # TODO: Make the backends able to implement this in a custom way
        self.save()

    def delete(self, using=None):
        with transaction.atomic():
            service_backend_dict = pool.get_dict(self.service_plan.service_backend)
            delete_instance(
                self.host.docker_api_endpoint,
                service_backend_dict['service'],
                self.container_id
            )
            return super(ServiceInstance, self).delete(using=using)

    def __unicode__(self):
        return u"%s" % self.uuid

    @classmethod
    def provision(cls, service_plan):
        obj = cls.objects.create(
            host=get_available_host(service_plan.service_backend),
            service_plan=service_plan,
        )
        obj.deploy()
        return obj


def create_service_instance_configuration(sender, instance, created, *args, **kwargs):
    if created:
        for name, value_cls in pool.get_plugin_class(instance.service_plan.service_backend).configuration.items():
            ServiceInstanceConfiguration.objects.create(
                service_instance=instance,
                name=name,
                value=value_cls().generate(),
            )

post_save.connect(create_service_instance_configuration, sender=ServiceInstance, dispatch_uid="create_service_instance_configuration")


class ServiceInstanceConfiguration(models.Model):
    service_instance = models.ForeignKey(ServiceInstance)
    name = models.CharField(max_length=64)
    value = models.CharField(max_length=256)
