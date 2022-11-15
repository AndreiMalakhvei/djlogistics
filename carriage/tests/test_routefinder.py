from django.test import TestCase
from carriage.models import City, CustTerritory, Coefficient, Country, Distance
from . import source_test
from carriage.routefinder import get_graph, shortest

class DbDependentViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        ct = source_test.source_maker(CustTerritory, source_test.list_custterritory)
        CustTerritory.objects.bulk_create(ct)
        cntr = source_test.source_maker(Country, source_test.list_country)
        Country.objects.bulk_create(cntr)
        cf = source_test.source_maker(Coefficient, source_test.list_coefficient)
        Coefficient.objects.bulk_create(cf)
        th = source_test.source_maker(City, source_test.list_city)
        City.objects.bulk_create(th)
        ds = source_test.source_maker(Distance, source_test.list_distance)
        Distance.objects.bulk_create(ds)


    def test_graph_creation(self):
        # self.graph = get_graph()
        self.assertEqual(3, len(CustTerritory.objects.all()))

    def test_automatic_creation(self):
        s = City.objects.all()
        print(len(s))



