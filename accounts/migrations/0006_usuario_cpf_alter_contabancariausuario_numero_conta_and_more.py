# Generated by Django 5.0.6 on 2024-08-02 02:22

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_usuario_cpf_alter_usuario_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='cpf',
            field=models.CharField(default=0, max_length=11, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contabancariausuario',
            name='numero_conta',
            field=models.CharField(max_length=11, unique=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='username',
            field=models.CharField(default=0, error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
            preserve_default=False,
        ),
    ]
