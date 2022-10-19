from django.db import models

class Test(models.Model):
    """ This is test description"""
    image = models.ImageField(upload_to='img/')


class CustTerritory(models.Model):
    cust_territory = models.CharField(max_length=5, verbose_name='Customs territory',
                                      null=False, primary_key=True, unique=True)
    territory_name = models.CharField(max_length=50, unique=True,
                                      verbose_name='Customs territory name', null=False)

    class Meta:
        verbose_name='Customs territory'
        verbose_name_plural = 'Customs territories'

    def __str__(self):
        return str(self.territory_name)


class Country(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Country', null=False)
    cust_territory = models.ForeignKey(CustTerritory, on_delete=models.CASCADE, related_name='cust_terr')
    flag_large = models.ImageField(upload_to='img/flaglarge')
    flag_small = models.ImageField(upload_to='img/flagsmall')

    class Meta:
        verbose_name='Country'
        verbose_name_plural='Countries'
        ordering = ['name']

    def __str__(self):
        return str(self.name)


class City(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='City', null=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='country' )
    airport = models.BooleanField(default=False, verbose_name='Airport')
    seaport = models.BooleanField(default=False, verbose_name='Seaport')
    warehouse = models.CharField(max_length=10, choices=[('CUST', 'CUSTOMS WAREHOUSE'), ('USUAL','USUAL WAREHOUSE')],
                                 blank=True, verbose_name='Consolidation warehouse')

    class Meta:
        verbose_name='City'
        verbose_name_plural='Cities'
        ordering = ['name']

    def __str__(self):
        return str(self.name)


class Coefficient(models.Model):
    coeff_code = models.CharField(max_length=5, verbose_name='Coefficient', null=False, primary_key=True, unique=True)
    coeff_value = models.FloatField(null=False, verbose_name='Coefficient value')
    coeff_name = models.CharField(max_length=50, verbose_name='Coefficient name', null=False)
    coeff_type = models.CharField(max_length=2, choices=[('r', 'ROAD ROUTE'), ('s', 'SEA ROUTE'), ('rl', 'RAIL ROUTE'),
                                                         ('a', 'AVIA ROUTE')], verbose_name='Transport type')

    class Meta:
        verbose_name = 'Coefficient'
        verbose_name_plural = 'Coefficients'

    def __str__(self):
        return str(f'{self.coeff_value} for {self.coeff_name}')


class Distance(models.Model):
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='start',
                                  verbose_name='City of departure')
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='finish',
                                verbose_name='City of destination')
    coeff = models.ForeignKey(Coefficient, on_delete=models.CASCADE)
    distance = models.IntegerField(null=False, verbose_name='Distance between cities')

    class Meta:
        verbose_name = 'Distance'
        verbose_name_plural = 'Distancies'
        unique_together = ['from_city', 'to_city', 'coeff']

    def __str__(self):
        return str(f'from {self.from_city} to {self.to_city}')


class BorderCrossing(models.Model):
    from_cust_territory = models.ForeignKey(CustTerritory, on_delete=models.CASCADE,
                                            related_name='territory_of_departure',
                                            verbose_name='Customs territory of departure')
    to_cust_territory = models.ForeignKey(CustTerritory, on_delete=models.CASCADE,
                                            related_name='territory_of_destination',
                                            verbose_name='Customs territory of destination')
    approx_time = models.IntegerField(null=False, verbose_name='Approximated time to cross the border')
    add_price = models.IntegerField(null=False, verbose_name='Costs for border-crossing', default=1)


class SiteContentData(models.Model):
    short_descr = models.CharField(max_length=20, verbose_name='Title description',
                                      null=False)
    main_content = models.TextField(verbose_name='content')
    site_image = models.ImageField(upload_to='img/sitecontent')
    class Meta:
        verbose_name = 'Site content'
        verbose_name_plural = 'Site content'



class News(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    body = models.TextField(verbose_name='News content')
    news_image = models.ImageField(upload_to='img/news')
    date_of_news = models.DateField(verbose_name='Date', default='2022-01-01')
    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'




list_of_models = [CustTerritory, Country, City, Coefficient, Distance, BorderCrossing, SiteContentData, News]