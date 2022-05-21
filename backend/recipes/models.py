from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    color = models.CharField(max_length=7, unique=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, null=True)

    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return (
            f'Название: {self.name} | '
            f'Цвет: {self.color} | '
            f'Идентификатор: {self.slug}'
        )
