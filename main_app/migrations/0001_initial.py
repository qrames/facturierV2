# Generated by Django 2.1.2 on 2018-10-02 09:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default='En attente de reglement', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business', models.CharField(max_length=150)),
                ('siren', models.IntegerField(max_length=14)),
                ('logo', models.ImageField(null=True, upload_to='media/user')),
                ('address', models.CharField(max_length=150)),
                ('zipcode', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(blank=True, max_length=250, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('short_desc', models.CharField(max_length=150)),
                ('pics', models.ImageField(upload_to='media/product')),
                ('price', models.FloatField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Quotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Customer', verbose_name='client')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='quotation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Quotation'),
        ),
        migrations.AddField(
            model_name='bill',
            name='quotation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Quotation', verbose_name='devis'),
        ),
    ]
