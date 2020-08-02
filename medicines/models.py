from django.db import models
from django.urls import reverse


# Create your models here.
class Medicine (models.Model):
    name = models.CharField(max_length=50, unique=True)

    def get_absolute_url(self):
        return reverse('medicines', args=[str(self.id)])

    def __str__(self):
        return self.name


class Source (models.Model):
    name = models.CharField(max_length=30)
    url = models.URLField(unique=True)
    scrap_function = models.BinaryField(null=True)

    def __str__(self):
        return f'{self.name} ({self.url})'


class Info (models.Model):
    TYPE_CHOICES = [(0, 'News'), (1, 'Article')]

    type = models.SmallIntegerField(choices=TYPE_CHOICES)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)

    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    url = models.URLField()
    img_src = models.URLField(default='', name='Image Source')

    report_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
