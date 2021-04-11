from django.test import Client, TestCase
from django.contrib.auth import get_user_model

from ..models import Post, Group

User = get_user_model()


class StaticUrlTest(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_homepage(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Группа фанатов групп',
            slug='gruppa',
            description='Это группа'
        )
        cls.user_owner = User.objects.create_user(username='Bob')
        cls.authorized_client_owner = Client()
        cls.authorized_client_owner.force_login(cls.user_owner)
        cls.post = Post.objects.create(
            author=cls.user_owner,
            text='Just a text',
            group=cls.group
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='Jakson')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.urls_common = ['/', '/group/gruppa/', f'/{self.user.username}/',
                            f'/{self.user.username}/{self.post.id}/']
        self.urls_authorized = {
            '/new/': '/auth/login/?next=/new/',
            f'/{self.user_owner.username}/{self.post.id}/edit/':
            f'/auth/login/?next=/{self.user_owner.username}/'
            f'{self.post.id}/edit/'
        }

    def test_url_exists_at_desired_location(self):
        for url in self.urls_common:
            with self.subTest():
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_url_exists_for_authorized(self):
        for url in self.urls_authorized.keys():
            with self.subTest():
                response = self.authorized_client_owner.get(url)
                self.assertEqual(response.status_code, 200)

    def test_url_redirect_for_anonymous(self):
        for url, redirect in self.urls_authorized.items():
            with self.subTest():
                response = self.guest_client.get(url, follow=True)
                self.assertRedirects(response, redirect)

    def test_urls_use_correct_template(self):
        template_url_names = {
            'index.html': '/',
            'group.html': '/group/gruppa/',
            'new_post.html': [
                '/new/',
                f'/{self.user_owner.username}/{self.post.id}/edit/'
            ],

        }
        for template, urls in template_url_names.items():
            with self.subTest():
                if isinstance(urls, list):
                    for url in urls:
                        response = self.authorized_client_owner.get(url)
                        self.assertTemplateUsed(response, template)
                else:
                    response = self.authorized_client_owner.get(urls)
                    self.assertTemplateUsed(response, template)

    def test_owner_can_edit(self):
        user_client = self.authorized_client_owner
        user_model = self.user_owner
        post = self.post
        response = user_client.get(f'/{user_model.username}/{post.id}/edit/')
        self.assertEqual(response.status_code, 200)

    def test_not_owner_post_edit_redirect(self):
        user_not_owner = self.authorized_client
        user_owner_model = self.user_owner
        post = self.post
        response = user_not_owner.get(f'/{user_owner_model.username}/'
                                      f'{post.id}/edit/')
        self.assertRedirects(response,
                             f'/{user_owner_model.username}/{post.id}/')


class ErrorTest(TestCase):
    def setUp(self) -> None:
        self.user = Client()

    def test_404_exist(self):
        response = self.user.get('/this/page/doesnt/exist')
        self.assertEqual(response.status_code, 404)
