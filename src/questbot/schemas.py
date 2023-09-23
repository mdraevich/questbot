schemav1 = {
    "type": "object",
    "required": ["name","description","start_date","duration","teams"],
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "start_date": {"type": "string"},
        "duration": {"type": "string"},
        "teams": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name","description","communication","tasks"],
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "communication": {"type": "string"},
                    "tasks": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["question","answer","hints"],
                            "properties": {
                                "question": {"type": "string"},
                                "answer": {"type": "string"},
                                "hints": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}