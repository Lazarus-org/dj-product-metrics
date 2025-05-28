from django.contrib.auth.models import AnonymousUser


class BasePermission:
    """Base class for custom permission checks in Django views.

    Subclasses must implement `has_permission` and may optionally implement
    `has_object_permission` for object-level checks. This class is designed to
    work with Django template views and generic views similar to Django
    REST Framework Permissions.

    Raises:
        NotImplementedError: If `has_permission` is not implemented by a subclass.

    """

    def has_permission(self, request, view):
        """Check if the request has permission to access the view.

        Args:
            request: The Django HTTP request object.
            view: The Django view instance being accessed.

        Returns:
            bool: True if permission is granted, False otherwise.

        Raises:
            NotImplementedError: If not implemented by a subclass.

        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement `has_permission`."
        )

    def has_object_permission(self, request, view, obj):
        """Check if the request has permission to access a specific object.

        By default, this method delegates to `has_permission`, but subclasses
        can override it for object-level permission checks.

        Args:
            request: The Django HTTP request object.
            view: The Django view instance being accessed.
            obj: The object being accessed (e.g., a model instance).

        Returns:
            bool: True if permission is granted, False otherwise.

        """
        return self.has_permission(request, view)


class AllowAny(BasePermission):
    """Allow access to all users, including unauthenticated users.

    This permission class grants access to any request, making it
    suitable for public views or read-only endpoints.

    """

    def has_permission(self, request, view):
        """Grant permission to all requests.

        Args:
            request: The Django HTTP request object.
            view: The Django view instance being accessed.

        Returns:
            bool: Always True.

        """
        return True

    def has_object_permission(self, request, view, obj):
        """Grant permission to all requests for any object.

        Args:
            request: The Django HTTP request object.
            view: The Django view instance being accessed.
            obj: The object being accessed (e.g., a model instance).

        Returns:
            bool: Always True.

        """
        return True


class IsAuthenticated(BasePermission):
    """Allow access only to authenticated users.

    This permission class grants access to users who are logged in,
    denying access to anonymous users. It is suitable for views that
    require user authentication.

    """

    def has_permission(self, request, view):
        """Check if the user is authenticated.

        Args:
            request: The Django HTTP request object.
            view: The Django view instance being accessed.

        Returns:
            bool: True if the user is authenticated, False otherwise.

        """
        return bool(
            request.user
            and not isinstance(request.user, AnonymousUser)
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """Check if the user is authenticated for object-level access.

        Delegates to `has_permission` by default, but can be overridden for
        object-specific checks (e.g., checking if the user owns the object).

        Args:
            request: The Django HTTP request object.
            view: The Django view instance being accessed.
            obj: The object being accessed (e.g., a model instance).

        Returns:
            bool: True if the user is authenticated, False otherwise.

        """
        return self.has_permission(request, view)


class IsAdminUser(BasePermission):
    """Allow access only to admin (staff) users.

    This permission class grants access to users with `is_staff=True`,
    typically administrators, denying access to non-staff users and
    anonymous users.

    """

    def has_permission(self, request, view):
        """Check if the user is authenticated and has staff status.

        Args:
            request: The Django HTTP request object.
            view: The Django view instance being accessed.

        Returns:
            bool: True if the user is authenticated and has `is_staff=True`, False otherwise.

        """
        return bool(
            request.user
            and not isinstance(request.user, AnonymousUser)
            and request.user.is_authenticated
            and request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        """Check if the user is authenticated and has staff status for object-
        level access.

        Delegates to `has_permission` by default, but can be overridden for
        object-specific checks.

        Args:
            request: The Django HTTP request object.
            view: The Django view instance being accessed.
            obj: The object being accessed (e.g., a model instance).

        Returns:
            bool: True if the user is authenticated and has `is_staff=True`, False otherwise.

        """
        return self.has_permission(request, view)


class IsSuperUser(BasePermission):
    """Allow access only to superuser accounts.

    This permission class grants access to users with
    `is_superuser=True`, typically reserved for high-level
    administrators, denying access to all other users, including staff
    and anonymous users.

    """

    def has_permission(self, request, view):
        """Check if the user is authenticated and has superuser status.

        Args:
            request: The Django HTTP request object.
            view: The Django view instance being accessed.

        Returns:
            bool: True if the user is authenticated and has `is_superuser=True`, False otherwise.

        """
        return bool(
            request.user
            and not isinstance(request.user, AnonymousUser)
            and request.user.is_authenticated
            and request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        """Check if the user is authenticated and has superuser status for
        object-level access.

        Delegates to `has_permission` by default, but can be overridden for
        object-specific checks.

        Args:
            request: The Django HTTP request object.
            view: The Django view instance being accessed.
            obj: The object being accessed (e.g., a model instance).

        Returns:
            bool: True if the user is authenticated and has `is_superuser=True`, False otherwise.

        """
        return self.has_permission(request, view)
