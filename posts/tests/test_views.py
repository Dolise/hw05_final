from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django import forms

from datetime import datetime
import shutil
import tempfile

from ..models import Post, Group, Follow

import posts.tests.constants as const

User = get_user_model()


class PostsPagesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        cls.image = SimpleUploadedFile(
            name=const.POST_IMAGE_NAME,
            content=const.POST_IMAGE,
            content_type=const.POST_IMAGE_TYPE
        )
        cls.group = Group.objects.create(
            title=const.GROUP_TITLE,
            slug=const.GROUP_SLUG,
            description=const.GROUP_DESCRPTION
        )
        cls.user_owner = User.objects.create_user(
            username=const.USER_OWNER_USERNAME,
            first_name=const.USER_OWNER_FIRST_NAME,
            last_name=const.USER_OWNER_LAST_NAME
        )
        cls.authorized_client_owner = Client()
        cls.authorized_client_owner.force_login(cls.user_owner)
        cls.post = Post.objects.create(
            author=cls.user_owner,
            text=const.POST_TEXT,
            group=cls.group,
            image=cls.image
        )

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username=const.USER_NOT_OWNER_USERNAME
        )
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_name_uses_correct_template(self):
        template_pages_url = {
            'index.html': const.INDEX_URL,
            'group.html': const.GROUP_URL,
            'new_post.html': const.NEW_POST_URL,
        }
        for template, reverse_name in template_pages_url.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_new_post_and_edit_post_pages_show_correct_context(self):
        urls = [const.NEW_POST_URL,
                reverse(const.POST_EDIT_NAME,
                        kwargs={
                            'username': const.USER_OWNER_USERNAME,
                            'post_id': self.post.id
                        })]
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for url in urls:
            response = self.authorized_client_owner.get(url)
            for value, expected in form_fields.items():
                with self.subTest(value=value):
                    form_field = response.context['form'].fields[value]
                    self.assertIsInstance(form_field, expected)

    def test_index_page_show_correct_context(self):
        response = self.authorized_client.get(const.INDEX_URL)
        self.assertEqual(response.context['page'][0].author.get_full_name(),
                         'Ronald Weasley')
        self.assertEqual(response.context['page'][0].pub_date.date(),
                         datetime.now().date())
        self.assertEqual(response.context['page'][0].text,
                         'Just a text')
        self.assertEqual(response.context['page'][0].image.name,
                         'posts/image.gif')
        self.assertEqual(response.context['page'][0].group.title,
                         'Группа фанатов групп')
        self.assertEqual(response.context['page'][0].group.title,
                         'Группа фанатов групп')

    def test_group_page_show_correct_context(self):
        response = self.authorized_client.get(const.GROUP_URL)
        self.assertEqual(response.context['group'].title,
                         'Группа фанатов групп')
        self.assertEqual(response.context['group'].description,
                         'Это группа')
        self.assertEqual(response.context['group'].slug,
                         'gruppa')
        self.assertEqual(response.context['page'][0].author.get_full_name(),
                         'Ronald Weasley')
        self.assertEqual(response.context['page'][0].pub_date.date(),
                         datetime.now().date())
        self.assertEqual(response.context['page'][0].text,
                         'Just a text')
        self.assertEqual(response.context['page'][0].image.name,
                         'posts/image.gif')

    def test_pages_shows_new_post(self):
        urls = [
            const.INDEX_URL,
            const.GROUP_URL,
        ]
        for url in urls:
            with self.subTest():
                response = self.authorized_client.get(url)
                first_object = response.context['page'][0]
                post_text_0 = first_object.text
                post_pub_date_0 = first_object.pub_date.date()
                post_author_0 = first_object.author.get_full_name()
                post_group_0 = first_object.group.title
                self.assertEqual(post_text_0, 'Just a text')
                self.assertEqual(post_author_0, 'Ronald Weasley')
                self.assertEqual(post_pub_date_0, datetime.now().date())
                self.assertEqual(post_group_0, 'Группа фанатов групп')

    def test_profile_page_shows_correct_context(self):
        response = self.authorized_client_owner.get(
            const.PROFILE_URL)
        self.assertEqual(response.context['page'][0].author.get_full_name(),
                         'Ronald Weasley')
        self.assertEqual(response.context['page'][0].pub_date.date(),
                         datetime.now().date())
        self.assertEqual(response.context['page'][0].text,
                         'Just a text')
        self.assertEqual(response.context['page'][0].image.name,
                         'posts/image.gif')
        self.assertEqual(response.context['author'].get_full_name(),
                         'Ronald Weasley')
        self.assertEqual(response.context['author'].username,
                         'Owner')
        self.assertEqual(len(response.context['posts_list']),
                         1)

    def test_post_page_shows_correct_context(self):
        response = self.authorized_client_owner.get(
            reverse(const.POST_NAME,
                    kwargs={
                        'username': const.USER_OWNER_USERNAME,
                        'post_id': self.post.id}))
        self.assertEqual(response.context['post'].author.get_full_name(),
                         'Ronald Weasley')
        self.assertEqual(response.context['post'].pub_date.date(),
                         datetime.now().date())
        self.assertEqual(response.context['post'].text,
                         'Just a text')
        self.assertEqual(response.context['post'].image.name,
                         'posts/image.gif')
        self.assertEqual(response.context['author'].get_full_name(),
                         'Ronald Weasley')
        self.assertEqual(response.context['author'].username,
                         'Owner')
        self.assertEqual(len(response.context['posts_list']),
                         1)

    def test_cache_index_page(self):
        post = Post.objects.create(
            author=self.user,
            text=const.POST_TEXT)
        response = self.authorized_client.get(const.INDEX_URL)
        self.assertEqual(len(response.context['page']), Post.objects.count())
        post.delete()
        self.assertEqual(len(
            response.context['page']),
            Post.objects.count() + 1)
        cache.clear()
        response = self.authorized_client.get(const.INDEX_URL)
        self.assertEqual(len(response.context['page']), Post.objects.count())

    def test_authorized_can_follow_and_unfollow(self):
        self.authorized_client_owner.get(const.USER_NOT_OWNER_FOLLOW_URL)
        self.assertTrue(Follow.objects.filter(
            user=self.user_owner,
            author=self.user
        ).exists())
        self.authorized_client_owner.get(const.USER_NOT_OWNER_UNFOLLOW_URL)
        self.assertFalse(Follow.objects.filter(
            user=self.user_owner,
            author=self.user
        ).exists())

    def test_post_shows_when_followed(self):
        self.authorized_client.get(const.USER_OWNER_FOLLOW_URL)
        response = self.authorized_client.get(const.FOLLOW_INDEX_URL)
        self.assertEqual(response.context['page'][0].text, const.POST_TEXT)
        self.authorized_client.get(const.USER_OWNER_UNFOLLOW_URL)
        response = self.authorized_client.get(const.FOLLOW_INDEX_URL)
        self.assertEqual(len(response.context['page']), 0)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create_user(username=const.USER_OWNER_USERNAME)
        for post in range(1, 14):
            Post.objects.create(
                text='Text',
                author=user
            )

    def setUp(self) -> None:
        self.client = Client()

    def test_first_index_page_contains_ten_posts(self):
        response = self.client.get(const.INDEX_URL)
        self.assertEqual(len(response.context.get('page').object_list), 10)

    def test_second_index_page_contains_three_posts(self):
        response = self.client.get(const.INDEX_URL + '?page=2')
        self.assertEqual(len(response.context.get('page').object_list), 3)

    def test_first_profile_page_contains_ten_posts(self):
        response = self.client.get(const.PROFILE_URL)
        self.assertEqual(len(response.context.get('page').object_list), 10)

    def test_second_profile_page_contains_three_posts(self):
        response = self.client.get(const.PROFILE_URL
                                   + '?page=2')
        self.assertEqual(len(response.context.get('page').object_list), 3)
