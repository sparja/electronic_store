from django.db import models

NULLABLE = {'null': True, 'blank': True}


class NetworkEntity(models.Model):
    ''' Модель сети '''
    LEVEL_ZERO = 0
    LEVEL_FIRST = 1
    LEVEL_SECOND = 2

    LEVEL = [
        (LEVEL_ZERO, 'Завод'),
        (LEVEL_FIRST, 'Розничная сеть'),
        (LEVEL_SECOND, 'Индивидуальный предприниматель'),
    ]

    name = models.CharField(max_length=100, verbose_name='Название')
    email = models.EmailField(verbose_name='Почта', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='Страна', **NULLABLE)
    city = models.CharField(max_length=50, verbose_name='Город', **NULLABLE)
    street = models.CharField(max_length=50, verbose_name='Улица', **NULLABLE)
    house_number = models.CharField(max_length=20, verbose_name='Номер дома ', **NULLABLE)
    level = models.IntegerField(choices=LEVEL, verbose_name='Уровень сети')
    parent_entity = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Поставщик', **NULLABLE)
    debt = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, verbose_name='Задолжность')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Звено сети'
        verbose_name_plural = 'Звенья сети'
        constraints = [
            models.CheckConstraint(check=~models.Q(parent_entity=models.F('pk')), name='no_self_reference'),
        ]  # проверка на создание циклических зависимостей


class Product(models.Model):
    ''' Модель продуктов '''
    name = models.CharField(max_length=30, verbose_name='Название')
    model = models.CharField(max_length=30, verbose_name='Модель')
    release_date = models.DateField(verbose_name='Дата релиза продукта')
    supplier = models.ForeignKey(NetworkEntity, on_delete=models.CASCADE, verbose_name='Поставщик')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
