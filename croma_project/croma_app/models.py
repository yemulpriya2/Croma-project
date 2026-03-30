from django.db import models

# Create your models here.
class Product(models.Model):
    p_id=models.IntegerField(primary_key=True)
    p_name=models.CharField(max_length=50)
    category=models.CharField(max_length=50)
    price=models.IntegerField()
    quantity=models.IntegerField()

    def __str__(self):
        return self.p_name
    
    

