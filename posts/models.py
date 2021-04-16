from django.db import models
from django.contrib.auth import get_user_model

import textwrap

User = get_user_model()


class Post(models.Model):
    """Is used to add model of post in database.

    Subclass of models.Model

    Attributes:
    text - text of post
    pub_date - date of publication
    author - author of post
    group - which group post belongs to
    """
    text = models.TextField('Текст', help_text='Введите текст')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True,)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='posts',
                               verbose_name='Автор')
    group = models.ForeignKey('Group',
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True,
                              verbose_name='Группа',
                              help_text='Выберите группу')
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    def __str__(self) -> str:
        author = self.author
        text = textwrap.wrap(self.text, width=30)[0]
        pub_date = self.pub_date
        return f'Author: {author}, Post: {text}, Pub date: {pub_date.date()}'

    class Meta:
        db_table = 'Posts'
        ordering = ('-pub_date', )


class Group(models.Model):
    """Is used to add model of group in database.

    Subclass of models.Model

    Attributes:
    title - title of group
    slug - link to group
    description - something about group
    """
    title = models.CharField('Заголовок',
                             max_length=200,
                             help_text='Введите название группы')
    slug = models.SlugField('Ссылка',
                            max_length=10,
                            unique=True,
                            help_text='Придумайте ссылку')
    description = models.TextField('Описание',
                                   help_text='Введите описание группы')

    def __str__(self) -> str:
        return f'{self.title}'

    class Meta:
        db_table = 'Groups'


class Comment(models.Model):
    """Is used to add model of comment in db.

    Subclass of models.Model

    Attributes:
    post - post instance
    author - user instance
    text - text of comment
    created - date of creation
    """
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Пост'

    )
    author = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата создания')

    def __str__(self):
        text = textwrap.wrap(self.text, width=30)[0]
        author = self.author
        return f'Автор: {author}, Текст: {text}'

    class Meta:
        db_table = 'Comments'
        ordering = ('-created', )


class Follow(models.Model):
    """Is used to add model of following on author in db.

    Subclass of models.Model

    Attributes:
    user - user instance (who follows)
    author - user instance (on whom follows)
    """
    user = models.ForeignKey(User,
                             related_name='follower',
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь'
                             )
    author = models.ForeignKey(User,
                               related_name='following',
                               on_delete=models.CASCADE,
                               verbose_name='Автор'
                               )

    def __str__(self):
        return f'{self.user} подписался на {self.author}'

    class Meta:
        db_table = 'Follow'
