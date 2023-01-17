# Generated by Django 4.1.5 on 2023-01-17 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0010_alter_giftorder_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giftorder',
            name='amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='giftorder',
            name='offer',
            field=models.ForeignKey(db_column='offer_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='data.offer'),
        ),
    ]
