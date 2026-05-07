"""JSON Schemas para validacao de contrato dos endpoints de Store.

`ORDER_SCHEMA` valida o body de uma order individual (POST/GET).
`INVENTORY_SCHEMA` valida o mapa retornado por GET /store/inventory
(chaves arbitrarias com valores inteiros).
"""
ORDER_SCHEMA = {
    "type": "object",
    "required": ["id", "petId", "quantity", "status"],
    "properties": {
        "id": {"type": "integer"},
        "petId": {"type": "integer"},
        "quantity": {"type": "integer"},
        "shipDate": {"type": "string"},
        "status": {"type": "string", "enum": ["placed", "approved", "delivered"]},
        "complete": {"type": "boolean"},
    },
}

INVENTORY_SCHEMA = {
    "type": "object",
    "additionalProperties": {"type": "integer"},
}
