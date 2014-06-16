# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Person.login'
        db.alter_column(u'gmah_person', 'login', self.gf('django.db.models.fields.CharField')(default='', max_length=140))

    def backwards(self, orm):

        # Changing field 'Person.login'
        db.alter_column(u'gmah_person', 'login', self.gf('django.db.models.fields.CharField')(max_length=140, null=True))

    models = {
        u'gmah.claim': {
            'Meta': {'ordering': "['id', 'open_date']", 'object_name': 'Claim'},
            'acl': ('django.db.models.fields.TextField', [], {'default': 'False'}),
            'close_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'open_date': ('django.db.models.fields.DateTimeField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'worker_for_task'", 'to': u"orm['gmah.Person']"})
        },
        u'gmah.person': {
            'Meta': {'ordering': "['fio']", 'object_name': 'Person'},
            'fio': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'raiting': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['gmah']