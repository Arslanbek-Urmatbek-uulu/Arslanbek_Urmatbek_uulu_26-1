from django.db import models

class Product(models.Model):
    image = models.ImageField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    rate = models.FloatField(default=0.0)
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    text = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.text} --> {self.product.title}'