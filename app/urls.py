from django.urls import path, re_path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings

urlpatterns = [
    path("", views.home),
    path('api/reg/staff/', views.reg_staff_view.as_view()),
    path('api/reg/', views.reg_view.as_view()),
    path('api/authenticate/', TokenObtainPairView.as_view()),
    path('api/follow/<int:id>/', views.follow_id_view.as_view()),
    path('api/unfollow/<int:id>/', views.unfollow_id_view.as_view()),
    path('api/user/', views.user_view.as_view()),
    path('api/posts/', views.posts_view.as_view()),
    path('api/posts/<str:id>/', views.posts_id_view.as_view()),
    path('api/like/<str:id>/', views.like_id_view.as_view()),
    path('api/unlike/<str:id>/', views.unlike_id_view.as_view()),
    path('api/comment/<str:id>/', views.comment_id_view.as_view()),
    path('api/all_posts/', views.all_posts_view.as_view()),
    path('api/all/', views.all_view.as_view()),
]

urlpatterns += []

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)