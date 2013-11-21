from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^dockerfile/(?P<service>\w+)/(?P<version>\d{1,4})/$', 'docker_service_provisioner.views.dockerfile', name='dockerfile'),
)
