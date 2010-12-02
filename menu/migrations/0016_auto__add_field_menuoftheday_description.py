# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'MenuOfTheDay.description'
        db.add_column('menu_menuoftheday', 'description', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)

        # Removing M2M table for field items on 'MenuOfTheDay'
        db.delete_table('menu_menuoftheday_items')


    def backwards(self, orm):
        
        # Deleting field 'MenuOfTheDay.description'
        db.delete_column('menu_menuoftheday', 'description')

        # Adding M2M table for field items on 'MenuOfTheDay'
        db.create_table('menu_menuoftheday_items', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('menuoftheday', models.ForeignKey(orm['menu.menuoftheday'], null=False)),
            ('item', models.ForeignKey(orm['menu.item'], null=False))
        ))
        db.create_unique('menu_menuoftheday_items', ['menuoftheday_id', 'item_id'])


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'menu.item': {
            'Meta': {'ordering': "['index']", 'object_name': 'Item'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'added_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description_def': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'internal_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'item_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.ItemGroup']", 'null': 'True', 'blank': 'True'}),
            'measurement_unit': ('django.db.models.fields.CharField', [], {'default': "'GR'", 'max_length': '2'}),
            'name_def': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'promotion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.Promotion']", 'null': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'toppings': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.ToppingGroup']", 'null': 'True', 'blank': 'True'}),
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
            'name_def': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.Unit']"})
        },
        'menu.itemgrouptranslation': {
            'Meta': {'object_name': 'ItemGroupTranslation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.Language']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.ItemGroup']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
        'menu.menuoftheday': {
            'Meta': {'ordering': "['-day']", 'object_name': 'MenuOfTheDay'},
            'day': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.Unit']"})
        },
        'menu.promotion': {
            'Meta': {'ordering': "['-start_date']", 'object_name': 'Promotion'},
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'end_hour': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'start_hour': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.Unit']"}),
            'value': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'weekdays': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '13', 'null': 'True', 'blank': 'True'})
        },
        'menu.topping': {
            'Meta': {'ordering': "['index']", 'object_name': 'Topping', '_ormbases': ['menu.Item']},
            'item_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['menu.Item']", 'unique': 'True', 'primary_key': 'True'}),
            'topping_groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['menu.ToppingGroup']", 'symmetrical': 'False'})
        },
        'menu.toppinggroup': {
            'Meta': {'object_name': 'ToppingGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'menu.vat': {
            'Meta': {'object_name': 'VAT'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'restaurant.communication': {
            'Meta': {'object_name': 'Communication'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'restaurant.currency': {
            'Meta': {'object_name': 'Currency'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
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
            'rate': ('django.db.models.fields.FloatField', [], {}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        'restaurant.partnerpackage': {
            'Meta': {'object_name': 'PartnerPackage'},
            'details': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monthly_fee': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rate': ('django.db.models.fields.FloatField', [], {}),
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
            'added_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'admin_users': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'communication': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['restaurant.Communication']", 'symmetrical': 'False'}),
            'contact_person': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'units_using_this'", 'to': "orm['restaurant.Currency']"}),
            'delivery_range': ('django.db.models.fields.FloatField', [], {}),
            'delivery_time': ('django.db.models.fields.IntegerField', [], {}),
            'delivery_time_user': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'delivery_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.DeliveryType']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.Employee']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'logo_path': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'minimum_ord_val': ('django.db.models.fields.IntegerField', [], {}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'overall_discount': ('django.db.models.fields.FloatField', [], {}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.PartnerPackage']"}),
            'payment_method': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['restaurant.PaymentMethod']", 'symmetrical': 'False'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        }
    }

    complete_apps = ['menu']
