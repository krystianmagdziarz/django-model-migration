from django.db import models


class Subscriber(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True)
    gdpr_consent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email} - {self.create_date}"


class SubscriberSMS(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(unique=True, max_length=15)
    gdpr_consent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.phone} - {self.create_date}"


class Client(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.email} - {self.phone} - {self.create_date}"


class User(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    gdpr_consent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email} - {self.phone}"
