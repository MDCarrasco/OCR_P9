from django.urls import path
from django.contrib import admin
from app import views

admin.autodiscover()

urlpatterns = [
	path('', views.index_view, name='index'),
	path('signup/', views.SignUp.as_view(), name='signup'),
	path('login/', views.Login.as_view(), name='login'),
	path('logout/', views.Logout.as_view(), name='logout'),
	path('admin/', admin.site.urls),
]
