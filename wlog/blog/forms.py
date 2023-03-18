
from django import forms
from .models import Profile, Post

class SignInForm(forms.Form):
    nickname = forms.CharField(max_length=200, label="nickname", required=True)
    password = forms.CharField(label="password", widget=forms.PasswordInput(), required=True)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        #fields = "__all__"
        fields = ["name", "last_name", "picture", "location"]


class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "body", "image"]