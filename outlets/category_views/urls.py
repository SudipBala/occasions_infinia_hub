from django.urls import path

from outlets.category_views.views import AddCategory, ListCategory, ListSubCategory, EditCategory, DeleteCategory

app_name = 'category'

urlpatterns = [
    path('create/', AddCategory.as_view(), name='create'),
    path('', ListCategory.as_view(), name='list_category'),
    path('<int:pk>/sub-category/', ListSubCategory.as_view(), name='sub-category'),
    path('<int:pk>/edit', EditCategory.as_view(), name='edit'),
    path('<int:pk>/delete', DeleteCategory.as_view(), name='delete')

]
