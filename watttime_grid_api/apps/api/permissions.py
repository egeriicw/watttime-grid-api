from rest_framework.permissions import IsAuthenticated


class IsInGroup(IsAuthenticated):
    """
    Allow access to authenticated users in a group
    """
    GROUP = 'team'

    def has_permission(self, request, view):
        if super(IsInGroup, self).has_permission(request, view):
            return request.user.groups.all().filter(name=self.GROUP).exists()
