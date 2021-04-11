from django.test import TestCase, Client, override_settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

import shutil
import tempfile

from ..forms import PostForm, CommentForm
from ..models import Post, Comment

import posts.tests.constants as const

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateForm(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = PostForm()
        cls.user = User.objects.create_user(
            username=const.USER_NOT_OWNER_USERNAME
        )
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.image = SimpleUploadedFile(
            name=const.POST_IMAGE_NAME,
            content=const.POST_IMAGE,
            content_type=const.POST_IMAGE_TYPE
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_create_post(self):
        post_count = Post.objects.count()
        form_data = {
            'text': const.POST_TEXT,
            'image': self.image
        }
        response = self.authorized_client.post(const.NEW_POST_URL,
                                               data=form_data, follow=True)
        self.assertRedirects(response, const.INDEX_URL)
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(Post.objects.filter(
            text=const.POST_TEXT,
            author=self.user,
            image='posts/' + const.POST_IMAGE_NAME
        ).exists())

    def test_edit_post(self):
        post = Post.objects.create(
            text=const.POST_TEXT,
            author=self.user
        )
        edit_data = {
            'text': const.POST_EDITED_TEXT
        }
        reverse_args = {'username': const.USER_NOT_OWNER_USERNAME,
                        'post_id': post.id}
        response_edit = self.authorized_client.post(
            reverse(const.POST_EDIT_NAME, kwargs=reverse_args),
            data=edit_data,
            follow=True)
        self.assertRedirects(response_edit, reverse(const.POST_NAME,
                                                    kwargs=reverse_args))
        self.assertTrue(Post.objects.filter(
            text=const.POST_EDITED_TEXT,
            author=self.user
        ).exists())


class CommentAddForm(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = CommentForm()
        cls.user = User.objects.create_user(
            username=const.USER_OWNER_USERNAME
        )
        cls.post = Post.objects.create(
            text=const.POST_TEXT,
            author=cls.user
        )
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.anonymous_client = Client()

    def test_authorized_can_add_comment(self):
        comment_count = Comment.objects.count()
        comment_data = {
            'text': const.POST_COMMENT_TEXT
        }

        self.authorized_client.post(
            reverse(const.POST_COMMENT_NAME,
                    kwargs={
                        'username': self.user,
                        'post_id': self.post.id
                    }),
            data=comment_data,
            follow=True
        )
        self.assertEqual(Comment.objects.count(), comment_count + 1)

    def test_anonymous_cant_add_comment(self):
        comment_data = {
            'text': const.POST_COMMENT_TEXT
        }

        response = self.anonymous_client.post(
            reverse(const.POST_COMMENT_NAME,
                    kwargs={
                        'username': self.user,
                        'post_id': self.post.id
                    }),
            data=comment_data,
            follow=True
        )
        self.assertRedirects(response,
                             reverse('login') + '?next=/Owner/1/comment/')
