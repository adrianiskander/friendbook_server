import string
from django import forms


USERNAME_CHARS = f'{ string.ascii_letters }{ string.digits }_'


class AuthForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        min_length=8,
        max_length=128,
        widget=forms.PasswordInput
    )


class EmailForm(forms.Form):
    email = forms.EmailField()


class PasswordForm(forms.Form):
    password = forms.CharField(
        min_length=8,
        max_length=128,
        widget=forms.PasswordInput
    )


class UserUpdateForm(forms.Form):

    email = forms.EmailField()
    username = forms.CharField(
        min_length=3,
        max_length=32
    )
    firstName = forms.CharField(max_length=30, required=False)
    lastName = forms.CharField(max_length=150, required=False)

    def clean_username(self):

        username = self.cleaned_data['username']

        if username.count('_') > 1:
            raise forms.ValidationError(
                (f"Username must contain no more than one character: '_'"),
                code='Too much characters',
                params={'character': '_'})

        for char in username:
            if char not in USERNAME_CHARS:
                raise forms.ValidationError(
                    (f"Username can't contain character: {char}"),
                    code='Invalid character',
                    params={'character': char})

        return username.lower()
