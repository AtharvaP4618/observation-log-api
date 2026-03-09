observation_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "title": {"type": "string"},
        "category": {"type": "string"},
        "date": {"type": "string"},
        "duration": {"type": "integer"},
        "notes": {"type": "string"},
        "created_at": {"type": "string"}
    }
}

get_observations_spec = {
    "tags": ["Observations"],
    "parameters": [
        {"name": "category", "in": "query", "type": "string"},
        {"name": "date", "in": "query", "type": "string"},
        {"name": "minDuration", "in": "query", "type": "integer"},
        {"name": "maxDuration", "in": "query", "type": "integer"},
        {"name": "page", "in": "query", "type": "integer"},
        {"name": "limit", "in": "query", "type": "integer"},
    ],
    "responses": {
        200: {
            "description": "List of observations",
            "schema": {
                "type": "array",
                "items": observation_schema
            }
        }
    }
}

get_observation_spec = {
    "tags": ["Observations"],
    "parameters": [
        {
            "name": "id",
            "in": "path",
            "type": "string",
            "required": True
        }
    ],
    "responses": {
        200: {
            "description": "Observation found",
            "schema": observation_schema
        },
        404: {
            "description": "Observation not found"
        }
    }
}

create_observation_spec = {
    "tags": ["Observations"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": observation_schema
        }
    ],
    "responses": {
        201: {
            "description": "Observation created"
        }
    }
}

update_observation_spec = {
    "tags": ["Observations"],
    "parameters": [
        {
            "name": "id",
            "in": "path",
            "type": "string",
            "required": True
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": observation_schema
        }
    ],
    "responses": {
        200: {
            "description": "Observation updated"
        },
        404: {
            "description": "Observation not found"
        }
    }
}

delete_observation_spec = {
    "tags": ["Observations"],
    "parameters": [
        {
            "name": "id",
            "in": "path",
            "type": "string",
            "required": True
        }
    ],
    "responses": {
        200: {
            "description": "Observation deleted"
        },
        404: {
            "description": "Observation not found"
        }
    }
}

health_spec = {
    "tags": ["System"],
    "responses": {
        200: {
            "description": "API health check"
        }
    }
}

meta_spec = {
    "tags": ["System"],
    "responses": {
        200: {
            "description": "API metadata"
        }
    }
}