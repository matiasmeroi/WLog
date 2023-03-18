from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    path("<int:page>", views.home, name="home"),
    path("sing_in/", views.sign_in, name="sign_in"),
    path("sign_out1/", views.sign_out, name="sign_out1"),
    path("sign_up", views.sign_up, name="sign_up"),
    path('logout/', auth_views.LogoutView.as_view(template_name='signout.html'), name='logout'),
    path('myaccount/', views.myaccount, name="myaccount"),
    path("about/", views.about, name="about"),

    path('create_post/', views.create_post, name="create_post"),
    path('list_posts/<int:user_id>/', views.list_posts, name="list_posts"),
    path('post/<int:post_id>/', views.post, name="post"),
    path('like/<int:post_id>/', views.like_post, name="like_post"),

    path('search/', views.search_user, name="search_user"),
    path('profile/<int:user_id>', views.profile, name="profile"),

]
