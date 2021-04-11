from django.test import TestCase, Client
from django.urls import reverse


class StaticViewsTest(TestCase):
    def setUp(self) -> None:
        self.user = Client()

    def test_pages_available_by_name(self):
        url_names = ['author', 'tech']
        for name in url_names:
            with self.subTest():
                response = self.user.get(reverse(f'about:{name}'))
                self.assertEqual(response.status_code, 200)

    def test_pages_uses_correct_templates(self):
        template_reverse = {
            'about/author.html': 'author',
            'about/tech.html': 'tech',
        }
        for template, name in template_reverse.items():
            with self.subTest():
                response = self.user.get(reverse(f'about:{name}'))
                self.assertTemplateUsed(response, template)
