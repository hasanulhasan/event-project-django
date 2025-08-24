from django import forms
from django.contrib.auth.models import User, Permission, Group
import re
from django.contrib.auth.forms import AuthenticationForm
from events.forms import StyledFormMixin

class CustomRegistrationForm(StyledFormMixin, forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name','last_name', 'email', 'password1', 'confirm_password')

    # field errors
    def clean_password1(self):
            password1 = self.cleaned_data.get('password1')
            if not password1:
                raise forms.ValidationError("Password is required")
            if len(password1) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long")
            return password1
    
    # non field errors
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("confirm_password")

        if password1 and confirm_password and password1 != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

class CustomLoginForm(StyledFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()
