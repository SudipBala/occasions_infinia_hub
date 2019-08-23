from django.contrib import messages
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from outlets.category_models import Category
from outlets.forms import CategoryForm


class ListCategory(ListView):
    model = Category
    template_name = "outlets/category/list_category.html"
    context_object_name = "category_status"

    def get_queryset(self):
        queryset = {'active': Category.objects.get_categories(),
                   'inactive': Category.objects.filter(level=0, disabled=True)
                    }
        return queryset


class ListSubCategory(ListView):
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


class DeleteCategory(DeleteView):
    model = Category
    queryset = Category.objects.all()

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, ** kwargs)

    def get_success_url(self):
        messages.success(self.request, "{name} {message}".format(name=self.object.category_name,
                                                                 message="had been deleted."))
        return reverse('category:list_category')
