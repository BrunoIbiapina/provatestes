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
