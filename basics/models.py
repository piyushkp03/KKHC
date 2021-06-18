from django.db import models

# Create your models here.

class Products(models.Model):
    pname=models.CharField(max_length=50,default="")
    pcategory=models.CharField(max_length=50,default="")
    pqty= models.FloatField(null=True, blank=True)
    pprice= models.FloatField(null=True, blank=True)
    pimage=models.ImageField(upload_to="Products",default="")
    pwt=models.CharField(max_length=50,default="",blank=True)
    pflavor=models.CharField(max_length=500,default="",blank=True)

    
    def __str__(self):
        return self.pname

class medicines(models.Model):
    pname=models.CharField(max_length=50,default="")
    pcategory=models.CharField(max_length=50,default="")
    pmolecule=models.CharField(max_length=50,default="",blank=True)
    pprice= models.FloatField(null=True, blank=True)
    pimage=models.ImageField(upload_to="Products",default="")
    pwt=models.CharField(max_length=50,default="",blank=True)
    pflavor=models.CharField(max_length=500,default="",blank=True)

    
    def __str__(self):
        return self.pname

class usercart(models.Model):
    email=models.CharField(max_length=50,default="")
    pname=models.CharField(max_length=50,default="")
    pcategory=models.CharField(max_length=50,default="")
    pprice= models.FloatField(null=True, blank=True)
    pimage=models.ImageField(upload_to="Products",default="")
    pwt=models.CharField(max_length=50,default="",blank=True)

    def __str__(self):
        return self.email

   

    
class orders(models.Model):
    
    name=models.CharField(max_length=50,default="")
    email=models.CharField(max_length=50,default="")
    address=models.CharField(max_length=200,default="")
    phone=models.CharField(max_length=50,default="")
    pid=models.CharField(max_length=50,default="")
    pname=models.CharField(max_length=50,default="")
    pprice= models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.pid+" "+self.pname+" "+self.name+" "+self.email

    


    

