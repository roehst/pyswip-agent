# Using the agents SDK will
# make it easier to provide tools and manage state,
# since the Agent handles all tool calls for us.
from typing import Any, Protocol

import dotenv
import rich
from agents import Agent, RunResult, Runner, function_tool

# We will use agents web search tool to gather
# macroeconomic data.
from agents.tool import WebSearchTool

import json

dotenv.load_dotenv()
from pyswip import Prolog  # noqa: E402

type PrologQueryAndResult = tuple[str, list[dict[str, Any]]]

_LAST_CALLS: list[PrologQueryAndResult] = []


def append_prolog_call(call: PrologQueryAndResult) -> None:
    global _LAST_CALLS
    _LAST_CALLS.append(call)


def get_last_calls() -> list[PrologQueryAndResult]:
    global _LAST_CALLS
    return _LAST_CALLS


def clear_last_calls() -> None:
    global _LAST_CALLS
    _LAST_CALLS.clear()


class Miniprolog:
    def __init__(self):
        self.prolog = Prolog()

    def assertz(self, fact: str, *args: Any):
        self.prolog.assertz(fact, *args)  # type: ignore

    def query(self, query: str) -> list[dict[str, Any]]:
        return list(self.prolog.query(query))  # type: ignore

    def consult(self, file: str) -> str:
        self.prolog.consult(file)  # type: ignore
        with open(file, "r") as f:
            return f.read()

    def consult_string(self, program: str):
        # put the program in a temporary file and consult it
        import tempfile

        with tempfile.NamedTemporaryFile(delete=True) as f:
            f.write(program.encode("utf-8"))
            f.flush()
            self.prolog.consult(f.name)  # type: ignore


class Car(Protocol):
    brand: str
    model: str
    year: int


# That said, we keep a history since we will log
# the full conversation to a JSON file.
def log_interaction(
    user_input: str, response: RunResult, queries: list[PrologQueryAndResult]
) -> None:
    # Append to a JSON file the full interaction
    log_entry = {
        "user_input": user_input,
        "agent_output": response.final_output_as(str),
        "queries": [
            {"query": str(q), "result": [str(r) for r in res]} for q, res in queries
        ],
    }
    with open("conversation_log.json", "a") as f:
        f.write(json.dumps(log_entry) + "\n")


def main():
    global _LAST_CALLS
    prolog = Miniprolog()

    prolog.consult("prelude.pl")

    with open("prelude.pl", "r") as f:
        prelude = f.read()
        prolog.consult_string(prelude)

    @function_tool
    def prolog_query(query: str) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = prolog.query(query)
        append_prolog_call((query, result))

        rich.print("[bold yellow]Prolog Call[/bold yellow]")
        rich.print(f"Query: {query}")
        for r in result:
            rich.print(f"  Result: {r}")
        return result

    instructions = f"""
    You are PrologGPT, an AI agent that can reason using Prolog.
    You have access to a Prolog interpreter via a single tool,
    `prolog_query(query: str) -> list[dict[str, Any]]`, which takes a Prolog query as input
    and returns the results as a list of dictionaries. If you must add new facts or rules,
    you can use query with assertz/1, retract/1, etc. Remember you can use listings, findall/3,
    and other Prolog predicates as needed. The full power of SWIPL is at your disposal.
    
    Your goal is to capture user knowledge in Prolog and reason about it.
    
    The original script, with Prelude definitions, is:
    ```
    {prelude}
    ```
    """

    rich.print(
        "Welcome to [bold magenta]PrologGPT[/bold magenta]! Type 'exit' or 'quit' to stop."
    )

    # Show the prompt in rich
    rich.print(f"[bold yellow]Instructions:[/bold yellow] {instructions}")

    agent = Agent(
        name="PrologGPT",
        model="gpt-5-mini",
        instructions=instructions,
        tools=[prolog_query, WebSearchTool()],
    )

    # This is how we keep the conversation state
    # in the new Responeses API and Agents SDK.
    # We do lose control over the full conversation state,
    # but this makes the demo simpler.
    previous_response_id: str | None = None

    # A basic input loop. The Agents SDK will handle all tool calls
    # which is a win over using Responses or Completions directly.

    while True:
        from rich.prompt import Prompt

        user_input = Prompt.ask("[bold green]User[/bold green]")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = Runner.run_sync(
            agent, user_input, previous_response_id=previous_response_id
        )
        previous_response_id = response.last_response_id
        last_calls: list[PrologQueryAndResult] = get_last_calls()
        log_interaction(user_input, response, last_calls)
        clear_last_calls()
        rich.print(
            f"[bold magenta]Agent[/bold magenta]: {response.final_output_as(str)}"
        )


if __name__ == "__main__":
    main()
