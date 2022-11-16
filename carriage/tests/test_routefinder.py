from django.test import TestCase
from carriage.models import City, CustTerritory, Coefficient, Country, Distance
from . import source_test
from carriage.routefinder import get_graph, shortest
from ..forms import RouteFindForm


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
        self.graph = get_graph()
        self.assertEqual(len(City.objects.all()), len(self.graph))

    def test_main_request_form_validation(self):
        self.lyon = City.objects.get(pk=9)
        data = {'from_city': self.lyon.name, 'to_city': self.lyon.name, 'selection': 1}
        form = RouteFindForm(data=data)
        self.assertFalse(form.is_valid())

        response = self.client.post('/carriage/', data)
        self.assertContains(response, "Cities of departure and destination must be different", 1, 200)




