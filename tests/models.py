from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class TestModel(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        app_label = "tests"
        abstract = True


class Customer(TestModel):
    first_name = models.TextField()
    last_name = models.TextField()


class Product(TestModel):
    sku = models.TextField()
    product_name = models.TextField()
    product_code = models.TextField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=16, decimal_places=2)
    regions = models.ManyToManyField("Region")


class Order(TestModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order_total = models.DecimalField(max_digits=16, decimal_places=2)


class Region(TestModel):
    name = models.TextField()
    label = models.TextField()


class TaggedItem(TestModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
