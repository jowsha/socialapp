from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from social.models import Comments,Posts,UserDetails


class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["first_name","last_name","email","username","password1","password2"]
        widgets={
            "first_name":forms.TextInput(attrs={"class":"form-control mt-3","placeholder":"first name"}),
            "last_name":forms.TextInput(attrs={"class":"form-control mt-3","placeholder":"last name"}),
            "email":forms.TextInput(attrs={"class":"form-control mt-3","placeholder":"email","label":""}),
            "username":forms.TextInput(attrs={"class":"form-control mt-3","placeholder":"Username"}),
        }
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = ""    
        self.fields['last_name'].label = ""    
        self.fields['username'].label = ""    
        self.fields['email'].label = ""    
        self.fields['password1'].label = ""    
        self.fields['password2'].label = ""    
        self.fields['password1'].widget.attrs.update({
            "class":"form-control mt-3",
            "placeholder":"password",
        })
        self.fields['password2'].widget.attrs.update({
            "class":"form-control mt-3",
            "placeholder":"confirm password"
        }) 
          


class LoginForm(forms.Form):
    username=forms.CharField(label="",widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Username"}))
    password=forms.CharField(label="",widget=forms.TextInput(attrs={"class":"form-control","type":"password","placeholder":"Password"}))

class CommentsForm(forms.ModelForm):
    class Meta:
        model=Comments
        fields=[
            "comment"
            ]

        widgets={
            "comment":forms.TextInput(attrs={"class":"combox bg-dark","placeholder":"Add a Comment...","size":30})
        }
    def __init__(self, *args, **kwargs):
        super(CommentsForm, self).__init__(*args, **kwargs)
        self.fields['comment'].label = ""

class PostForm(forms.ModelForm):
    class Meta:
        model=Posts
        fields=[
            "post",
            "image",
            "decsription"
        ]
        widgets={
            "post":forms.TextInput(attrs={"class":"posbox bg-dark","placeholder":"Post title..","size":22},),
            "image":forms.FileInput(attrs={"class":"form-select imge bg-dark","placeholder":"select image",}),
            "decsription":forms.Textarea(attrs={"class":"posbox bg-dark","placeholder":"Write a caption..","rows":3,"cols":25}),
        }
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['post'].label = ""
        self.fields['decsription'].label = ""
        self.fields['image'].label = ""

class UserDetailForm(forms.ModelForm):
    class Meta:
        model=UserDetails
        fields=[
            "contact_no",
            "about",
            "place",
            "image"
        ]
        widgets={
            "contact_no":forms.TextInput(attrs={"class":"form-control","placeholder":"Phone","size":22},),
            "about":forms.Textarea(attrs={"class":"form-control","placeholder":"Write about you..","rows":3,"cols":25}),
            "place":forms.TextInput(attrs={"class":"form-control","placeholder":"place","rows":3,"cols":25}),
            "image":forms.FileInput(attrs={"class":"form-select ","placeholder":"select image",}),

        }
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserDetailForm, self).__init__(*args, **kwargs)
        self.fields['image'].label = "" 
        print(self.request)
        if self.request:
            userde=UserDetails.objects.get(user=self.request.user)
            self.fields['about'].initial= userde.about
            self.fields['contact_no'].initial= userde.contact_no
            self.fields['place'].initial= userde.place
  


