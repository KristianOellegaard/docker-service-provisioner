# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Host'
        db.create_table(u'docker_service_provisioner_host', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('uuidfield.fields.UUIDField')(unique=True, max_length=32, blank=True)),
            ('hostname', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('docker_api_endpoint', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('use_for_building_images', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('use_for_running_images', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'docker_service_provisioner', ['Host'])

        # Adding model 'Service'
        db.create_table(u'docker_service_provisioner_service', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'docker_service_provisioner', ['Service'])

        # Adding model 'ServicePlan'
        db.create_table(u'docker_service_provisioner_serviceplan', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['docker_service_provisioner.Service'])),
            ('service_backend', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('ram', self.gf('django.db.models.fields.IntegerField')(default=128)),
            ('cpu_weight', self.gf('django.db.models.fields.DecimalField')(default=1, max_digits=8, decimal_places=2)),
            ('disk_space', self.gf('django.db.models.fields.IntegerField')(default=128)),
        ))
        db.send_create_signal(u'docker_service_provisioner', ['ServicePlan'])

        # Adding model 'ServiceInstance'
        db.create_table(u'docker_service_provisioner_serviceinstance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('uuidfield.fields.UUIDField')(unique=True, max_length=32, blank=True)),
            ('host', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['docker_service_provisioner.Host'])),
            ('service_plan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['docker_service_provisioner.ServicePlan'])),
        ))
        db.send_create_signal(u'docker_service_provisioner', ['ServiceInstance'])

        # Adding model 'ServiceInstanceConfiguration'
        db.create_table(u'docker_service_provisioner_serviceinstanceconfiguration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('service_instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['docker_service_provisioner.ServiceInstance'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'docker_service_provisioner', ['ServiceInstanceConfiguration'])


    def backwards(self, orm):
        # Deleting model 'Host'
        db.delete_table(u'docker_service_provisioner_host')

        # Deleting model 'Service'
        db.delete_table(u'docker_service_provisioner_service')

        # Deleting model 'ServicePlan'
        db.delete_table(u'docker_service_provisioner_serviceplan')

        # Deleting model 'ServiceInstance'
        db.delete_table(u'docker_service_provisioner_serviceinstance')

        # Deleting model 'ServiceInstanceConfiguration'
        db.delete_table(u'docker_service_provisioner_serviceinstanceconfiguration')


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
            'host': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['docker_service_provisioner.Host']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service_plan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['docker_service_provisioner.ServicePlan']"}),
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