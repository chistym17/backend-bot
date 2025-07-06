from typing import Any, Dict

class Tool:
    def __init__(self, name: str, description: str, parameters: Dict[str, Any]):
        self.name = name
        self.description = description
        self.parameters = parameters

class ToolCallResult:
    def __init__(self, result: Any):
        self.result = result



class FormFillingTool(Tool):
    def __init__(self):
        super().__init__(
            name="form_filling",
            description="Fills a form field based on user speech. Requires a field name and a value.",
            parameters={
                "field": {
                    "type": "string",
                    "description": "The name of the form field to update, like 'name', 'email', or 'phone'."
                },
                "value": {
                    "type": "string",
                    "description": "The value to put into the field."
                }
            }
        )
