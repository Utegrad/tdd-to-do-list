# Generated by Django 2.2.3 on 2019-08-11 22:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=128)),
                ('list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lists.List')),
            ],
            options={
                'ordering': ('id',),
                'unique_together': {('text', 'list')},
            },
        ),
    ]
