from django import forms
from posts.models import Post, Comment


class PostForm(forms.ModelForm):
    """Is used to create form for adding new post.

    Subclass of forms.ModelForm

    Instance to Post model.

    Create new Post form with text and group fields.
    """
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')


class CommentForm(forms.ModelForm):
    """Is used to create form of adding comment.

    Subclass of form.ModelForm

    Instance of Comment model

    Create new comment form with text field."""
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
            }),
        }
