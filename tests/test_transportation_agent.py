
import json
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from app.agents.transportation_agent import TransportationAgent


def function_call(name, call_id, arguments):
    return SimpleNamespace(
        type="function_call",
        name=name,
        call_id=call_id,
        arguments=json.dumps(arguments),
    )


def model_response(response_id, output, text=""):
    return SimpleNamespace(
        id=response_id,
        output=output,
        output_text=text,
    )


def test_agent_calculates_total_demand():
    client = Mock()

    client.responses.create.side_effect = [
        model_response(
            "response_1",
            [
                function_call(
                    "calculate_total_demand",
                    "call_1",
                    {"demand": [100, 150, 80]},
                )
            ],
        ),
        model_response(
            "response_2",
            [],
            "Total demand is 330 units.",
        ),
    ]

    agent = TransportationAgent(client=client)

    result = agent.run("Calculate demand for 100, 150, 80")

    assert "330" in result
    assert client.responses.create.call_count == 2

    second_request = client.responses.create.call_args_list[1].kwargs

    assert second_request["previous_response_id"] == "response_1"

    tool_output = second_request["input"][0]

    assert tool_output["call_id"] == "call_1"
    assert json.loads(tool_output["output"]) == {
        "total_demand": 330
    }


def test_agent_checks_capacity_feasibility():
    client = Mock()

    client.responses.create.side_effect = [
        model_response(
            "response_1",
            [
                function_call(
                    "check_capacity_feasibility",
                    "call_1",
                    {
                        "demand": [100, 150, 80],
                        "capacity": [200, 100],
                    },
                )
            ],
        ),
        model_response(
            "response_2",
            [],
            "Capacity is insufficient by 30 units.",
        ),
    ]

    agent = TransportationAgent(client=client)

    result = agent.run("Can my DCs satisfy demand?")

    assert "30" in result

    second_request = client.responses.create.call_args_list[1].kwargs

    output = json.loads(second_request["input"][0]["output"])

    assert output["total_demand"] == 330
    assert output["total_capacity"] == 300
    assert output["is_feasible"] is False
    assert output["capacity_shortfall"] == 30


def test_agent_handles_multiple_tool_calls():
    client = Mock()

    client.responses.create.side_effect = [
        model_response(
            "response_1",
            [
                function_call(
                    "calculate_total_demand",
                    "call_1",
                    {"demand": [100, 150, 80]},
                ),
                function_call(
                    "check_capacity_feasibility",
                    "call_2",
                    {
                        "demand": [100, 150, 80],
                        "capacity": [200, 100],
                    },
                ),
            ],
        ),
        model_response(
            "response_2",
            [],
            "Demand is 330, capacity is 300, shortfall is 30.",
        ),
    ]

    agent = TransportationAgent(client=client)

    result = agent.run("Calculate demand and feasibility")

    assert "30" in result

    second_request = client.responses.create.call_args_list[1].kwargs

    tool_outputs = second_request["input"]

    assert len(tool_outputs) == 2
    assert {item["call_id"] for item in tool_outputs} == {
        "call_1",
        "call_2",
    }


def test_agent_rejects_unknown_tool():
    client = Mock()

    client.responses.create.return_value = model_response(
        "response_1",
        [
            function_call(
                "unknown_tool",
                "call_1",
                {},
            )
        ],
    )

    agent = TransportationAgent(client=client)

    with pytest.raises(ValueError, match="Unknown tool"):
        agent.run("Execute unknown tool")


def test_agent_stops_after_max_iterations():
    client = Mock()

    client.responses.create.side_effect = [
        model_response(
            f"response_{i}",
            [
                function_call(
                    "calculate_total_demand",
                    f"call_{i}",
                    {"demand": [100]},
                )
            ],
        )
        for i in range(6)
    ]

    agent = TransportationAgent(client=client)

    with pytest.raises(RuntimeError, match="maximum tool-calling"):
        agent.run("Keep calculating")
