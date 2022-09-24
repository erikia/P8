"""LITReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import include, path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('django.contrib.auth.urls')),
    path('', views.home, name='home'),
    path('flux/', views.flux_view, name='flux'),
    path('abos/', views.abos_view, name='abos'),
    path('posts/', views.posts_view, name='posts'),
    path('flux/create_ticket/', include('ticket.urls', namespace='ticket')),
    path('flux/create_user', views.create_user, name='create_user'),
    path('flux/log_user', views.log_user, name='log_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('flux/create_review/', include('review.urls', namespace='review')),
    path('posts/modify/<str:content_type>/<int:content_id>', views.modify_view, name='modify'),
    path('posts/delete/<str:content_type>/<int:content_id>', views.delete_view, name='delete'),
    path('abos/unfollow/<str:username>', views.unfollow_view, name='unfollow')
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)