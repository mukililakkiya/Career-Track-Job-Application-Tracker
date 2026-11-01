from django.db import models
from django.contrib.auth.models import User


class JobApplication(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Interview', 'Interview'),
        ('Selected', 'Selected'),
        ('Rejected', 'Rejected'),
    ]

    company_name = models.CharField(max_length=100)
    job_role = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    applied_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Applied'
    )

    job_link = models.URLField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.company_name + " - " + self.job_role