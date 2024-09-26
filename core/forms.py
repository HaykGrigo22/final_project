from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailForm(forms.Form):

    subject = forms.CharField(max_length=55)
    content = forms.CharField()
    to_email = forms.CharField()


class UserRegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True

    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'image']
