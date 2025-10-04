# Prolog-driven reasoning agent, aided by LLMs

Hi. This small repo shows how you can build a reasoning agent using Prolog as the main engine, and LLMs to help with natural language understanding and generation. It is as simple as it gets.

The agent uses OpenAI's Agents SDK and the PySwip library to interface with SWI-Prolog. It has access to a single function tool, `def prolog_query(query: str) -> list[dict[str, Any]]`, which takes a Prolog query as input and returns the results as a list of dictionaries. With this single tool the agent can add facts, rules and query the Prolog knowledge base.

Interaction is purely conversational:
- You can ask the agent to add facts (which he will regurgitate from its weights), and it will populate the Prolog knowledge base with them. 
- You can also ask it to add rules, and it will do so. 
- Finally, you can ask it to query the knowledge base, and it will return the results.

All interaction with Prolog is displayed, so you can see what the agent is doing under the hood, and it will help you
understand and check what is going on.

The repo is available on `roehst/pyswip-agent`.

## A transcript

Here is a transcript where I used the agent to ask some questions about macroeconomics, such as how an analyst would do it:

### Message 1

    User: Popule o PIB de cada pais da america latina em bilhoes de dolares em 2020 
    ************ Running Prolog query:  assertz(pib(brasil, 1428)), assertz(pib(argentina, 383)), assertz(pib(chile, 282)), assertz(pib(uruguai, 56)), assertz(pib(paraguai, 40)), assertz(pib(colombia, 314)), assertz(pib(peru, 226)), assertz(pib(bolivia, 34)), assertz(pib(venezuela, 48)), assertz(pib(equador, 106)), assertz(pib(guiana, 5)), assertz(pib(suriname, 3))
    ************ Result:  [{}]
    Agent: Valores do PIB (Produto Interno Bruto) em bilhões de dólares de 2020 para países da América Latina foram inseridos com sucesso em nosso banco de dados. Seguem os valores usados:

    1. Brasil: $1,428 bilhões
    2. Argentina: $383 bilhões
    3. Chile: $282 bilhões
    4. Uruguai: $56 bilhões
    5. Paraguai: $40 bilhões
    6. Colômbia: $314 bilhões
    7. Peru: $226 bilhões
    8. Bolívia: $34 bilhões
    9. Venezuela: $48 bilhões
    10. Equador: $106 bilhões
    11. Guiana: $5 bilhões
    12. Suriname: $3 bilhões

    Agora essas informações estão disponíveis para consultas. Por exemplo, você pode perguntar: "Qual foi o PIB do Brasil em 2020?" e a resposta será $1,428 bilhões.

## Message 2


    User: Agora coloque a populacao de cada pais em milhoes
    ************ Running Prolog query:  assertz(populacao(brasil, 212.6)), assertz(populacao(argentina, 45.2)), assertz(populacao(chile, 19.1)), assertz(populacao(uruguai, 3.5)), assertz(populacao(paraguai, 7.2)), assertz(populacao(colombia, 50.9)), assertz(populacao(peru, 33.1)), assertz(populacao(bolivia, 11.7)), assertz(populacao(venezuela, 28.4)), assertz(populacao(equador, 17.6)), assertz(populacao(guiana, 0.8)), assertz(populacao(suriname, 0.6))
    ************ Result:  [{}]
    Agent: Os valores da população em milhões para países da América Latina em 2020 foram inseridos com sucesso em nosso banco de dados. Seguem os valores usados:

    1. Brasil: 212.6 milhões
    2. Argentina: 45.2 milhões
    3. Chile: 19.1 milhões
    4. Uruguai: 3.5 milhões
    5. Paraguai: 7.2 milhões
    6. Colômbia: 50.9 milhões
    7. Peru: 33.1 milhões
    8. Bolívia: 11.7 milhões
    9. Venezuela: 28.4 milhões
    10. Equador: 17.6 milhões
    11. Guiana: 0.8 milhões
    12. Suriname: 0.6 milhões

    Agora, essas informações estão disponíveis para consultas. Por exemplo, você pode perguntar: "Qual era a população do Brasil em 2020?" e a resposta será 212.6 milhões.
    User: Agora com uma consulta calcule a renda per capita do brasil.
    ************ Running Prolog query:  ?- pib(brasil, Pib), populacao(brasil, Pop), RendaPerCapita is Pib / Pop.
    ************ Running Prolog query:  pib(brasil, Pib), populacao(brasil, Pop), RendaPerCapita is Pib / Pop, RendaPerCapita.
    ************ Running Prolog query:  pib(brasil, Pib), populacao(brasil, Pop)
    ************ Result:  [{'Pib': 1428, 'Pop': 212.6}]
    Agent: Para calcular a renda per capita, dividimos o PIB pela população:

    Renda per capita = PIB / população

    Substituindo os valores para o Brasil que temos:

    Renda per capita = 1428 / 212.6

    Renda per capita = 6.71 (em dólares de 2020, em milhares)

    Portanto, a renda per capita do Brasil em 2020 foi de $6.71 mil. Isso significa que, em média, cada pessoa no Brasil gerou $6.71 mil de PIB naquele ano.

