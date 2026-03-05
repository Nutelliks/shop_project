from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Categories(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Name')
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name='URL')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='children',
        verbose_name='subCategory'
    )
    is_active = models.BooleanField(default=True, verbose_name='Is_active')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data created')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data updated')


    class Meta:
        db_table = 'category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)



class Products(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Name')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    image = models.ImageField(upload_to='goods_images', blank=True, null=True, verbose_name='Image')
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Price')
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, verbose_name='Discount')
    quantity = models.PositiveIntegerField(default=0.00, verbose_name='Quantity')
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Category')


    class Meta:
        db_table = 'product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ("id", )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:product", kwargs={"product_slug": self.slug})
    
    def display_id(self):
        return f"{self.id:05}"
    
    
    
    def sell_price(self):
        if self.discount:
            return round(self.price - self.price*self.discount/100, 2)
        return self.price


