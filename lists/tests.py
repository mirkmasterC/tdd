#This test suite functions as a part of the project unit tests.

from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from django.http import HttpResponse, HttpRequest
from django.template.loader import render_to_string
from lists.models import Item, List


class HomePageTest(TestCase):

	def test_root_url_resolves_to_homepage(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)


class ListAndItemModelsTest(TestCase):

	def test_saving_retrieving_items(self):
		list_ = List()
		list_.save()

		#make one item
		first = Item()
		first.text = 'first item'
		first.list = list_
		first.save()

		#make a second item
		second = Item()
		second.text = 'second item'
		second.list = list_
		second.save()

		saved_list = List.objects.first()
		self.assertEquals(saved_list, list_)

		#get all of the items
		all_items = Item.objects.all()
		self.assertEqual(all_items.count(), 2)

		#retrieve first and second items
		first_item = all_items[0]
		second_item = all_items[1]
		self.assertEqual(first_item.text, 'first item')
		self.assertEqual(first_item.list, list_)
		self.assertEqual(second_item.text, 'second item')
		self.assertEqual(first_item.list, list_)

class ListViewTest(TestCase):

	def test_uses_list_template(self):
		list_ = List.objects.create()
		response = self.client.get('/lists/%d/' % (list_.id,))
		self.assertTemplateUsed(response, 'list.html')

	def test_displays_only_items_items_for_that_list(self):
		correct_list = List.objects.create()
		Item.objects.create(text='itemey 1', list=correct_list)
		Item.objects.create(text='itemey 2', list=correct_list)
		other_list = List.objects.create()
		Item.objects.create(text='other list item 1', list=other_list)
		Item.objects.create(text='other list item 2', list=other_list)
		response = self.client.get('/lists/%d/' % (correct_list.id,))

		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')
		self.assertNotContains(response, 'other list item 1')
		self.assertNotContains(response, 'other list item 2')

	def test_passes_correct_list_to_template(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		response = self.client.get('/lists/%d/' % (correct_list.id,))
		self.assertEqual(response.context['list'], correct_list)

class NewListTest(TestCase):

	def test_saving_a_POST_request(self):
		self.client.post('/lists/new', data={'item_text': "A new item in the list"})
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item in the list')

	def test_redirects_after_POST(self):
		response = self.client.post('/lists/new', data={'item_text': "A new item in the list"})
		new_list = List.objects.first()
		self.assertRedirects(response, '/lists/%d/' % (new_list.id,))


class NewItemTest(TestCase):

	def test_can_save_a_POST_request_to_an_existing_list(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		self.client.post('/lists/%d/add_item' % (correct_list.id,), data={'item_text': 'A new item for an existing list'})
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item for an existing list')
		self.assertEqual(new_item.list, correct_list)

	def test_redirects_to_list_view(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		response = self.client.post('/lists/%d/add_item' % (correct_list.id), data={'item_text':'A new item for an existing list'})
		self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))
































