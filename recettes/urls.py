from django.urls import path
from recettes import views


app_name = 'recettes'


urlpatterns = [
    path('', views.recette_category, name="category"),
    path('<slug:recettecategory_slug>/',views.recettes_list,name='recettes'),
    path('recette/<str:recettecategory_title',views.recettes_list,name='recettes_list'),
    path('recettesdetail/<str:recettes_slug>/', views.recettes_detail, name='recettesdetail'),
]