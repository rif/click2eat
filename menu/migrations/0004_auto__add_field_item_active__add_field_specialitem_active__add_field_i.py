# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Item.active'
        db.add_column('menu_item', 'active', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SpecialItem.active'
        db.add_column('menu_specialitem', 'active', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'ItemGroup.active'
        db.add_column('menu_itemgroup', 'active', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Item.active'
        db.delete_column('menu_item', 'active')

        # Deleting field 'SpecialItem.active'
        db.delete_column('menu_specialitem', 'active')

        # Deleting field 'ItemGroup.active'
        db.delete_column('menu_itemgroup', 'active')


    models = {
        'menu.item': {
            'Meta': {'object_name': 'Item'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'discount': ('django.db.models.fields.IntegerField', [], {}),
            'discount_time_end': ('django.db.models.fields.DateTimeField', [], {}),
            'discount_time_start': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'item_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.ItemGroup']"}),
            'new_item_end_date': ('django.db.models.fields.DateField', [], {}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'special': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sub_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.SubCategory']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.Unit']"}),
            'vat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.VAT']"})
        },
        'menu.itemgroup': {
            'Meta': {'object_name': 'ItemGroup'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'exclusive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
        'menu.specialitem': {
            'Meta': {'object_name': 'SpecialItem'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'item_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.ItemGroup']"}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'time_end': ('django.db.models.fields.DateTimeField', [], {}),
            'time_start': ('django.db.models.fields.DateTimeField', [], {}),
            'vat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.VAT']"})
        },
        'menu.specialitemtranslation': {
            'Meta': {'object_name': 'SpecialItemTranslation'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.Language']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.SpecialItem']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'payment_method': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.PaymentMethod']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'unit_devlivery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.DeliveryArea']"})
        }
    }

    complete_apps = ['menu']
