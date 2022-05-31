from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('<slug:slug>/', views.product_page, name="individual_product"),
]