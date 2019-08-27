from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from libs.db_func import update_file_path, CATEGORY_IMAGE_PATH
from libs.models import CustomModel, CustomManager


def category_image_path(instance, filename):
    return update_file_path(CATEGORY_IMAGE_PATH + '{0}.{1}'.format(instance.category_name,
                                                                  filename.split('.')[-1]))


class CategoryManager(models.Manager):

    def get_categories(self):
        return self.filter(level=0, disabled=False)

    def get_sub_categories(self):
        return self.filter(level=1, disabled=False)


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
    image = models.ImageField('Category Image', upload_to=category_image_path, help_text="Upload an icon for category.")
    disabled = models.BooleanField('Is Inactive', default=False)
    objects = CategoryManager()

    def __str__(self):
        return '({0}).{1}, {2}'.format(self.level,
                                       self.parent.category_name if self.parent else " ",
                                       self.category_name)

    def get_childs(self):
        return type(self).objects.filter(parent=self)

    def get_display_name(self):
        return self.category_name
