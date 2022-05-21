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


# class Recipe(models.Model):
#     name = models.CharField(max_length=200)
#     ingredients = models.ManyToMany('Ingredient') # количество
#     tags = models.ManyToMany('Tag')
#     image = models.BinaryField()
#     text = models.TextField('Описание')
#     cooking_time = models.PositiveSmallIntegerField()

#     class Meta:
#         ordering = ('name',)
    
#     def __str__(self):
#         return (
#             f'Название: {self.name} | '
#             # f'Автор: {self.username}'
#         )


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    measurement_unit = models.CharField(max_length=50)

    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return (
            f'Название: {self.name} | '
            f'Единицы измерения: {self.measurement_unit}'
        )