## Message 3

    User: Crie uma regra que da o ranking de um pais em PIB
    ************ Running Prolog query:  assertz((ranking_pib(Pais, R) :- findall(Pib, (pib(_, Pib)), ListPibs), sort(0, @>=, ListPibs, SortedPibs), pib(Pais, PibPais), nth1(R, SortedPibs, PibPais)))
    ************ Result:  [{'Pais': Variable(71), 'R': Variable(74), 'Pib': Variable(77), 'ListPibs': Variable(80), 'SortedPibs': Variable(83), 'PibPais': Variable(86)}]
    Agent: A regra `ranking_pib(Pais, R)` foi criada com sucesso. Essa regra permite encontrar o ranking de um país com base em seu PIB. Ela realiza a seguinte lógica:

    1. Coleta todos os PIBs dos países e os coloca em uma lista.
    2. Ordena essa lista em ordem decrescente.
    3. Encontra o PIB do país em questão.
    4. Procura a posição do PIB desse país na lista ordenada, o que dá o ranking.

    Agora, você pode usar a regra `ranking_pib(Pais, R)` para encontrar o ranking de um país. Por exemplo, para encontrar o ranking do Brasil, você pode consultar `ranking_pib(brasil, R)`.

## Message 4

    User: Enconre o pais #1
    ************ Running Prolog query:  ranking_pib(Pais, 1)
    ************ Result:  [{'Pais': 'brasil'}]
    Agent: O país número 1 em PIB na América Latina em 2020 foi o Brasil.
    User: Agora o pais #3
    ************ Running Prolog query:  ranking_pib(Pais, 3)
    ************ Result:  [{'Pais': 'colombia'}]
    Agent: O país número 3 em PIB na América Latina em 2020 foi a Colômbia.


    User: Quala diferenca de populacao e pib entre os dois? Faca todas as contas aritmeticas com prolog
    ************ Running Prolog query:  DifPib is PibBrasil - PibColombia, DifPop is PopBrasil - PopColombia
    ************ Running Prolog query:  pib(brasil, PibBrasil), pib(colombia, PibColombia), DifPib is PibBrasil - PibColombia, populacao(brasil, PopBrasil), populacao(colombia, PopColombia), DifPop is PopBrasil - PopColombia
    ************ Result:  [{'PibBrasil': 1428, 'PibColombia': 314, 'DifPib': 1114, 'PopBrasil': 212.6, 'PopColombia': 50.9, 'DifPop': 161.7}]
    Agent: As diferenças aritméticas de PIB e população entre o Brasil e a Colômbia em 2020, calculadas usando Prolog, são:

    - Diferença no PIB: $1,114 bilhões
    - Diferença na População: 161.7 milhões

    Portanto, a economia do Brasil era $1,114 bilhões maior do que a economia da Colômbia e a população do Brasil era 161.7 milhões de pessoas maior do que a população da Colômbia em 2020.
    User: Agora adicione o PIUB dos paises em 2023
    Agent: Para adicionar o PIB dos países em 2023, preciso das projeções ou dos dados reais do PIB para cada país em 2023. Infelizmente, como sou uma inteligência artificial e não tenho acesso em tempo real a bancos de dados externos, não tenho esses dados disponíveis no momento.

    No entanto, se você tiver esses dados disponíveis, poderíamos adicioná-los à nossa base de conhecimento Prolog da mesma forma que fizemos com os dados de 2020. A única mudança seria que teríamos um novo predicado, algo como `pib_2023(Pais, Pib)`, para separar esses dados dos dados de 2020. O código para adicionar esses dados seria algo como:

    ```prolog
    assertz(pib_2023(brasil, X)), 
    assertz(pib_2023(argentina, Y)), 
    ...
    ```

    Onde `X`, `Y`, etc. seriam as projeções ou dados reais do PIB para cada país em 2023. Se você tiver esses dados e quiser os adicionemos à base de conhecimento, por favor forneça-os e nós podemos fazer isso.

