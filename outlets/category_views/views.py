from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView

from outlets.category_models import Category
from outlets.forms import CategoryForm


class ListCategory(ListView):
    model = Category
    queryset = Category.objects.get_categories()
    template_name = "outlets/category/list_category.html"


class ListSubCategory(ListView):
    model = Category
    queryset = Category.objects.get_sub_categories()
    template_name = "outlets/category/list_sub_category.html"

    def get_queryset(self):
        category_id = self.kwargs['pk']
        return Category.objects.filter(parent_id=category_id)


class AddCategory(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "outlets/category/add_category.html"

    def get_success_url(self):
        return reverse('category:list_category')


class EditCategory(UpdateView):
    model = Category
    form_class = CategoryForm
    queryset = Category.objects.all()
    template_name = "outlets/category/add_category.html"

    def get_queryset(self):
        category_id = self.kwargs['pk']
        return Category.objects.filter(id=category_id)

    def get_success_url(self):
        return reverse('category:list_category')

