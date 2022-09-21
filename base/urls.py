from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="home-page"),
    path('login', views.loginUser, name="login"),
    path('logout', views.logoutUser, name="logout"),
    path('signup', views.registerUser, name="signup"),
    path('adminpage', views.admin_page, name="admin-page"),
    path('adminlogin', views.loginAdmin, name="admin-login"),
    path('admincreateuser', views.admin_create_user, name="admin-create-user"),
    path('adminupdateuser/<str:pk>', views.admin_update_user, name="admin-update-user"),
    path('admindeleteuser/<str:pk>', views.admin_delete_user, name="admin-delete-user"),
    path('createblog', views.createBlog, name="create-blog"),
    path('updateblog/<str:pk>', views.updateBlog, name="update-blog"),
    path('deleteblog/<str:pk>', views.deleteBlog, name="delete-blog"),
]
