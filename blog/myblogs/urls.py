from django.urls import path
from . import views

app_name = 'myblogs'

urlpatterns = [
    path('', views.PublicPostIndexView.as_view(), name='top'),
    path('private/', views.PrivatePostIndexView.as_view(),
         name='private_post_list'),
    path('detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('comment/<int:pk>/', views.CommentCreate.as_view(), name='comment_create'),
    path('reply/create/<int:pk>/', views.ReplyCreate.as_view(), name='reply_create'),
]
