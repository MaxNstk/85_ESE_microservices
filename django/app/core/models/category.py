from django.db import models

from .base_model import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Nome")
    description = models.CharField(max_length=255, verbose_name="Descrição")

    class Meta:
        verbose_name= "Categoria"
        verbose_name_plural= "Categorias"

    def __str__(self) -> str:
        return self.name