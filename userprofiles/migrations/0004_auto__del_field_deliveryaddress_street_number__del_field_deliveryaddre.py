# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'DeliveryAddress.street_number'
        db.delete_column('userprofiles_deliveryaddress', 'street_number')

        # Deleting field 'DeliveryAddress.house_number'
        db.delete_column('userprofiles_deliveryaddress', 'house_number')

        # Adding field 'DeliveryAddress.number'
        db.add_column('userprofiles_deliveryaddress', 'number', self.gf('django.db.models.fields.CharField')(default='', max_length=5), keep_default=False)

        # Adding field 'DeliveryAddress.block'
        db.add_column('userprofiles_deliveryaddress', 'block', self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True), keep_default=False)

        # Adding field 'DeliveryAddress.entrance'
        db.add_column('userprofiles_deliveryaddress', 'entrance', self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True), keep_default=False)

        # Adding field 'DeliveryAddress.geolocated_address'
        db.add_column('userprofiles_deliveryaddress', 'geolocated_address', self.gf('django.db.models.fields.CharField')(default='', max_length=200), keep_default=False)

        # Adding field 'DeliveryAddress.latitude'
        db.add_column('userprofiles_deliveryaddress', 'latitude', self.gf('django.db.models.fields.FloatField')(default=1), keep_default=False)

        # Adding field 'DeliveryAddress.longitude'
        db.add_column('userprofiles_deliveryaddress', 'longitude', self.gf('django.db.models.fields.FloatField')(default=1), keep_default=False)

        # Changing field 'DeliveryAddress.floor'
        db.alter_column('userprofiles_deliveryaddress', 'floor', self.gf('django.db.models.fields.SmallIntegerField')(null=True))

        # Changing field 'DeliveryAddress.ap_number'
        db.alter_column('userprofiles_deliveryaddress', 'ap_number', self.gf('django.db.models.fields.SmallIntegerField')(null=True))


    def backwards(self, orm):
        
        # Adding field 'DeliveryAddress.street_number'
        db.add_column('userprofiles_deliveryaddress', 'street_number', self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True), keep_default=False)

        # Adding field 'DeliveryAddress.house_number'
        db.add_column('userprofiles_deliveryaddress', 'house_number', self.gf('django.db.models.fields.CharField')(default=1, max_length=5), keep_default=False)

        # Deleting field 'DeliveryAddress.number'
        db.delete_column('userprofiles_deliveryaddress', 'number')

        # Deleting field 'DeliveryAddress.block'
        db.delete_column('userprofiles_deliveryaddress', 'block')

        # Deleting field 'DeliveryAddress.entrance'
        db.delete_column('userprofiles_deliveryaddress', 'entrance')

        # Deleting field 'DeliveryAddress.geolocated_address'
        db.delete_column('userprofiles_deliveryaddress', 'geolocated_address')

        # Deleting field 'DeliveryAddress.latitude'
        db.delete_column('userprofiles_deliveryaddress', 'latitude')

        # Deleting field 'DeliveryAddress.longitude'
        db.delete_column('userprofiles_deliveryaddress', 'longitude')

        # Changing field 'DeliveryAddress.floor'
        db.alter_column('userprofiles_deliveryaddress', 'floor', self.gf('django.db.models.fields.SmallIntegerField')())

        # Changing field 'DeliveryAddress.ap_number'
        db.alter_column('userprofiles_deliveryaddress', 'ap_number', self.gf('django.db.models.fields.SmallIntegerField')())


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'restaurant.communication': {
            'Meta': {'object_name': 'Communication'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'userprofiles.deliveryaddress': {
            'Meta': {'ordering': "['-primary']", 'object_name': 'DeliveryAddress'},
            'additional_info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ap_number': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'block': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "'Timisoara'", 'max_length': '50'}),
            'entrance': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'floor': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'geolocated_address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'userprofiles.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'communication': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['restaurant.Communication']", 'symmetrical': 'False'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'newsletter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['userprofiles']
