# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Server.query_port'
        db.add_column('minecraft_server', 'query_port', self.gf('django.db.models.fields.IntegerField')(default=25565), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Server.query_port'
        db.delete_column('minecraft_server', 'query_port')


    models = {
        'minecraft.motd': {
            'Meta': {'object_name': 'MOTD'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['minecraft.Server']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'minecraft.server': {
            'Meta': {'object_name': 'Server'},
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'port': ('django.db.models.fields.IntegerField', [], {'default': '25565'}),
            'query_port': ('django.db.models.fields.IntegerField', [], {'default': '25565'})
        }
    }

    complete_apps = ['minecraft']
