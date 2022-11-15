from django.test import TestCase, client
from django.urls import reverse

from carriage import views


class SimpleViewTestCase(TestCase):

    def test_start_correct_view_and_template(self):
        response = self.client.get(reverse('start'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='carriage/index.html')
        self.assertEqual(response.resolver_match.func, views.start_page)

    def test_carriage_main_correct_view_and_template(self):
        response = self.client.get(reverse('carriage:carriage_main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='carriage/carriage_main.html')
        self.assertEqual(response.resolver_match.func, views.carriage_main)

    def test_contact_correct_view_and_template(self):
        response = self.client.get(reverse('carriage:contacts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='carriage/contact.html')
        self.assertEqual(response.resolver_match.func, views.contacts)

    def test_contact_result_correct_view_and_template(self):
        response = self.client.get(reverse('carriage:contacts_result'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='carriage/contacts_result.html')
        self.assertEqual(response.resolver_match.func, views.contacts_result)

    def test_warehouse_correct_view_and_template(self):
        response = self.client.get(reverse('carriage:warehouse'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='carriage/warehouse.html')
        self.assertEqual(response.resolver_match.func, views.warehouse)

    def test_search_correct_view_and_template(self):
        response = self.client.get(reverse('carriage:search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='carriage/search.html')
        self.assertEqual(response.resolver_match.func, views.search)

    # def test_warehouse_detail_correct_view_and_template(self):
    #     response = self.client.get(reverse('carriage:warehouse_detail'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, template_name='carriage/warehouse_detail.html')
    #     self.assertEqual(response.resolver_match.func, views.warehouse_detail)


# class DbDependentViewTestCase(TestCase):
#     @classmethod
#     def setUpTestData(cls):

