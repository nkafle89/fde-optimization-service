from openai import OpenAI
from pydantic import BaseModel, Field


class TransportationIntent(BaseModel):
    objective: str
    num_distribution_centers: int | None = Field(
        default=None, ge=1
    )
    num_stores: int | None = Field(
        default=None, ge=1
    )
    constraints: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)     


class LLMService:
    def __init__(self, client: OpenAI | None = None):
        self.client = client or OpenAI()


    def parse_optimization_request(
            self,
            user_message: str,
    ) -> TransportationIntent:
        response = self.client.responses.parse(
            model="gpt-4o-mini",
            instructions=(
                "Extract a transportation optimization problem "
                "from the user's request. "
                "Do not invent missing numerical inputs. "
                "Report missing information explicitly."
            ),
            input=user_message,
            text_format=TransportationIntent,
        )
        if response.output_parsed is None:
            raise ValueError(
                "Model did not return a structured optimization intent"
            )

        return response.output_parsed

