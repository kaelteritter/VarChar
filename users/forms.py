from django import forms
from django.contrib.auth import authenticate, get_user_model


User = get_user_model()

class SignUpForm(forms.ModelForm):
    error_messages = {
        'no_password_confirmation': 'Пожалуйста подтвердите пароль',
        'password_mismatch': 'Пароли не совпадают',
    }

    password1 = forms.CharField(
        widget=forms.PasswordInput, 
        label='Пароль',
        strip=False,
        help_text='Пароль должен состоять из латинских символов, цифр или знаков @/./+/-/_'
        )
    password2 = forms.CharField(
        widget=forms.PasswordInput, 
        label='Повторите пароль',
        strip=False,
        )
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        labels = {
            'username': 'Имя',
        }
        help_texts = {
            'username': 'Не более 150 символов. Допустима латиница , цифры или символы @/./+/-/_'
        }
        error_messages = {
            'username': {
                'unique': 'Пользователь с таким именем уже существует'
            }
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError(self.error_messages['no_password_confirmation'])
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(self.error_messages['password_mismatch'])
        
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user
    

class LoginForm(forms.Form):
    error_messages = {
        'invalid_credentials': 'Неверный логин или пароль'
    }

    username = forms.CharField(
        label='Имя',
        widget=forms.TextInput,
        help_text='Введите ваше имя'
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        help_text='Введите ваш пароль'
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError(self.error_messages['invalid_credentials'])
            cleaned_data['user'] = user
            
        return cleaned_data