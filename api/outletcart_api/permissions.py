from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

    message= 'Only the owner of the cart can perform write operation on cart'
    """
    custom permissions to allow onwer of an object to edit it
    """
    def has_object_permission(self, request, view, obj): #obj is the model instance returned by queryset for model
        """
        Read permission are allowed owners of object to edit it ,
        so we will allow GET, HEAD or OPTIONS requests
        :param request:
        :param view:
        :param obj:
        :return:
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        """
        Write permissions are allowed only for the owner of the object
        """
        return obj.associated_user == request.user