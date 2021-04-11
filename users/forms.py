from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CreationForm(UserCreationForm):
    """Is used to create form for registration of new user.

    Subclass of UserCreationForm

    Instance to User model.

    Create registration form with first name, last name, username,
    email, password and confirm password fields.
    """
    class Meta(UserCreationForm.Meta):
        model = User

        fields = ['first_name', 'last_name', 'username', 'email']
