from . import pc_build_schema_registry


malis_schema_registry.add(
    "pc_build",
    {
        "pc_id": {
            "type": "integer",
            "required": True,
            "coerce": int,
        },
        "quantity": {"type": "string", "required": False, "empty": True},
    },
)