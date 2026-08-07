"""
URL configuration for GeneralBlogProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from GeneralBlogApp.views import home, post_detail, write_post, delete_post, edit_post, signup, delete_comment
from django.conf.urls.static import static
from django.conf import settings
from GeneralBlogApp.views import PostListApi, PostDetailApi, CommentListApi, CommentDetailApi
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home , name='home'),
    path('post/<int:pk>/', post_detail, name='post_detail' ),
    path('write/', write_post, name='write_post'),
    path('post/<int:pk>/edit/', edit_post, name='edit_post'),
    path('post/<int:pk>/delete/', delete_post, name='delete_post'),
    path('comment/<int:pk>/delete/', delete_comment, name='delete_comment'),

    path('login/', auth_views.LoginView.as_view(template_name = 'GeneralBlogApp/login.html'), name='login' ),
    path('signup/', signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page = 'home'), name='logout' ),

    path('api/posts/', PostListApi.as_view(), name='posts_api'),
    path('api/posts/<int:pk>/', PostDetailApi.as_view(), name='post_detail_api'),
    path('api/login/', obtain_auth_token, name='api_login'),

    path('api/comments/', CommentListApi.as_view(), name='comments_api'),
    path('api/comments/<int:pk>/', CommentDetailApi.as_view(), name='comment_detail_api')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)