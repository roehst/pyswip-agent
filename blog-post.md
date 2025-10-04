# Building a Reasoning Agent with Verifiable Logic: Prolog meets LLMs

Have you ever wondered how to build an AI agent that doesn't just *claim* to do calculations, but actually *proves* them? This is the story of combining Prolog's logical reasoning with LLM's natural language understanding to create something special: a reasoning agent where every calculation and logical inference is verifiable.

## The Concept

This small project shows how you can build a reasoning agent using **Prolog as the main engine**, with LLMs helping with natural language understanding and generation. It's as simple as it gets, yet incredibly powerful.

The agent uses OpenAI's Agents SDK and the PySwip library to interface with SWI-Prolog. It has access to a single function tool that takes a Prolog query as input and returns results as a list of dictionaries:

```python
@function_tool
def prolog_query(query: str) -> list[dict[str, Any]]:
    print("************ Running Prolog query: ", query)
    result = prolog.query(query)
    print("************ Result: ", result)
    return result
```

With this single tool, the agent can:
- Add facts to the knowledge base
- Define rules and predicates
- Query the Prolog knowledge base
- Perform logical inferences and mathematical calculations

## The Architecture

The implementation is straightforward. Here's the core integration code:

```python
from agents import Runner, Agent, function_tool
from typing import Any
from pyswip import Prolog

class Miniprolog:
    def __init__(self):
        self.prolog = Prolog()

    def query(self, query: str) -> list[dict[str, Any]]:
        return list(self.prolog.query(query))

def main():
    prolog = Miniprolog()
    
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
```

## A Real Example: Economic Analysis with Verifiable Math

Let's see this in action with a macroeconomic analysis scenario. The interaction is purely conversational, but every calculation is verifiable through Prolog.

### Populating Facts

```
User: Popule o PIB de cada pais da america latina em bilhoes de dolares em 2020

************ Running Prolog query:  assertz(pib(brasil, 1428)), assertz(pib(argentina, 383)), 
assertz(pib(chile, 282)), assertz(pib(uruguai, 56)), assertz(pib(paraguai, 40)), 
assertz(pib(colombia, 314)), assertz(pib(peru, 226)), ...

************ Result:  [{}]
```

The agent stores these as Prolog facts. Now they're in a structured knowledge base, ready for logical reasoning.

### Creating Rules

```
User: Crie uma regra que da o ranking de um pais em PIB

************ Running Prolog query:  assertz((ranking_pib(Pais, R) :- 
    findall(Pib, (pib(_, Pib)), ListPibs), 
    sort(0, @>=, ListPibs, SortedPibs), 
    pib(Pais, PibPais), 
    nth1(R, SortedPibs, PibPais)))
```

This creates a Prolog rule that:
1. Collects all GDP values
2. Sorts them in descending order
3. Finds a country's position in the sorted list

### Verifiable Calculations

Here's where it gets interesting. When asked to calculate per capita income:

```
User: Agora com uma consulta calcule a renda per capita do brasil.

************ Running Prolog query:  pib(brasil, Pib), populacao(brasil, Pop)
************ Result:  [{'Pib': 1428, 'Pop': 212.6}]

Agent: Para calcular a renda per capita, dividimos o PIB pela população:
Renda per capita = PIB / população = 1428 / 212.6 = 6.71 (em dólares de 2020, em milhares)
```

### Computing Growth Rates

Even complex financial formulas like CAGR (Compound Annual Growth Rate) become verifiable:

```
User: Crie um predicado CAGR que calcula o CAGR de dois valores em dois anos.

************ Running Prolog query:  assertz((cagr(ValorInicial, ValorFinal, AnoInicial, AnoFinal, CAGR) :- 
    DiferencaAnos is AnoFinal - AnoInicial, 
    CAGR is ((ValorFinal / ValorInicial) ** (1 / DiferencaAnos) - 1) * 100))

User: Agora, compute com essa regra o CAGR do brasil de 2000 a 2020

************ Running Prolog query:  pib_2000(brasil, Pib2000), pib(brasil, Pib2020), 
    cagr(Pib2000, Pib2020, 2000, 2020, CAGR)
************ Result:  [{'Pib2000': 644, 'Pib2020': 1428, 'CAGR': 4.061987665473099}]

Agent: O CAGR do PIB do Brasil de 2000 a 2020 foi de aproximadamente 4.06%.
```

## Why This Matters: Verifiable Logic and Math

**Here's the crucial insight**: Unlike traditional LLM-based agents that might hallucinate calculations or make logical errors, this Prolog integration makes the logic and mathematics **verifiable**. 

Every arithmetic operation, every logical inference, every rule application happens in Prolog's formal logic system. You can see exactly what queries are being run, what facts are being used, and what results are returned. The LLM handles the natural language interaction, but Prolog ensures the reasoning is sound.

This is particularly important for:
- **Financial calculations** where accuracy matters
- **Logical reasoning** where consistency is critical  
- **Auditable systems** where you need to trace every step
- **Complex rule-based domains** where relationships matter

All interaction with Prolog is displayed transparently, so you can see what the agent is doing under the hood. This transparency helps you understand and verify what's going on at every step.

## Try It Yourself

The repo is available at `roehst/pyswip-agent`. It's a simple yet powerful demonstration of how formal logic systems and LLMs can work together, each doing what they do best: Prolog handling verifiable reasoning and calculations, LLMs handling natural language interaction.

The beauty is in the simplicity: one function tool, one Prolog interpreter, and suddenly you have an AI agent with verifiable logic at its core.
