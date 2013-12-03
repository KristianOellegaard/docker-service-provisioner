import json
from django.http import HttpResponse, Http404
from django.shortcuts import render

# Create your views here.
from docker_service_provisioner.models import ServicePlan, ServiceInstance
from docker_service_provisioner.service_pool import pool
from rest_framework import authentication, permissions, exceptions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView


def dockerfile(request, service, version):
    plugin = pool.get_plugin_class_from_params(service, version)
    return HttpResponse(plugin.dockerfile)

def exception_handler(exc):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's builtin `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['X-Throttle-Wait-Seconds'] = '%d' % exc.wait

        return Response({'detail': exc.detail},
                        status=exc.status_code if not exc.status_code == 403 else 401,  # Override 403s to 401s for compliance with Kensa
                        headers=headers)

    elif isinstance(exc, Http404):
        return Response({'detail': 'Not found'},
                        status=status.HTTP_404_NOT_FOUND)

    elif isinstance(exc, PermissionDenied):
        return Response({'detail': 'Permission denied'},
                        status=status.HTTP_401_UNAUTHORIZED)
    # Note: Unhandled exceptions will raise a 500 error.
    return None


class CustomAPIView(APIView):
    def permission_denied(self, request):
        raise exceptions.NotAuthenticated()


class ServiceInstanceProvisionAPIView(CustomAPIView):
    def post(self, request, service, format=None):
        """
        Request: POST https://username:password@api.heroku.com/heroku/resources
        Request Body: {
          "heroku_id": "app123@heroku.com",
          "plan": "basic",
          "region": "amazon-web-services::us-east-1",
          "callback_url": "https://api.heroku.com/vendor/apps/app123%40heroku.com",
          "logplex_token": "t.abc123",
          "options": {}
        }
        Response Body: {
          "id": 456,
          "config": {"MYADDON_URL": "http://myaddon.com/52e82f5d73"},
          "message": "your message here"
        }
        """
        try:
            body = json.loads(request.body)
        except ValueError:
            return Response({
                'message': 'No JSON received.'
            }, status=422)
        try:
            plan = ServicePlan.objects.get(name=body['plan'], service__name__iexact=service)
        except ServicePlan.DoesNotExist:
            raise Http404("Service plan %s does not exist for service %s" % (body['plan'], service))
        try:
            service_instance = ServiceInstance.provision(plan)
            return Response({
                'id': str(service_instance.uuid),
                'config': {("%s_URL" % service_instance.service_plan.service.name).upper(): service_instance.uri},
                'message': "Addon %s (%s) successfully provisioned" % (service_instance.service_plan.service.name,
                                                                       service_instance.service_plan.name)
            })
        except Exception as e:
            return Response({
                'message': 'An error has occured.'
            }, status=422)


class ServiceInstanceUpdateDeleteAPIView(CustomAPIView):
    def delete(self, request, service, uuid, format=None):
        """
        Request: DELETE https://username:password@api.heroku.com/heroku/resources/:id
        Request Body: none
        Response Status: 200
        """
        try:
            service_instance = ServiceInstance.objects.get(uuid=uuid, service_plan__service__name__iexact=service)
            service_instance.delete()
            return Response({
                'message': 'Success'
            })
        except Exception as e:
            return Response({
                'message': 'An error has occured.'
            }, status=422)

    def put(self, request, service, uuid, format=None):
        """
        Request: PUT https://username:password@api.heroku.com/heroku/resources/:id
        Request Body: {"heroku_id": "app123@heroku.com", "plan": "premium"}
        Response Body: {"config": { ... }, "message": "your message here"}
        """
        try:
            body = json.loads(request.body)
        except ValueError:
            return Response({
                'message': 'No JSON received.'
            }, status=422)
        try:
            plan = ServicePlan.objects.get(name=body['plan'], service__name__iexact=service)
            service_instance = ServiceInstance.objects.get(uuid=uuid, service_plan__service__name__iexact=service)
            service_instance.change_plan_to(plan)
            return Response({
                'message': 'Success'
            })
        except Exception as e:
            return Response({
                'message': 'An error has occured.'
            }, status=422)