from django.urls import reverse

# index
INDEX_URL = reverse('index')
INDEX_CACHE_TIME = 20

# group
GROUP_TITLE = 'Группа фанатов групп'
GROUP_SLUG = 'gruppa'
GROUP_DESCRPTION = 'Это группа'
GROUP_URL = reverse('group',
                    kwargs={
                        'slug': GROUP_SLUG,
                    })

GROUP_VERBOSE_TITLE = 'Заголовок'
GROUP_VERBOSE_SLUG = 'Ссылка'
GROUP_VERBOSE_DESCRIPTION = 'Описание'

GROUP_HELP_TITLE = 'Введите название группы'
GROUP_HELP_SLUG = 'Придумайте ссылку'
GROUP_HELP_DESCRIPTION = 'Введите описание группы'

# Follow urls
FOLLOW_NAME = 'profile_follow'
UNFOLLOW_NAME = 'profile_unfollow'
FOLLOW_INDEX_NAME = 'follow_index'
FOLLOW_INDEX_URL = reverse(FOLLOW_INDEX_NAME)

# User owner
USER_OWNER_USERNAME = 'Owner'
USER_OWNER_FIRST_NAME = 'Ronald'
USER_OWNER_LAST_NAME = 'Weasley'
USER_OWNER_FOLLOW_URL = reverse(
    FOLLOW_NAME,
    kwargs={
        'username': USER_OWNER_USERNAME
    }
)
USER_OWNER_UNFOLLOW_URL = reverse(
    UNFOLLOW_NAME,
    kwargs={
        'username': USER_OWNER_USERNAME
    }
)

# User not owner
USER_NOT_OWNER_USERNAME = 'Harry'
USER_NOT_OWNER_FOLLOW_URL = reverse(
    FOLLOW_NAME,
    kwargs={
        'username': USER_NOT_OWNER_USERNAME
    }
)
USER_NOT_OWNER_UNFOLLOW_URL = reverse(
    UNFOLLOW_NAME,
    kwargs={
        'username': USER_NOT_OWNER_USERNAME
    }
)

# Post
POST_NAME = 'post'
POST_TEXT = 'Just a text'
POST_IMAGE = (
    b'\x47\x49\x46\x38\x39\x61\x02\x00'
    b'\x01\x00\x80\x00\x00\x00\x00\x00'
    b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
    b'\x00\x00\x00\x2C\x00\x00\x00\x00'
    b'\x02\x00\x01\x00\x00\x02\x02\x0C'
    b'\x0A\x00\x3B'
)
POST_IMAGE_NAME = 'image.gif'
POST_IMAGE_TYPE = 'image/gif'
POST_EDITED_TEXT = 'Test post edited'


POST_VERBOSE_TEXT = 'Текст'
POST_VERBOSE_PUB_DATE = 'Дата публикации'
POST_VERBOSE_AUTHOR = 'Автор'
POST_VERBOSE_GROUP = 'Группа'

POST_HELP_TEXT = 'Введите текст'
POST_HELP_GROUP = 'Выберите группу'

# New post form
NEW_POST_NAME = 'new_post'
NEW_POST_URL = reverse(NEW_POST_NAME)

# Post edit form
POST_EDIT_NAME = 'post_edit'

# Post comment
POST_COMMENT_NAME = 'add_comment'
POST_COMMENT_TEXT = 'Comment'

# User profile
PROFILE_NAME = 'profile'
PROFILE_URL = reverse(PROFILE_NAME,
                      kwargs={
                          'username': USER_OWNER_USERNAME,
                      })
