from django.urls import path
from .import views

urlpatterns = [
    path('',views.main,name='main'),
    path('store/',views.store,name='store'),
    path('app/contact/',views.contact,name='contact'),
    path('app/about/',views.about,name='about'),
    path('app/checkout/',views.checkout,name='checkout'),
    path('app/tracker/',views.tracker,name='tracker'),
    path('app/search/',views.search,name='search'),
    path('basic/',views.basic,name='basic'),
    # path('app/productView/',views.productView,name='productView'),
    path("app/products<int:myid>/", views.productView, name="productView"),


]