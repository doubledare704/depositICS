# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20160510_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credits',
            name='all_sum',
            field=models.DecimalField(max_digits=12, decimal_places=2, unique_for_month='date_credit', verbose_name='Вся сума'),
        ),
    ]
