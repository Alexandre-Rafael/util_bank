
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userbankaccount',
            name='account_no',
        ),
        migrations.AddField(
            model_name='userbankaccount',
            name='cpf',
            field=models.CharField(default=0, max_length=11, unique=True),
            preserve_default=False,
        ),
    ]