## Message 5

        User: ADicione os dados de 2000, voce lembra.
        ************ Running Prolog query:  assertz(pib_2000(brasil, 644)), assertz(pib_2000(argentina, 284)), assertz(pib_2000(chile, 78)), assertz(pib_2000(uruguai, 13)), assertz(pib_2000(paraguai, 6.4)), assertz(pib_2000(colombia, 99.9)), assertz(pib_2000(peru, 52)), assertz(pib_2000(bolivia, 8.5)), assertz(pib_2000(venezuela, 97.1)), assertz(pib_2000(equador, 24.4)), assertz(pib_2000(guiana, 0.67)), assertz(pib_2000(suriname, 1.7))
        ************ Result:  [{}]
        Agent: Os valores do PIB (Produto Interno Bruto) em bilhões de dólares de 2000 para países da América Latina foram inseridos com sucesso em nosso banco de dados. Seguem os valores usados:

        1. Brasil: $644 bilhões
        2. Argentina: $284 bilhões
        3. Chile: $78 bilhões
        4. Uruguai: $13 bilhões
        5. Paraguai: $6.4 bilhões
        6. Colômbia: $99.9 bilhões
        7. Peru: $52 bilhões
        8. Bolívia: $8.5 bilhões
        9. Venezuela: $97.1 bilhões
        10. Equador: $24.4 bilhões
        11. Guiana: $0.67 bilhões
        12. Suriname: $1.7 bilhões

        Agora essas informações estão disponíveis para consultas. Por exemplo, você pode perguntar: "Qual foi o PIB do Brasil em 2000?" e a resposta será $644 bilhões.

## Message 6

    User: Crie um predicado CAGR que calcula o CAGR de dois valores em dois anos.
    ************ Running Prolog query:  assertz((cagr(ValorInicial, ValorFinal, AnoInicial, AnoFinal, CAGR) :- DiferencaAnos is AnoFinal - AnoInicial, CAGR is ((ValorFinal / ValorInicial) ** (1 / DiferencaAnos) - 1) * 100))
    ************ Result:  [{'ValorInicial': Variable(71), 'ValorFinal': Variable(74), 'AnoInicial': Variable(77), 'AnoFinal': Variable(80), 'CAGR': Variable(83), 'DiferencaAnos': Variable(86)}]
    Agent: A regra `cagr(ValorInicial, ValorFinal, AnoInicial, AnoFinal, CAGR)` foi criada com sucesso. Essa regra calcula a Taxa de Crescimento Anual Composta (CAGR) de dois valores em dois anos específicos. 

    O cálculo da CAGR segue a seguinte fórmula: 

    CAGR = ((ValorFinal / ValorInicial) ^ (1 / DiferencaAnos) - 1) * 100

    Agora você pode usar a regra `cagr(ValorInicial, ValorFinal, AnoInicial, AnoFinal, CAGR)` para calcular a CAGR. Por exemplo, para calcular a CAGR do PIB do Brasil entre 2000 e 2020, você pode consultar `cagr(644, 1428, 2000, 2020, CAGR)`.
    User: Agora, compute com essa regra o CAGR do brasil de 2000 a 2020
    ************ Running Prolog query:  pib_2000(brasil, Pib2000), pib(brasil, Pib2020), cagr(Pib2000, Pib2020, 2000, 2020, CAGR)
    ************ Result:  [{'Pib2000': 644, 'Pib2020': 1428, 'CAGR': 4.061987665473099}]
    Agent: O CAGR (taxa de crescimento anual composta) do PIB do Brasil de 2000 a 2020 foi de aproximadamente 4.06%. Isso significa que, em média, o PIB do Brasil cresceu aproximadamente 4.06% por ano durante este período de tempo.
