"""JSON Schemas para validacao de contrato dos endpoints de Pet.

`PET_SCHEMA` (strict) e usado em recursos criados pelos proprios testes
(POST/GET por id), onde garantimos os dados.

`PET_LIST_ITEM_SCHEMA` (frouxo) e usado em listagens publicas
(`/pet/findByStatus`), onde a API compartilhada retorna entradas poluidas
de outros usuarios. Apenas `id` e exigido; demais campos sao validados
quando presentes.
"""
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

PET_LIST_ITEM_SCHEMA = {
    "type": "object",
    "required": ["id"],
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

PET_LIST_SCHEMA = {"type": "array", "items": PET_LIST_ITEM_SCHEMA}
