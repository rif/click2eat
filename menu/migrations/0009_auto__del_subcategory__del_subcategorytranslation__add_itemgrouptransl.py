# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'SubCategory'
        db.delete_table('menu_subcategory')

        # Deleting model 'SubCategoryTranslation'
        db.delete_table('menu_subcategorytranslation')

        # Adding model 'ItemGroupTranslation'
        db.create_table('menu_itemgrouptranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menu.Language'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menu.ItemGroup'])),
        ))
        db.send_create_signal('menu', ['ItemGroupTranslation'])

        # Adding model 'Topping'
        db.create_table('menu_topping', (
            ('item_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['menu.Item'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('menu', ['Topping'])

        # Adding M2M table for field topping_groups on 'Topping'
        db.create_table('menu_topping_topping_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('topping', models.ForeignKey(orm['menu.topping'], null=False)),
            ('toppinggroup', models.ForeignKey(orm['menu.toppinggroup'], null=False))
        ))
        db.create_unique('menu_topping_topping_groups', ['topping_id', 'toppinggroup_id'])

        # Adding model 'ToppingGroup'
        db.create_table('menu_toppinggroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('internal_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('menu', ['ToppingGroup'])

        # Deleting field 'Item.discount_time_end'
        db.delete_column('menu_item', 'discount_time_end')

        # Deleting field 'Item.sub_category'
        db.delete_column('menu_item', 'sub_category_id')

        # Deleting field 'Item.discount_time_start'
        db.delete_column('menu_item', 'discount_time_start')

        # Deleting field 'Item.discount'
        db.delete_column('menu_item', 'discount')

        # Deleting field 'Item.special'
        db.delete_column('menu_item', 'special')

        # Adding field 'Item.toppings'
        db.add_column('menu_item', 'toppings', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menu.ToppingGroup'], null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding model 'SubCategory'
        db.create_table('menu_subcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('internal_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('menu', ['SubCategory'])

        # Adding model 'SubCategoryTranslation'
        db.create_table('menu_subcategorytranslation', (
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menu.SubCategory'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menu.Language'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('menu', ['SubCategoryTranslation'])

        # Deleting model 'ItemGroupTranslation'
        db.delete_table('menu_itemgrouptranslation')

        # Deleting model 'Topping'
        db.delete_table('menu_topping')

        # Removing M2M table for field topping_groups on 'Topping'
        db.delete_table('menu_topping_topping_groups')

        # Deleting model 'ToppingGroup'
        db.delete_table('menu_toppinggroup')

        # Adding field 'Item.discount_time_end'
        db.add_column('menu_item', 'discount_time_end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)

        # Adding field 'Item.sub_category'
        db.add_column('menu_item', 'sub_category', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['menu.SubCategory']), keep_default=False)

        # Adding field 'Item.discount_time_start'
        db.add_column('menu_item', 'discount_time_start', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)

        # Adding field 'Item.discount'
        db.add_column('menu_item', 'discount', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'Item.special'
        db.add_column('menu_item', 'special', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Deleting field 'Item.toppings'
        db.delete_column('menu_item', 'toppings_id')


    models = {
        'menu.item': {
            'Meta': {'ordering': "['index']", 'object_name': 'Item'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'internal_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'item_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.ItemGroup']", 'null': 'True', 'blank': 'True'}),
            'measurement_unit': ('django.db.models.fields.CharField', [], {'default': "'GR'", 'max_length': '2'}),
            'new_item_end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
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
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'units_using_this'", 'to': "orm['restaurant.Currency']"}),
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
