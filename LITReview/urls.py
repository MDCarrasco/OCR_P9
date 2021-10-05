from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from django.contrib import admin
from app import views

admin.autodiscover()

urlpatterns = [
	path('', views.index_view, name='index'),
	path('feed/', views.feed_view, name='feed'),
	path(
		'feed/new_review_request/',
		views.NewReviewRequest.as_view(),
		name='new_review_request'
	),
	path(
		'feed/new_review_without_ticket/',
		views.NewReviewWithoutTicket.as_view(),
		name='new_review_without_ticket'
	),
	path(
		'feed/new_review_with_ticket/<int:ticket_id>/',
		views.NewReviewWithTicket.as_view(),
		name='new_review_with_ticket'
	),
	path('posts/', views.posts_view, name='posts'),
	path('signup/', views.SignUp.as_view(), name='signup'),
	path('login/', views.Login.as_view(), name='login'),
	path('logout/', views.Logout.as_view(), name='logout'),
	path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
