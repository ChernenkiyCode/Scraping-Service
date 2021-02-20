from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

from scraping.models import City, Language

User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label='Email',
                             required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Password',
                               required=True)

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        usr = User.objects.get(email=email)

        if not usr:
            raise forms.ValidationError('User does not exist.')
        if not check_password(password, usr.password):
            raise forms.ValidationError('Invalid password')
        user = authenticate(email=email, password=password)
        if not user:
            raise forms.ValidationError('This account was disabled.')

        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label='Email',
                             required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Password',
                               required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                label='Password confirmation', required=True)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise forms.ValidationError('Password does not match')
        return self.cleaned_data['password2']


class UserUpdateForm(forms.ModelForm):
    city = forms.ModelChoiceField(queryset=City.objects.all(), to_field_name='slug', required=True,
                                  widget=forms.Select(attrs={'class': 'form-control'}), label='Город')
    language = forms.ModelChoiceField(queryset=Language.objects.all(), to_field_name='slug', required=True,
                                      widget=forms.Select(attrs={'class': 'form-control'}), label='Специальность')
    send_emails = forms.BooleanField(widget=forms.CheckboxInput, label='Let the service send emails?')

    class Meta:
        model = User
        fields = ('city', 'language', 'send_emails')


class ContactForm(forms.Form):
    city = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}),
                           label='Город', max_length=80)
    language = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}),
                               label='Специность', max_length=100)
    message = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}),
                              label='Дополнительно')
