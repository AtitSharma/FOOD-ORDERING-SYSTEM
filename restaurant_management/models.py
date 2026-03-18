import uuid

from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Food(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField(default=1)
    in_stock = models.BooleanField(default=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="food_category",blank=True,null=True)

    def __str__(self):
        return self.name

class FoodImage(models.Model):
    food = models.ForeignKey(Food,related_name="food_image",on_delete=models.CASCADE)
    image = models.ImageField(upload_to="food_images")

    def __str__(self):
        return self.food.name

class Table(models.Model):
    name = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True)
    table_unique_id = models.UUIDField(default=uuid.uuid4(),unique=True)
    table_qr_code = models.ImageField(upload_to="table_qr_code",blank=True,null=True)

    def __str__(self):
        return self.name
    

    def save(self,*args,**kwargs):
        super().save(*args, **kwargs)
        if not self.table_qr_code:
            # URL with unique table ID
            qr_url = f"http://{settings.BE_LOCALHOST_IP}:8000/home/{self.table_unique_id}/"

            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_url)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            # Save image to BytesIO
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)

            # Save to ImageField
            self.table_qr_code.save(f"table_{self.table_unique_id}.png", File(buffer), save=False)

            # Save again to update the table_qr_code field
            super().save(*args, **kwargs)


class TableOrder(models.Model):
    table = models.ForeignKey(Table,on_delete=models.CASCADE,related_name="table_order")
    is_paid = models.BooleanField(default=False)
    amount = models.IntegerField(default=0)
    def __str__(self):
        return self.table.name


class TableOrderItem(models.Model):
    order = models.ForeignKey(TableOrder,related_name="table_order",on_delete=models.CASCADE)
    food = models.ForeignKey(Food,related_name="order_food",on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.food + self.order.table.name
    

class Cart(models.Model):
    table = models.ForeignKey(Table,on_delete=models.CASCADE,related_name="table_cart")
    food = models.ForeignKey(Food,on_delete=models.CASCADE,related_name="table_food_cart")
    quantity = models.PositiveIntegerField(default=1)
    