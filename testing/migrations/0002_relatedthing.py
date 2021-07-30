# Generated by Django 3.2.5 on 2021-07-29 06:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelatedThing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('data', models.JSONField(blank=True, default=None, null=True)),
                ('thing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testing.thing')),
            ],
        ),
    ]
