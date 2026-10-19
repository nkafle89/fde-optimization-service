import json
from openai import OpenAI
from app.tools.transportation_tools import calculate_total_demand, check_capacity_feasibility

TOOLS= [
    {
        "type": "function",
        "name": "calculate_total_demand",
        "description": "Calculate the total demand across stores.",
        "parameters": {
            "type": "object",
            "properties": {
                "demand": {
                    "type": "array",
                    "items": {"type": "number"},
                    "description": "Nonnegative store demand values",
                }
            },
            "required": ["demand"],
            "additionalProperties": False,
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "check_capacity_feasibility",
        "description": (
            "Check whether total distribution center capacity "
            "is sufficient to satisfy total store demand."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "demand": {
                    "type": "array",
                    "items": {"type": "number"},
                    "description": "Demand for each store",
                },
                "capacity": {
                    "type": "array",
                    "items": {"type": "number"},
                    "description": "Capacity of each distribution center",
                },
            },
            "required": ["demand", "capacity"],
            "additionalProperties": False,
        },
        "strict": True,
    }
]


class TransportationAgent:
    def __init__(self, client: OpenAI | None = None):
        self.client = client or OpenAI()

    def run(self, user_message: str) -> str:
        response = self.client.responses.create(
            model="gpt-4o-mini",
            instructions=(
                "You are a transportation optimization assistant. "
                "Use available tools for numerical calculations. "
                "Do not invent tool results."
            ),
            input=user_message,
            tools=TOOLS,
        )

        #Preserve the model's tool-call messages.
        conversation = [
            {"role": "user", "content": user_message},
            *response.output,
        ]

        for item in response.output:
            if item.type != "function_call":
                continue

            arguments = json.loads(item.arguments)

            if item.name == "calculate_total_demand":
                result = calculate_total_demand(arguments["demand"])
            elif item.name == " check_capacity_feasibility":
                result = check_capacity_feasibility(
                    demand=arguments["demand"],
                    capacity=arguments["capacity"],
                    )
            else:
                raise ValueError(f"Unknown tool: {item.name}")

            conversation.append(
                {
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps({"total_demand": result}),
                }
            )

            if not any(
                item.type == "function_call" for item in response.output
            ):
                return response.output_text

            final_response = self.client.responses.create(
                model="gpt-4o-mini",
                instructions=(
                    "Answer using the results returned by the tools."
                ),
                input=conversation,
                tools=TOOLS,
            )

            return final_response.output_text