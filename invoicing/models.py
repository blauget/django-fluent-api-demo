from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=20, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.sku} - {self.name}"

class Invoice(models.Model):
    client = models.ForeignKey(Client, related_name='invoices', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Invoice {self.id} - {self.client.name}"

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='invoice_items', on_delete=models.PROTECT)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"
