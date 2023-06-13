from django.db import models
from category.models import Category
from django.urls import reverse

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug         = models.SlugField(max_length=200,unique=True)
    description  = models.TextField(max_length=500,blank=True)
    price        = models.IntegerField()
    images       = models.ImageField(upload_to='images/products/')
    stock        = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category     = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        #reverse function is used to generate a URL based on a view function or a named URL pattern.
        return reverse('product_detail', args=[self.category.slug,self.slug])

    def __str__(self):
        return self.product_name 


#Variation Manager allows you to modify Queryset
class VariationManager(models.Manager):
      def colors(self):
          return super(VariationManager, self).filter(variation_category='color',is_active=True)
      
      def size(self):
          return super(VariationManager, self).filter(variation_category='size',is_active=True) 


variation_category_choice = (
    ('color','color'),
    ('size','size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100,choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    #Now we are telling this model that we have created variation manager for you. so we can use it
    objects = VariationManager()

    def __str__(self):
        #to return non string as product is foregein model, we use unicode
        return self.variation_value
    

class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products', max_length=255)

    def __str__(self) :
        return self.product.product_name
    
    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'