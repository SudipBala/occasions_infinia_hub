from django.db import models


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Category"

    name = models.CharField("Category", max_length=50, blank=False)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='children')

    def __str__(self):
        full_path = [self.name]
        k = self.parent

        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' -> '.join(full_path[::-1])