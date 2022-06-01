from django.test import TestCase, SimpleTestCase
from product.sample_file_for_test import calc
#from product import views

# class ViewsTest(SimpleTestCase):
#     def test_make_list_unique(self):
#         sample_items = [1, 1, 2, 3, 3, 3, 5, 4, 5]
#
#         res = views.remove_duplicate(sample_items)
#         self.assertEqual(res, [1, 2, 3, 5, 4])


class ClacTests(SimpleTestCase):
    def test_add_numbers(self):
        res = calc(10, -5)
        self.assertEqual(res, 5)