from rest_framework.permissions import BasePermission

class IsOpsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Ops').exists()

class IsClientUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Client').exists()

