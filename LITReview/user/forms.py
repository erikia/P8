from django.forms import ModelForm
from user.models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']