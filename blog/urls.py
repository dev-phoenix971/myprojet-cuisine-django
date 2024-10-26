from django.urls import path
from blog import views


app_name = 'blog'



urlpatterns = [
    path('', views.BlogList.as_view(), name="blog_list"),
    path('create/', views.CreateBlog.as_view(), name="create_blog"),
    # path('<str:slug>/', views.DetailBlog.as_view(), name="detail_blog"),
    path('details/<str:slug>/', views.blog_details, name="blog_details"),
    path('liked/<pk>', views.liked, name="liked_post"),
    path('unliked/<pk>', views.unliked, name="unliked_post"),
    path('edit/<str:slug>/', views.UpdateBlog.as_view(), name="edit_blog"),
    path('delete/<str:slug>/', views.DeleteBlog.as_view(), name="delete_blog"),
]