from django.db import models
from django.urls import reverse


CATEGORY_CHOICES = (
    ("S", "Shirt"),
    ("SW", "Sportwear"),
    ("OW", "Outwear")
)

LABEL_CHOICES = (
    ("P", "primary"),
    ("S", "secondary"),
    ("D", "danger")
)


class Item(models.Model):
    title = models.CharField(max_length=150)
    price = models.FloatField()
    category = models.CharField(choices = CATEGORY_CHOICES, max_length = 2)
    discount = models.FloatField(blank=True,null = True)
    label = models.CharField(choices = LABEL_CHOICES, max_length = 1)
    description = models.TextField()
    
    slug = models.SlugField()


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("product", kwargs={"slug": self.slug})
    
    def get_add_to_cart(self):
        return reverse("addtocart", kwargs={"slug": self.slug})
        
    def get_remove_from_cart(self):
        return reverse("removefromcart", kwargs={"slug": self.slug})
