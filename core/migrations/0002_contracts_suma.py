# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contracts',
            name='suma',
            field=models.DecimalField(default=1, verbose_name='Сума', decimal_places=2, max_digits=12),
            preserve_default=False,
        ),
    ]
