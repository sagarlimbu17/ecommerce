import os
import random

from django.http import Http404
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView, DetailView

from products.models import Product


class ProductFeaturedListView(ListView):
    template_name = "products/featured-list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.featured()


class ProductFeaturedDetailView(DetailView):
    template_name = "products/featured-detail.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.featured()


class ProductListView(ListView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        print(**kwargs)
        print(*args)
        return context


def view_product_list(request):
    queryset = Product.objects.all()
    context = {'object_list': queryset}
    return render(request, 'products/product_list.html', context)


class ProductDetailSlugView(DetailView):

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        # instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Product not found")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Exception Caught")
        return instance


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Product not found")
        return instance


def view_product_detail(request, pk):
    instance = Product.objects.get_by_id(pk)
    print(instance)
    if instance is None:
        raise Http404("Product doesn't exist")
    context = {
        'object': instance
    }
    return render(request, 'products/product_detail.html', context)
