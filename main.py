from agents import Runner, Agent, function_tool
from typing import Any, Protocol
import dotenv
from pprint import pprint

dotenv.load_dotenv()
from pyswip import Prolog  # noqa: E402


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


def main():
    print("Hello from pyswip-agent!")

    prolog = Miniprolog()

    prolog.consult("agent.pl")

    @function_tool
    def prolog_query(query: str) -> list[dict[str, Any]]:
        print("************ Running Prolog query: ", query)
        result = prolog.query(query)
        print("************ Result: ", result)
        return result

    instructions = """
    You are PrologGPT, an AI agent that can reason using Prolog.
    You have access to a Prolog interpreter via a single tool,
    `prolog_query(query: str) -> list[dict[str, Any]]`, which takes a Prolog query as input
    and returns the results as a list of dictionaries. If you must add new facts or rules,
    you can use query with assertz/1, retract/1, etc. Remember you can use listings, findall/3,
    and other Prolog predicates as needed. The full power of SWIPL is at your disposal.
    
    Your goal is to capture user knowledge in Prolog and reason about it.
    """

    agent = Agent(
        name="PrologGPT", model="gpt-4", instructions=instructions, tools=[prolog_query]
    )

    pprint(agent)

    previous_response_id: str | None = None
    

    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = Runner.run_sync(
            agent, user_input, previous_response_id=previous_response_id
        )
        previous_response_id = response.last_response_id
        print(f"Agent: {response.final_output_as(str)}")
        


if __name__ == "__main__":
    main()
