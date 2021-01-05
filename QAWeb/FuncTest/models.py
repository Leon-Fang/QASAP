from django.db import models

# Create your models here.
class CheckpointImage(models.Model):
    description = models.CharField(max_length=120)
    testEv = models.ImageField(upload_to='checkpoint0')
    def __str__(self):
        return self.description
    class Meta:
        db_table = "CheckpointImage"
    