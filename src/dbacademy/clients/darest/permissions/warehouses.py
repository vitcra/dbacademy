__all__ = ["Warehouses"]

from dbacademy.clients.rest.common import ApiClient
from dbacademy.clients.darest.permissions.crud import PermissionsCrud


class Warehouses(PermissionsCrud):
    valid_permissions = ["CAN_USE", "CAN_MANAGE"]

    def __init__(self, client: ApiClient):
        super().__init__(client, "/api/2.0/permissions/sql/warehouses", "warehouses")