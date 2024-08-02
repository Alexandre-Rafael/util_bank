# Generated by Django 5.0.6 on 2024-08-02 01:26

import accounts.managers
import django.contrib.auth.models
import django.contrib.auth.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usuario',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterModelManagers(
            name='usuario',
            managers=[
                ('objetos', accounts.managers.GerenciadorUsuarios()),
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='primeiro_nome',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='eh_superusuario',
            new_name='is_superuser',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='ultimo_login',
            new_name='last_login',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='ultimo_nome',
            new_name='last_name',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='senha',
            new_name='password',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='grupos',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='permissoes_usuarios',
        ),
        migrations.AddField(
            model_name='contabancariausuario',
            name='data_inicio_juros',
            field=models.DateField(blank=True, help_text='O número do mês que o cálculo de juros começará', null=True),
        ),
        migrations.AddField(
            model_name='usuario',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='username',
            field=models.CharField(default=0, error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contabancariausuario',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
