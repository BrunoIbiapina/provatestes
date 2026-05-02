PET_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "photoUrls"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "category": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
            },
        },
        "photoUrls": {"type": "array", "items": {"type": "string"}},
        "tags": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                },
            },
        },
        "status": {"type": "string", "enum": ["available", "pending", "sold"]},
    },
}

PET_LIST_SCHEMA = {"type": "array", "items": PET_SCHEMA}
