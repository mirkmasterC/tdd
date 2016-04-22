#This test suite functions as a part of the project unit tests.

from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from django.http import HttpResponse, HttpRequest
from django.template.loader import render_to_string
from lists.models import Item


class HomePageTest(TestCase):

	def test_root_url_resolves_to_homepage(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)

	def test_homepage_can_save_a_POST_request(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new item in the list'

		response = home_page(request)

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item in the list')

		self.assertIn('A new item in the list', response.content.decode())
		the_expected_html = render_to_string('home.html', {'new_item_text':'A new item in the list'})
		self.assertEqual(response.content.decode(), the_expected_html)

	def test_home_page_saves_items_only_when_necessary(self):
		request = HttpRequest()
		home_page(request)
		self.assertEqual(Item.objects.count(), 0)

class ItemModelTest(TestCase):

	def test_save_retrieve_items(self):
		#make one item
		first = Item()
		first.text = 'first item'
		first.save()

		#make a second item
		second = Item()
		second.text = 'second item'
		second.save()

		#get all of the items
		all_items = Item.objects.all()
		self.assertEqual(all_items.count(), 2)

		#retrieve first and second items
		first_item = all_items[0]
		second_item = all_items[1]
		self.assertEqual(first_item.text, 'first item')
		self.assertEqual(second_item.text, 'second item')






