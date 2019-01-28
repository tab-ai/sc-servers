from django.db import models

# Create your models here.

class Bt_dev(models.Model):
    bt_id = models.CharField(max_length=20, blank=True)
    bt_address = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=10, blank=True)
    time = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.bt_id

    class Meta:
        get_latest_by = 'time'

class Bt_data(models.Model):
    # bt_id = models.ForeignKey(Bt_dev, on_delete=models.PROTECT, blank=True, null=True)
    bt_id = models.CharField(max_length=20, blank=True, null=True)
    temp = models.FloatField(null=True, blank=True)
    bpm = models.FloatField(null=True, blank=True)
    battery = models.FloatField(null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return "{}_{}".format(self.bt_id, str(self.time))

    class Meta:
        get_latest_by = 'time'

