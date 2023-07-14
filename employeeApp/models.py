from django.db import models

class Province(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Qada(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Municipal(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    qada = models.ForeignKey(Qada, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name  
class Employee(models.Model):
    username = models.CharField(max_length=255 ,null=False, blank=False)
    password = models.CharField(max_length=255 ,null=False, blank=False)
    login_time = models.DateTimeField(auto_now_add=True,null=False)
    is_active = models.BooleanField(default=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True, blank=True)
    qada = models.ForeignKey(Qada, on_delete=models.CASCADE, null=True, blank=True)
    municipal = models.ForeignKey(Municipal, on_delete=models.CASCADE, null=True, blank=True)
    last_login = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.username
