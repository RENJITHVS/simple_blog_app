from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Blog
from django.core.exceptions import ValidationError


class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2",)

    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return username  
  
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError(" Email Already Exist")  
        return email  
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2  

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class BlogForm(forms.ModelForm):
    title = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter the Blog title'}),)
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter the description' }))
    # public = forms.BooleanField(widget=forms.RadioSelect())
    
    class Meta:
        model = Blog
        fields = ('title', 'tag_line', 'description',)

    def clean_title(self):
        data = self.cleaned_data['title']
        if len(data)<=10:
            raise ValidationError("Please Enter the title with more than 10 letters!")
        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data
    

    
