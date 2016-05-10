# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_contracts_suma'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credits',
            name='all_sum',
            field=models.DecimalField(decimal_places=2, unique_for_month=models.DateField(verbose_name='Дата визначення суми'), max_digits=12, verbose_name='Вся сума'),
        ),
    ]
