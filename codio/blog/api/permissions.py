from rest_framework import permissions


class AuthorModifyOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user == obj.author


class IsAdminUserForObject(permissions.IsAdminUser):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_staff)



# class ExampleComOnly(permissions.BasePermission): # allow only @example.com email
#     def has_permission(self, request, view):
#         email = getattr(request.user, "email", "")
#         return email.split("@")[-1] == "example.com"

## has_object_permission in DRF-defined classed always return True! => Caution with A | B. So C(B) and then A|C in above
