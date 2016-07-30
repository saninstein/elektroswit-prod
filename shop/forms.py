from django.forms import ValidationError, PasswordInput,EmailField, CharField, ModelForm, TextInput, Textarea, EmailInput, HiddenInput, NumberInput
from shop.models import Order
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    email = EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')



    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise ValueError('Такой адрес уже зарегистрирован')

    def save(self, commit=True):
        user = sum(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.is_active = False
            user.save()
        return user


class OrderForm(ModelForm):
    class Meta:
        model = Order
        exclude = ['items', 'link_client']
        widgets = {
            'email': EmailInput(attrs={
                'placeholder': 'Введите адрес',
                'class': 'new-cont-textinput',
            }),
            'phone': NumberInput(attrs={
                'placeholder': 'Введите номер',
                'class': 'new-cont-textinput',
            }),
            'message': Textarea(attrs={
                'placeholder': 'Текст сообщения',
                'class': 'new-cont-textarea',
            }),
        }
