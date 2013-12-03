# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ServiceInstance.uri'
        db.add_column(u'docker_service_provisioner_serviceinstance', 'uri',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=256),
                      keep_default=False)

        # Adding field 'ServiceInstance.container_id'
        db.add_column(u'docker_service_provisioner_serviceinstance', 'container_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=128),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ServiceInstance.uri'
        db.delete_column(u'docker_service_provisioner_serviceinstance', 'uri')

        # Deleting field 'ServiceInstance.container_id'
        db.delete_column(u'docker_service_provisioner_serviceinstance', 'container_id')


    models = {
        u'docker_service_provisioner.host': {
            'Meta': {'object_name': 'Host'},
            'docker_api_endpoint': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'use_for_building_images': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_for_running_images': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'blank': 'True'})
        },
        u'docker_service_provisioner.service': {
            'Meta': {'object_name': 'Service'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'docker_service_provisioner.serviceinstance': {
            'Meta': {'object_name': 'ServiceInstance'},
            'container_id': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['docker_service_provisioner.Host']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service_plan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['docker_service_provisioner.ServicePlan']"}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'blank': 'True'})
        },
        u'docker_service_provisioner.serviceinstanceconfiguration': {
            'Meta': {'object_name': 'ServiceInstanceConfiguration'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'service_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['docker_service_provisioner.ServiceInstance']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'docker_service_provisioner.serviceplan': {
            'Meta': {'object_name': 'ServicePlan'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'cpu_weight': ('django.db.models.fields.DecimalField', [], {'default': '1', 'max_digits': '8', 'decimal_places': '2'}),
            'disk_space': ('django.db.models.fields.IntegerField', [], {'default': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'ram': ('django.db.models.fields.IntegerField', [], {'default': '128'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['docker_service_provisioner.Service']"}),
            'service_backend': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['docker_service_provisioner']