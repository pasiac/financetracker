from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=128)
    category = models.CharField(max_length=30)
    image = models.ImageField(upload_to="img", null=True, blank=True)
    description = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.title


class Price(models.Model):
    shop_name = models.CharField(max_length=30)
    value = models.DecimalField(decimal_places=2, max_digits=8)
    pub_date = models.DateTimeField(auto_now_add=True, blank=True)
    expire_date = models.DateTimeField(blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product}, {self.value}"
