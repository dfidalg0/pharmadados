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

    def html(self):
        return f'<a href="{self.url}">{self.name}</a>'


class Info (models.Model):
    class Meta:
        ordering = ['-id']

    TYPE_CHOICES = [(0, 'News'), (1, 'Article')]

    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)

    type = models.SmallIntegerField(choices=TYPE_CHOICES)

    title = models.CharField(max_length=150)
    description = models.TextField()

    url = models.URLField(verbose_name='URL', max_length=1000)
    img_src = models.URLField(
        null=True, blank=True, max_length=1000,
        verbose_name='Image Source'
    )

    report_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
