from django.test import TestCase
from posts.models import Post, Group, User

from datetime import datetime

import posts.tests.constants as const


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create()
        group = Group.objects.create()
        cls.post = Post.objects.create(
            text=const.POST_TEXT,
            author=user,
            group=group
        )

    def test_verbose_name(self):
        post = self.post
        field_verbose = {
            'text': const.POST_VERBOSE_TEXT,
            'pub_date': const.POST_VERBOSE_PUB_DATE,
            'author': const.POST_VERBOSE_AUTHOR,
            'group': const.POST_VERBOSE_GROUP,
        }
        for value, expected in field_verbose.items():
            with self.subTest(value=value):
                self.assertEqual(post._meta.get_field(value).verbose_name,
                                 expected)

    def test_help_text(self):
        post = self.post
        field_help_text = {
            'text': const.POST_HELP_TEXT,
            'group': const.POST_HELP_GROUP,
        }
        for value, expected in field_help_text.items():
            with self.subTest(value=value):
                self.assertEqual(post._meta.get_field(value).help_text,
                                 expected)

    def test_str(self):
        post = self.post
        value = post.__str__()
        expected = (f'Author: , Post: {const.POST_TEXT}, '
                    f'Pub date: {datetime.now().date()}')
        self.assertEqual(value, expected)


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title=const.GROUP_TITLE,
            slug=const.GROUP_SLUG,
            description=const.GROUP_DESCRPTION
        )

    def test_verbose_name(self):
        group = self.group
        field_verbose = {
            'title': const.GROUP_VERBOSE_TITLE,
            'slug': const.GROUP_VERBOSE_SLUG,
            'description': const.GROUP_VERBOSE_DESCRIPTION,
        }
        for value, expected in field_verbose.items():
            with self.subTest(value=value):
                self.assertEqual(group._meta.get_field(value).verbose_name,
                                 expected)

    def test_help_text(self):
        group = self.group
        field_help_text = {
            'title': const.GROUP_HELP_TITLE,
            'slug': const.GROUP_HELP_SLUG,
            'description': const.GROUP_HELP_DESCRIPTION,
        }
        for value, expected in field_help_text.items():
            with self.subTest(value=value):
                self.assertEqual(group._meta.get_field(value).help_text,
                                 expected)

    def test_str(self):
        group = self.group
        value = group.__str__()
        expected = const.GROUP_TITLE
        self.assertEqual(value, expected)
