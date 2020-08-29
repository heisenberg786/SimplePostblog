from django import forms
from django.contrib.auth.models import User
from basic_app.models import UserProfileInfo
from basic_app.models import Post

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('first_name','last_name','username','email','password')
class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site','profile_pic')

class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = '__all__'
