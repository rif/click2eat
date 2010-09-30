# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Item.index'
        db.add_column('menu_item', 'index', self.gf('django.db.models.fields.CharField')(default=1, max_length=50), keep_default=False)

        # Adding field 'ItemGroup.index'
        db.add_column('menu_itemgroup', 'index', self.gf('django.db.models.fields.CharField')(default=1, max_length=50), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Item.index'
        db.delete_column('menu_item', 'index')

        # Deleting field 'ItemGroup.index'
        db.delete_column('menu_itemgroup', 'index')


    models = {
        'menu.item': {
            'Meta': {'ordering': "['index']", 'object_name': 'Item'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'discount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'discount_time_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'discount_time_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'internal_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'item_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.ItemGroup']", 'null': 'True', 'blank': 'True'}),
            'new_item_end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'special': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sub_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.SubCategory']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.Unit']"}),
            'vat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.VAT']"})
        },
        'menu.itemgroup': {
            'Meta': {'ordering': "['index']", 'object_name': 'ItemGroup'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'exclusive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'internal_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.Unit']"})
        },
        'menu.itemtranslation': {
            'Meta': {'object_name': 'ItemTranslation'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.Language']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.Item']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'menu.language': {
            'Meta': {'object_name': 'Language'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'menu.subcategory': {
            'Meta': {'object_name': 'SubCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'menu.subcategorytranslation': {
            'Meta': {'object_name': 'SubCategoryTranslation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.Language']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.SubCategory']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'menu.vat': {
            'Meta': {'object_name': 'VAT'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'restaurant.communication': {
            'Meta': {'object_name': 'Communication'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'restaurant.deliveryarea': {
            'Meta': {'object_name': 'DeliveryArea'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'restaurant.deliverytype': {
            'Meta': {'object_name': 'DeliveryType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.FloatField', [], {})
        },
        'restaurant.employee': {
            'Meta': {'object_name': 'Employee'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        'restaurant.partnerpackage': {
            'Meta': {'object_name': 'PartnerPackage'},
            'details': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'restaurant.paymentmethod': {
            'Meta': {'object_name': 'PaymentMethod'},
            'details': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'restaurant.unit': {
            'Meta': {'object_name': 'Unit'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'admin_users': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'communication': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['restaurant.Communication']", 'symmetrical': 'False'}),
            'contact_person': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'delivery_time': ('django.db.models.fields.IntegerField', [], {}),
            'delivery_time_user': ('django.db.models.fields.FloatField', [], {}),
            'delivery_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.DeliveryType']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.Employee']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'logo_path': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'minimum_ord_val': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'open_hours': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'overall_discount': ('django.db.models.fields.FloatField', [], {}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.PartnerPackage']"}),
            'payment_method': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['restaurant.PaymentMethod']", 'symmetrical': 'False'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'unit_devlivery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.DeliveryArea']"})
        }
    }

    complete_apps = ['menu']
