from django.db import models


class signup(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.IntegerField()
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=225)
    pincode = models.IntegerField(null=True)
    state = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30,null=True)
    building_name = models.TextField(null=True)
    road_name = models.CharField(max_length=30,null=True)



class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcats')

    def __str__(self):
        return self.name

class Subsubcategory(models.Model):
    name = models.CharField(max_length=100)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='subsubcats')

    def __str__(self):
        return self.name
class HairType(models.Model):
    name = models.CharField(max_length=50)

class HairColor(models.Model):
    name = models.CharField(max_length=50)

class product(models.Model):
    product_name = models.CharField(max_length=100)
    product_price = models.IntegerField()
    product_quantity = models.IntegerField()
    image = models.ImageField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    sub_sub_category = models.ForeignKey(Subsubcategory, on_delete=models.CASCADE, null=True, blank=True)
    hair_type = models.CharField(max_length=50, blank=True, null=True)
    hair_color = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    def stock_status(self):
        if self.product_quantity == 0:
            return "Out of Stock"
        elif self.product_quantity <= 5:
            return "Low Stock"
        return "In Stock"



class orders(models.Model):
    user_details = models.ForeignKey(signup, on_delete=models.CASCADE)
    product_details = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    amount = models.IntegerField()
    delivery_boy = models.CharField(max_length=30,null=True)
    product_status = models.CharField(max_length=30,default='order placed')
    order_date = models.DateTimeField()

class cart(models.Model):
    product_details=models.ForeignKey(product,on_delete=models.CASCADE)
    user_details=models.ForeignKey(signup,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    total_price=models.IntegerField()

# class orders(models.Model):
#     user_details = models.ForeignKey(signup, on_delete=models.CASCADE)
#     product_details = models.ForeignKey(product, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     amount = models.IntegerField()
#     delivery_boy = models.CharField(max_length=30,null=True)
#     product_status = models.CharField(max_length=30,default='order placed')
#     order_date = models.DateTimeField()

class wishlist(models.Model):
    user_details = models.ForeignKey(signup, on_delete=models.CASCADE)
    product_details = models.ForeignKey(product, on_delete=models.CASCADE)


class delivery_boy_register(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.IntegerField()
    driving_license_no = models.IntegerField()
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    work_status = models.CharField(max_length=30,default='Free')
    status = models.CharField(max_length=30,default='Pending')

class PasswordReset(models.Model):
    user_details = models.ForeignKey(signup, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
