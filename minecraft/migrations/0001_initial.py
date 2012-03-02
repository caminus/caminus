# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Server'
        db.create_table('minecraft_server', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hostname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('port', self.gf('django.db.models.fields.IntegerField')(default=25565)),
        ))
        db.send_create_signal('minecraft', ['Server'])

        # Adding model 'MOTD'
        db.create_table('minecraft_motd', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['minecraft.Server'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('minecraft', ['MOTD'])


    def backwards(self, orm):
        
        # Deleting model 'Server'
        db.delete_table('minecraft_server')

        # Deleting model 'MOTD'
        db.delete_table('minecraft_motd')


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
            'port': ('django.db.models.fields.IntegerField', [], {'default': '25565'})
        }
    }

    complete_apps = ['minecraft']
