"""thecode URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include, re_path
from accounts import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from questions.views import QuestionView, TagListView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', QuestionView.as_view(), name = "main_page"),
    path('question/', include('questions.urls')),

    path('accounts/', include('allauth.urls')),
    path('accounts/edit/', user_views.Edit.as_view(), name = 'edit'),
    path('accounts/profile/', user_views.Profile.as_view(), name = 'profile'),
    
    path('tags/', TagListView.as_view(), name = "tag_list"),

    path('user/<int:pk>/', user_views.GetUserData.as_view(), name = 'get_user'),
    path('user/', user_views.GetUsersList.as_view(), name = "user_list"),
    path('inbox/notifications/', include('notifications.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT) 