from audioop import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.shortcuts import get_object_or_404

#model import
from .models import Blog
from .forms import UserForm, BlogForm


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def registerUser(request):
    form = UserForm()
    if request.user.is_authenticated:
        return redirect('home-page')  

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("home-page")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    return render (request=request, template_name="base/signup.html", context={"register_form":form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def loginUser(request):

    if request.user.is_authenticated:
        return redirect('home-page')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome! {request.user.username}")
            return redirect('home-page')
        else:
            messages.error(request, 'Username OR password does not match')
    return render(request, 'base/login.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def logoutUser(request):
    if request.user.is_staff:
        logout(request)
        messages.warning(request, "Admin successfully logged out")
        return redirect('admin-login')
    logout(request)
    messages.warning(request, "You are successfully logged out")
    return redirect('login')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def homepage(request):
    blogs = Blog.objects.all()
    context = { 'blogs': blogs}
    return render(request, 'base/home.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def loginAdmin(request):
    user = None
    if request.user.is_staff:
        return redirect('admin-page')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            User.objects.get(username=username, is_staff=True)
            user = authenticate(request, username=username, password=password)
        
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome! {request.user.username}")
                return redirect('admin-page')
            else:
                messages.error(request, 'Username OR password does not match')
        except:
            messages.error(request, 'You are not an Admin Yet')
    return render(request, 'base/admin/admin-login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda user: user.is_staff,login_url='/adminlogin')
def admin_page(request):
    users = User.objects.filter(is_staff= False)
    if(request.method=="POST"):
        keyword=request.POST.get('keyword')
        users=users.filter(username__icontains=keyword) 
    context = { 'users': users}
    return render(request, 'base/admin/home-page.html', context)

@user_passes_test(lambda user: user.is_staff,login_url='/adminlogin')
def admin_create_user(request):
    form = UserForm()
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, " User Created Successfully" )
            return redirect("admin-page")
        messages.error(request, "OOPs! Error Occured, Please Create Again!")
    return render (request, template_name="base/admin/create_user.html", context={"register_form":form})

@user_passes_test(lambda user: user.is_staff,login_url='/adminlogin')
def admin_update_user(request, pk):
    user = get_object_or_404(User, id = pk)
    if request.method == "POST":
        form = UserForm(request.POST,instance=user)
        if form.is_valid():
            user = form.save()
            messages.success(request, "User information updated Succesfully" )
            return redirect("admin-page")
        messages.error(request, "OOPs! Error Occured, Please Update Again!")

    form = UserForm(instance=user)
    return render(request, template_name="base/admin/create_user.html", context={"register_form":form})

@user_passes_test(lambda user: user.is_staff,login_url='/adminlogin')
def admin_delete_user(request, pk):
    user = get_object_or_404(User, id = pk)
    user.delete()
    messages.warning(request, "User Deleted Successfully")
    return redirect("admin-page")
    # return render (request, template_name="base/admin/create_user.html")

@login_required(login_url='login')
def createBlog(request):
    form = BlogForm()
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user_data = request.user
            blog.save()
            messages.success(request, "Blog created !")
            return redirect("home-page")
        messages.error(request, "OOPs! Blog not created!")
    return render(request, 'base/blog/create_blog.html', context={"blog_form":form})


@login_required(login_url='login')
def updateBlog(request, pk):
    blog = get_object_or_404(Blog, id = pk)

    if not (request.user.is_staff or request.user == blog.user_data):
        messages.error(request, "You can't update this post")
        return redirect("home-page")

    form = BlogForm(instance=blog)
    if request.method == "POST":
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            blog.save()
            messages.success(request, "Blog Updated Succesfully!")
            return redirect("home-page")
        messages.error(request, "OOPS! Blog not created!")
    return render(request, 'base/blog/create_blog.html', context={"blog_form":form})

 
@login_required(login_url='login')
def deleteBlog(request, pk):
    blog = get_object_or_404(Blog, id = pk)
    if request.user.is_staff or request.user == blog.user_data:
        blog.delete()
        messages.warning(request, "Post Deleted Successfully")
    else:
        messages.error(request, "You can't delete this post!")
    return redirect("home-page")

