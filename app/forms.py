from django import forms
from .models import Review, User
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('name', 'text', 'mark', 'product')


class ReviewFormset(ReviewForm):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(ReviewFormset, self).__init__(**kwargs)

    class Meta:
        model = Review
        fields = ('name', 'text', 'mark',)
        widgets = {
            'mark': forms.RadioSelect,
            'product': forms.HiddenInput
        }
        labels = {'name': 'Имя', 'text': 'Содержание', 'mark': ''}


class CustomUserCreationForm(UserCreationForm):

    email = forms.CharField(
        label=("Почтовый адрес"),
        widget=forms.EmailInput,
        strip=False,
    )

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = "Пароль"
        self.fields['password2'].label = "Подтверждение пароля"

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class CustomUserAuthenticationForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField()

    class Meta:
        model = User
        fields = ('email', 'password',)






