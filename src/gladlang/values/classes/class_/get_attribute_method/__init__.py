"""Check MRO class for method match with visibility and binding."""

from .bind_instance import ClassGetAttributeMethodBindInstance
from .bind_static import ClassGetAttributeMethodBindStatic
from .core import ClassGetAttributeMethodCore
from .instance_guard import ClassGetAttributeMethodInstanceGuard
from .visibility import ClassGetAttributeMethodVisibility


class ClassGetAttributeMethod(
    ClassGetAttributeMethodCore,
    ClassGetAttributeMethodVisibility,
    ClassGetAttributeMethodInstanceGuard,
    ClassGetAttributeMethodBindStatic,
    ClassGetAttributeMethodBindInstance,
):
    __slots__ = ()


__all__ = ["ClassGetAttributeMethod"]
