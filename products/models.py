import os
import random

from django.db import models

# Create your models here.
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.views.generic import ListView, DetailView

from products.utils import unique_slug_generator


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 999999999)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return 'products/{new_filename}/{final_filename}'.format(
        new_filename=new_filename,
        final_filename=final_filename
    )


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)


class ProductManager(models.Manager):

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def featured(self):
        return self.get_queryset().filter(featured=True)

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def all(self):
        return self.get_queryset().active()


class Product(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(null=True, blank=True, unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
    image = models.ImageField(upload_to='product_images/', blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/products/{slug}/".format(slug=self.slug)

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     slug_check = Product.objects.filter(slug=self.slug)
    #     if slug_check:
    #         new_count = slug_check.count() + 1
    #         self.slug = self.slug + '-' + str(new_count)
    #
    #     super(Product, self).save(*args, **kwargs)


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)
