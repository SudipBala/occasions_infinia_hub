from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class CategoryManager(models.Manager):

    def get_categories(self):
        return self.filter(level=0)

    def get_sub_categories(self):
        return self.filter(level=1)


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Category"

    level = models.IntegerField(_("Level"), validators=[
        MinValueValidator(-1, _("Minimum is zero.")),
        MaxValueValidator(2, _("Maximum is two. Levels go upto sub category only."))
    ], choices=((0, _("Category")),
                (1, _("Sub-Category")),
                )
                                )

    category_name = models.CharField("Category", max_length=50, blank=False)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='children')

    objects = CategoryManager()

    def __str__(self):
        return '({0}).{1}, {2}'.format(self.level,
                                       self.parent.category_name if self.parent else " ",
                                       self.category_name)

    def get_childs(self):
        return type(self).objects.filter(parent=self)

    def get_display_name(self):
        return self.category_name
