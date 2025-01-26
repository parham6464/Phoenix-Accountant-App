# Generated by Django 4.2.10 on 2024-04-02 15:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hesabha',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_hesab', models.PositiveIntegerField(verbose_name='کد حساب کل')),
                ('name_hesab', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Moein',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_hesab', models.PositiveIntegerField(verbose_name='کد حساب معین')),
                ('name_hesab', models.CharField(max_length=200)),
                ('hesabha', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.hesabha')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='tafsili',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_hesab', models.PositiveIntegerField(verbose_name='کد حساب معین')),
                ('name_hesab', models.CharField(max_length=200)),
                ('moein', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.moein')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
