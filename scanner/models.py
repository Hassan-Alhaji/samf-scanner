# scanner/models.py
from django.db import models

class IntakeItem(models.Model):
    description = models.CharField(max_length=255)
    color       = models.CharField(max_length=50, blank=True)
    size        = models.CharField(max_length=50, blank=True)
    brand       = models.CharField(max_length=100, blank=True)
    quantity    = models.PositiveIntegerField(default=1)
    image       = models.ImageField(upload_to='products/%Y/%m/')
    created_at  = models.DateTimeField(auto_now_add=True)
    approved    = models.BooleanField(default=False)  # لا تُمنح رقم أصل إلا بعد الموافقة

    def __str__(self):
        return f"{self.description} – {self.brand} (x{self.quantity})"
    
    
class CustodyLocation(models.Model):
    name = models.CharField(max_length=100, unique=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    
class Asset(models.Model):
    asset_number = models.CharField(max_length=50, unique=True)
    intake_item  = models.OneToOneField(IntakeItem, on_delete=models.PROTECT)
    location     = models.ForeignKey(CustodyLocation, on_delete=models.SET_NULL, null=True)
    assigned_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ASSET {self.asset_number} – {self.intake_item.description}"