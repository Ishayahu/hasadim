# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'File'
        db.create_table(u'gmah_file', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('file_name', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'gmah', ['File'])

        # Adding M2M table for field file on 'Claim'
        m2m_table_name = db.shorten_name(u'gmah_claim_file')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('claim', models.ForeignKey(orm[u'gmah.claim'], null=False)),
            ('file', models.ForeignKey(orm[u'gmah.file'], null=False))
        ))
        db.create_unique(m2m_table_name, ['claim_id', 'file_id'])


    def backwards(self, orm):
        # Deleting model 'File'
        db.delete_table(u'gmah_file')

        # Removing M2M table for field file on 'Claim'
        db.delete_table(db.shorten_name(u'gmah_claim_file'))


    models = {
        u'gmah.claim': {
            'Meta': {'ordering': "['id', 'open_date']", 'object_name': 'Claim'},
            'acl': ('django.db.models.fields.TextField', [], {'default': 'False'}),
            'close_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'for_claim'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['gmah.File']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'open_date': ('django.db.models.fields.DateTimeField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'worker_for_task'", 'to': u"orm['gmah.Person']"})
        },
        u'gmah.file': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'File'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
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