from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View,TemplateView,CreateView,FormView,ListView,DetailView,UpdateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from social.forms import RegistrationForm,LoginForm,CommentsForm,PostForm,UserDetailForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from social.models import Comments,Posts,UserDetails
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
import os

from django.contrib import auth
 
# def create_profile(self, **kwargs):
#     UserDetails.objects.create(
#         user=self,
#         **kwargs # you can pass other fields values upon creating
#     )
# auth.models.User.add_to_class('create_profile',create_profile)
# Create your views here.
def signin_required(fn):
    def wrapper(request,*args,**kw):
        if not request.user.is_authenticated:
            messages.error(request,"u must login")
            return redirect("signin")
        else:
            return fn(request,*args,**kw)
    return wrapper

decorators=[signin_required,never_cache]
@method_decorator(decorators,name="dispatch")
class HomeView(CreateView,ListView,View):
    form_class=PostForm
    model=Posts
    template_name="index.html"
    success_url="home"
    context_object_name="posts"
    
    def get_context_data(self, **kwargs):
        context = super(HomeView,self).get_context_data(**kwargs)
        context["userd"] =UserDetails.objects.get(user=self.request.user) 
        context["use"] =Posts.objects.filter(user=self.request.user) 
        context["usep"] =Posts.objects.filter(user=self.request.user).count 
        return context

    # def get_context_data(self, **kwargs):
    #     context = super(HomeView,self).get_context_data(**kwargs)
    #     context["use"] =Posts.objects.filter(user=self.request.user) 
    #     return context
    
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        return Posts.objects.all().exclude(user=self.request.user)

decorators   
@method_decorator(decorators,name="dispatch")
class ProfileView(CreateView,ListView,View):
    model=UserDetails
    form_class=UserDetailForm
    template_name="profile.html"
    context_object_name="userdetails"
    success_url="profile"
    # def get(self,request,*args,**kw):
    #     form=UserDetailForm
    #     role=UserDetails.objects.get(user=self.request.user)
    #     use=Posts.objects.filter(user=self.request.user)
    #     usep=Posts.objects.filter(user=self.request.user).count
    #     return render(request,"profile.html",{"form":form,"role":role,"use":use,"usep":usep})
    # def get_queryset(self):
    #     return UserDetails.objects.get(user=self.request.user)
    def get_queryset(self):
        return UserDetails.objects.get(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context["use"] = Posts.objects.filter(user=self.request.user) 
        context["usep"] = Posts.objects.filter(user=self.request.user).count 
        context["role"] = UserDetails.objects.get(user=self.request.user)
        return context

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    def post(self,request,*args,**kwargs):
        id=self.request.user
        todo=UserDetails.objects.get(user=id)
        form=UserDetailForm(request.POST,request.FILES,instance=todo)
        if form.is_valid():
            form.save()
            firstn=request.POST.get("name")
            lastn=request.POST.get("lname")
            email=request.POST.get("email")
            User.objects.filter(username=self.request.user).update(first_name=firstn,last_name=lastn,email=email)
            return redirect("profile")
        else:
            return redirect("profile")
    def get_form_kwargs(self):
       kwargs = super(ProfileView, self).get_form_kwargs()
       kwargs['request'] =UserDetails.objects.get(user=self.request.user)
       return kwargs
class RegisterView(CreateView):
    model=User
    form_class=RegistrationForm
    template_name="register.html"
    context_object_name="form"
    success_url=reverse_lazy("signin")
    

    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            user = authenticate(request, username=user.username, password=request.POST['password1'])
            UserDetails.objects.create(user=user)
            if user is not None:
                login(request, user)
                return redirect('signin')
        return super().post(request, *args, **kwargs)


decorators
def upvote_view(request,*args,**kwargs):
    ans_id=kwargs.get("id")
    ans=Posts.objects.get(id=ans_id)
    ans.up_vote.add(request.user)
    ans.save()
    return redirect("home")
decorators    
def add_ans(request,*args,**kwargs):
    q_id=kwargs.get('id')
    ques=Posts.objects.get(id=q_id)
    ans=request.POST.get("comment")
    ques.comments_set.create(comment=ans,user=request.user)
    messages.success(request,"answer added successfully")
    return redirect("home")

class LoginView(FormView):
    template_name="login.html"
    form_class=LoginForm
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user=authenticate(request,username=uname,password=pwd)
            if user:
                login(request,user)
                return redirect("home")
            else:
                messages.error(request,"invalid details")
                return render(request,self.template_name,{"form":form})


decorators
def signout(request,*args,**kw):
    logout(request)
    return redirect("home")

    
