from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from app import views
admin.autodiscover()

urlpatterns = [
    path('', views.index_view, name='index'),
	path('login/', views.Login.as_view(), name='login'),
	path('signup/', views.SignUp.as_view(), name='signup'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
]
