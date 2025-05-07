from django.db import models

class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    medication_name = models.CharField(max_length=100)
    administration_notes = models.CharField(max_length=500)
    usage_time = models.CharField(max_length=100)
    usage_importance = models.CharField(max_length=100)

    def __str__(self):
        return self.name
