from django.db import models


# Create your models here.
class SWOT(models.Model):
    Strengths = 'S'
    Weaknesses = 'W'
    Opportunities = 'O'
    Threats = 'T'
    SWOT_TYPE_CHOICES = (
        (Strengths, 'Strengths'),
        (Weaknesses, 'Weaknesses'),
        (Opportunities, 'Opportunities'),
        (Threats, 'Threats'),
    )

    class Meta:
        verbose_name = 'SWOT'
        verbose_name_plural = 'SWOT analysis'

    swot_attr = models.CharField(
        verbose_name='Swot attribute',
        max_length=100
    )
    swot_type = models.CharField(
        choices=SWOT_TYPE_CHOICES,
        max_length=20
    )

    def __str__(self):
        return '{0} {1}'.format(self.swot_attr, self.swot_type)


class Valuta(models.Model):
    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюти'

    name = models.CharField(
        verbose_name='Назва валюти',
        max_length=30
    )
    sign = models.CharField(
        verbose_name='Умовне позначення',
        max_length=5
    )

    def __str__(self):
        return '{0} {1}'.format(self.name, self.sign)


class Credits(models.Model):
    class Meta:
        verbose_name_plural = 'Суми в кредитному портфелі'
        verbose_name = 'Сума в кредитному портфелі'

    date_credit = models.DateField(
        verbose_name='Дата визначення суми'
    )
    all_sum = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Вся сума'
    )

    def __str__(self):
        return '{0} {1}'.format(self.date_credit, self.all_sum)


class Deposits(models.Model):
    K = 3
    KK = 6
    D = 12
    DURATION_CHOICES = (
        (K, 'Короткостроково, 3 місяці'),
        (KK, 'Короткостроково, 6 місяців'),
        (D, 'Довгостроково, 12 місяців'),
    )

    class Meta:
        verbose_name = 'Депозитна програма'
        verbose_name_plural = 'Депозитні програми'

    id_valuta = models.ForeignKey(
        Valuta,
        verbose_name='Валюта'
    )
    name = models.CharField(
        verbose_name='Назва депозиту',
        max_length=40
    )
    percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Відсоткова ставка'
    )
    duration = models.IntegerField(
        verbose_name='Тривалість',
        choices=DURATION_CHOICES
    )

    def __str__(self):
        return '{0} {1}'.format(self.name, self.percent)


class Client(models.Model):
    LP = 'юридична особа'
    FP = 'фізична особа'
    BANK = 'банк'
    CLIENT_TYPE_CHOICES = (
        (LP, 'юридична особа'),
        (FP, 'фізична особа'),
        (BANK, 'банк'),
    )

    class Meta:
        verbose_name = 'Клієнт'
        verbose_name_plural = 'Клієнти'

    name = models.CharField(
        verbose_name='''Ім’я клієнта''',
        max_length=50
    )
    type_cl = models.CharField(
        verbose_name='Тип клієнта',
        choices=CLIENT_TYPE_CHOICES,
        max_length=30
    )

    def __str__(self):
        return '{0} {1}'.format(self.name, self.type_cl)


class Contracts(models.Model):
    class Meta:
        verbose_name = 'Укладений договір'
        verbose_name_plural = 'Укладені договори'

    id_deposits = models.ForeignKey(
        Deposits,
        verbose_name='Депозит'
    )
    id_client = models.ForeignKey(
        Client,
        verbose_name='Клієнт'
    )
    datestart = models.DateField(
        verbose_name='Дата укладення договору'
    )
    suma = models.DecimalField(
        verbose_name='Сума',
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return 'З {0} від {1}'.format(self.id_client, self.datestart)


class Reports(models.Model):
    class Meta:
        verbose_name = 'Звіт'
        verbose_name_plural = 'Звіти'

    id_contracts = models.ForeignKey(
        Contracts,
        verbose_name='Договір',
        blank=True,
        null=True
    )
    id_client = models.ForeignKey(
        Client,
        verbose_name='Клієнт',
        blank=True,
        null=True
    )
    id_credits = models.ForeignKey(
        Credits,
        verbose_name='Сума кредиту',
        blank=True,
        null=True
    )
    name = models.CharField(
        verbose_name='Назва',
        max_length=30
    )
    document = models.CharField(
        verbose_name='Документ',
        max_length=150
    )

    def __str__(self):
        return '{0} {1}'.format(self.name, self.id)
