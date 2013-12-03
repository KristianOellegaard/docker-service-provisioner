from django.contrib import admin

# Register your models here.
from models import *


class ServicePlanInline(admin.TabularInline):
    model = ServicePlan

class ServiceAdmin(admin.ModelAdmin):
    inlines = [ServicePlanInline, ]
    list_display = ('name', )

admin.site.register(Service, ServiceAdmin)


class ServiceInstanceConfigurationInline(admin.TabularInline):
    model = ServiceInstanceConfiguration
    extra = 0
    readonly_fields = ('name', 'value')


def deploy_instances(modeladmin, model, queryset):
    for instance in queryset:
        instance.deploy()

class ServiceInstanceAdmin(admin.ModelAdmin):
    inlines = [ServiceInstanceConfigurationInline, ]
    list_display = ('uuid', 'service_plan',)
    actions = [deploy_instances, ]
    readonly_fields = ('uri', 'uuid', 'container_id')

admin.site.register(ServiceInstance, ServiceInstanceAdmin)

admin.site.register(Host)