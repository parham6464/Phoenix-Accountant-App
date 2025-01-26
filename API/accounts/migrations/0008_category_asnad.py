# Generated by Django 4.2.10 on 2024-04-03 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_hesabha_name_hesab_alter_moein_name_hesab_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shomare_sanad', models.PositiveIntegerField(unique=True)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_modify', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Asnad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kol', models.CharField(max_length=200)),
                ('moein', models.CharField(max_length=200)),
                ('tafs', models.CharField(max_length=200)),
                ('sharhe_hesab', models.CharField(max_length=200)),
                ('bedehkar', models.PositiveBigIntegerField(blank=True, null=True)),
                ('bestankar', models.PositiveBigIntegerField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.category')),
            ],
        ),
    ]
