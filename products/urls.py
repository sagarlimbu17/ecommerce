from django.urls import path

from products.views import (ProductListView, view_product_list,
                            ProductDetailView, view_product_detail,
                            ProductFeaturedListView, ProductFeaturedDetailView, ProductDetailSlugView)

urlpatterns = [
    path('products/', ProductListView.as_view()),
    path('fn-product-list', view_product_list, name='product-list'),
    path('cb-product-detail/<int:pk>', ProductDetailView.as_view()),
    path('products/<str:slug>/', ProductDetailSlugView.as_view()),
    path('fn-product-detail/<int:pk>', view_product_detail, name='product-detail'),
    path('featured/', ProductFeaturedListView.as_view()),
    path('fn-product-detail/<int:pk>', view_product_detail, name='product-detail'),
]