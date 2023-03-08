from django.urls import path
from category import views


urlpatterns = [
    path('',views.category_page, name = 'category-page')
]

