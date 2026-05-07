"""JSON Schema para validacao de contrato do recurso User.

Valida o body retornado por GET /user/{username}. Exige `id` e `username`;
demais campos sao opcionais mas validados por tipo quando presentes.
"""
USER_SCHEMA = {
    "type": "object",
    "required": ["id", "username"],
    "properties": {
        "id": {"type": "integer"},
        "username": {"type": "string"},
        "firstName": {"type": "string"},
        "lastName": {"type": "string"},
        "email": {"type": "string"},
        "password": {"type": "string"},
        "phone": {"type": "string"},
        "userStatus": {"type": "integer"},
    },
}
