# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'SpecialItemTranslation'
        db.create_table('menu_specialitemtranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menu.Language'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menu.SpecialItem'])),
        ))
        db.send_create_signal('menu', ['SpecialItemTranslation'])

        # Adding model 'SubCategoryTranslation'
        db.create_table('menu_subcategorytranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menu.Language'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menu.SubCategory'])),
        ))
        db.send_create_signal('menu', ['SubCategoryTranslation'])

        # Deleting field 'SubCategory.name'
        db.delete_column('menu_subcategory', 'name')

        # Adding field 'SubCategory.internal_name'
        db.add_column('menu_subcategory', 'internal_name', self.gf('django.db.models.fields.CharField')(default='', max_length=50), keep_default=False)

        # Deleting field 'SpecialItem.description'
        db.delete_column('menu_specialitem', 'description')

        # Deleting field 'SpecialItem.name'
        db.delete_column('menu_specialitem', 'name')

        # Adding field 'SpecialItem.internal_name'
        db.add_column('menu_specialitem', 'internal_name', self.gf('django.db.models.fields.CharField')(default='', max_length=50), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'SpecialItemTranslation'
        db.delete_table('menu_specialitemtranslation')

        # Deleting model 'SubCategoryTranslation'
        db.delete_table('menu_subcategorytranslation')

        # Adding field 'SubCategory.name'
        db.add_column('menu_subcategory', 'name', self.gf('django.db.models.fields.CharField')(default='', max_length=50), keep_default=False)

        # Deleting field 'SubCategory.internal_name'
        db.delete_column('menu_subcategory', 'internal_name')

        # Adding field 'SpecialItem.description'
        db.add_column('menu_specialitem', 'description', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)

        # Adding field 'SpecialItem.name'
        db.add_column('menu_specialitem', 'name', self.gf('django.db.models.fields.CharField')(default='', max_length=100), keep_default=False)

        # Deleting field 'SpecialItem.internal_name'
        db.delete_column('menu_specialitem', 'internal_name')


    models = {
        'menu.item': {
            'Meta': {'object_name': 'Item'},
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
            'communication': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.Communication']"}),
            'contact_person': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'delivery_time': ('django.db.models.fields.IntegerField', [], {}),
            'delivery_time_user': ('django.db.models.fields.FloatField', [], {}),
            'delivery_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.DeliveryType']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.Employee']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
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
