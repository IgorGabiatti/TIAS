# Tutorial 2 – LangChain com Python (terminal)

**IA aplicada à Saúde – Sistemas de Informação (8º semestre)**

No Tutorial 1 você chamou os modelos "à mão", pela biblioteca da OpenAI. Agora vai usar o **LangChain**, um framework que oferece peças prontas para montar aplicações com modelos de linguagem: *prompts* reutilizáveis, encadeamento de etapas, saída estruturada e agentes. O modelo continua sendo acessado pela **OpenRouter**, então você reaproveita a mesma chave.

Ao final, você terá cinco programas pequenos e um modelo (`template_langchain.py`) para adaptar ao seu caso.

**Tempo estimado:** 90 a 120 minutos.

**Pré-requisito:** ter feito o Tutorial 1 (conta e chave da OpenRouter, noção de ambiente virtual).

> **Regra de ouro em saúde:** use apenas **casos fictícios**. Nunca envie dados reais de pacientes. As respostas dos modelos são **material de estudo e não substituem avaliação profissional**.

---

## Passo 1 – Ambiente

```bash
mkdir tutorial_langchain
cd tutorial_langchain
python -m venv .venv
```

```bash
# Linux ou macOS
source .venv/bin/activate

# Windows (cmd ou PowerShell)
.venv\Scripts\activate
```

```bash
pip install -U langchain langchain-openai python-dotenv pydantic
```

Confira a versão instalada:

```bash
pip show langchain
```

Este tutorial foi escrito para o **LangChain 1.x**. O framework evolui rápido, então, se algum nome de função mudar na sua versão, consulte a documentação oficial (docs.langchain.com).

Crie o arquivo `.env` (pode ser a mesma chave do Tutorial 1):

```
OPENROUTER_API_KEY=sk-or-cole-sua-chave-aqui
MODELO=openai/gpt-4o-mini
```

E o `.gitignore`:

```
.env
.venv/
__pycache__/
```

## Passo 2 – Conectar o LangChain à OpenRouter

Como a OpenRouter é compatível com a API da OpenAI, usamos a classe `ChatOpenAI` do LangChain apontando para o endereço da OpenRouter. Para tornar o código reutilizável, crie um arquivo `modelo.py`, que será importado pelos demais:

```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


def criar_modelo(temperatura: float = 0.2, max_tokens: int = 500) -> ChatOpenAI:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise SystemExit("Defina OPENROUTER_API_KEY no arquivo .env")

    return ChatOpenAI(
        model=os.getenv("MODELO", "openai/gpt-4o-mini"),
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=temperatura,
        max_tokens=max_tokens,
    )
```

> **Nota:** existe também um pacote específico, o `langchain-openrouter`, com a classe `ChatOpenRouter`, que expõe recursos próprios da OpenRouter (roteamento, metadados). Para a aula, usamos `ChatOpenAI` com `base_url` porque é a forma mais simples e de menor dependência. Se quiser testar o pacote nativo, a documentação do LangChain traz o passo a passo.

## Passo 3 – Primeira chamada com mensagens

Crie `01_invocar.py`:

```python
from langchain_core.messages import HumanMessage, SystemMessage

from modelo import criar_modelo

llm = criar_modelo()

mensagens = [
    SystemMessage(content="Você é um assistente educacional de saúde digital. Responda em português, em até 3 frases."),
    HumanMessage(content="O que é telemedicina?"),
]

resposta = llm.invoke(mensagens)

print(resposta.content)
print("Uso de tokens:", resposta.usage_metadata)
```

```bash
python 01_invocar.py
```

**O que aconteceu:** o método `invoke` envia as mensagens e devolve um objeto `AIMessage`. O texto está em `.content`, e `.usage_metadata` traz os tokens consumidos. Compare com o Tutorial 1: o resultado é o mesmo, mas agora as mensagens são objetos do LangChain, que servem de base para todas as outras peças.

## Passo 4 – Prompt template e cadeia (chain)

Em vez de montar o texto à mão a cada chamada, definimos um **modelo de prompt** com variáveis e o **encadeamos** ao modelo com o operador `|`. Crie `02_cadeia.py`:

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from modelo import criar_modelo

llm = criar_modelo()

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Você é um assistente educacional para estudantes de {curso}. "
     "Explique de forma clara, em português, em no máximo {max_linhas} linhas. "
     "Você não faz diagnósticos."),
    ("human", "{pergunta}"),
])

cadeia = prompt | llm | StrOutputParser()

texto = cadeia.invoke({
    "curso": "Sistemas de Informação",
    "max_linhas": 4,
    "pergunta": "Qual a diferença entre HL7 e FHIR?",
})
print(texto)
```

**Como ler a linha `prompt | llm | StrOutputParser()`:** os dados fluem da esquerda para a direita. O *prompt* preenche as variáveis, o modelo responde e o `StrOutputParser` extrai só o texto. Essa composição é a ideia central do LangChain.

Exercício rápido: reutilize a mesma `cadeia` para duas perguntas diferentes, mudando apenas o dicionário de entrada.

## Passo 5 – Chat com histórico

Aqui o histórico entra no *prompt* por meio de um `MessagesPlaceholder`. Crie `03_chat.py`:

```python
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from modelo import criar_modelo

llm = criar_modelo()

prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente educacional de saúde digital. Responda em português, de forma breve."),
    MessagesPlaceholder("historico"),
    ("human", "{pergunta}"),
])

cadeia = prompt | llm | StrOutputParser()

historico = []
print("Chat iniciado. Digite 'sair' para encerrar.\n")

while True:
    pergunta = input("Você: ").strip()
    if pergunta.lower() in ("sair", "exit"):
        break
    if not pergunta:
        continue

    resposta = cadeia.invoke({"historico": historico, "pergunta": pergunta})

    historico.append(HumanMessage(content=pergunta))
    historico.append(AIMessage(content=resposta))
    print(f"\nAssistente: {resposta}\n")
```

Aqui o histórico é uma lista que **você** mantém, o que deixa o mecanismo explícito. Em aplicações maiores, o LangChain 1.x oferece persistência de conversa por meio do LangGraph, assunto para um próximo estudo.

## Passo 6 – Streaming

Troque `invoke` por `stream` para exibir o texto aos poucos. Crie `04_stream.py`:

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from modelo import criar_modelo

llm = criar_modelo()

prompt = ChatPromptTemplate.from_messages([
    ("system", "Responda em português, de forma didática."),
    ("human", "{pergunta}"),
])
cadeia = prompt | llm | StrOutputParser()

for pedaco in cadeia.stream({"pergunta": "Liste 3 desafios de segurança em prontuários eletrônicos."}):
    print(pedaco, end="", flush=True)
print()
```

## Passo 7 – Saída estruturada (extração de dados)

Esta é uma das funções mais úteis em saúde digital: transformar um **texto livre** em **dados estruturados**, prontos para um banco de dados. Definimos o formato desejado com uma classe Pydantic e pedimos ao modelo que a preencha. Crie `05_estruturado.py`:

```python
from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from modelo import criar_modelo


class FichaEducacional(BaseModel):
    """Dados extraídos de um relato clínico FICTÍCIO, para fins de estudo."""

    idade: Optional[int] = Field(default=None, description="Idade em anos, se citada")
    sexo: Optional[str] = Field(default=None, description="Sexo informado no texto, se citado")
    queixa_principal: str = Field(description="Queixa principal em poucas palavras")
    sintomas: List[str] = Field(default_factory=list, description="Lista de sintomas citados")
    duracao: Optional[str] = Field(default=None, description="Há quanto tempo os sintomas ocorrem")
    sinais_de_alerta: List[str] = Field(default_factory=list, description="Sinais de alerta citados, se houver")
    prioridade_sugerida: Literal["baixa", "media", "alta"] = Field(
        description="Prioridade educacional sugerida para fins didáticos, não clínicos"
    )


llm = criar_modelo(temperatura=0.0)
extrator = llm.with_structured_output(FichaEducacional, method="function_calling")

relato = (
    "Paciente fictícia, 34 anos, sexo feminino, relata dor de cabeça há três dias, "
    "sem febre. Diz dormir pouco e passar muitas horas no computador. "
    "Nega vômitos e alterações visuais."
)

ficha = extrator.invoke(relato)

print(type(ficha).__name__)
print(ficha.model_dump_json(indent=2))
```

**Pontos de atenção:**

- O resultado é um **objeto Python** (`ficha.idade`, `ficha.sintomas`), e não um texto, o que facilita salvar em banco, validar e testar.
- A saída estruturada depende de o modelo escolhido **suportar chamada de ferramentas** (*tool calling*). Se der erro, troque de modelo, escolhendo outro no catálogo da OpenRouter.
- O campo `prioridade_sugerida` é um **exercício didático**. Discuta em aula por que classificar urgência clínica automaticamente exige validação rigorosa e supervisão profissional.

## Passo 8 (opcional) – Um agente simples com ferramenta

Um **agente** é um modelo que decide quando chamar uma função (ferramenta) para obter um resultado confiável, em vez de "adivinhar". Cálculos devem ser feitos por código, não pelo modelo. Crie `06_agente.py`:

```python
from langchain.agents import create_agent
from langchain.tools import tool

from modelo import criar_modelo


@tool
def calcular_imc(peso_kg: float, altura_m: float) -> str:
    """Calcula o IMC (índice de massa corporal) a partir do peso em kg e da altura em metros."""
    imc = peso_kg / (altura_m ** 2)
    if imc < 18.5:
        faixa = "abaixo do peso"
    elif imc < 25:
        faixa = "peso adequado"
    elif imc < 30:
        faixa = "sobrepeso"
    else:
        faixa = "obesidade"
    return f"IMC = {imc:.1f} ({faixa})"


agente = create_agent(
    model=criar_modelo(temperatura=0.0),
    tools=[calcular_imc],
    system_prompt=(
        "Você é um assistente educacional. Para calcular IMC, use sempre a ferramenta. "
        "Explique o resultado em português e lembre que o IMC não substitui avaliação profissional."
    ),
)

resultado = agente.invoke(
    {"messages": [{"role": "user", "content": "Uma pessoa fictícia tem 82 kg e 1,75 m. Qual o IMC?"}]}
)

# Mostra o "passo a passo" do agente: pergunta, chamada da ferramenta, resultado, resposta
for mensagem in resultado["messages"]:
    mensagem.pretty_print()
```

Observe na saída as quatro etapas: a pergunta, a decisão do modelo de chamar `calcular_imc`, o retorno da ferramenta e a resposta final. Esse ciclo é a base dos agentes. Esse exemplo exige o LangChain 1.x (`create_agent`) e um modelo com suporte a *tool calling*.

## Problemas comuns

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| `401` ou erro de autenticação | Chave ausente ou incorreta | Confira o `.env` e reinicie o terminal |
| `ImportError` ao importar `create_agent` ou `tool` | Versão antiga do LangChain | Rode `pip install -U langchain` e confira com `pip show langchain` |
| Erro no `with_structured_output` | O modelo não suporta chamada de ferramentas | Escolha outro modelo no catálogo da OpenRouter |
| Erro de modelo não encontrado | Nome (slug) incorreto | Use o nome exato copiado do catálogo da OpenRouter |
| `KeyError` ao preencher o *prompt* | Variável do `ChatPromptTemplate` ausente no dicionário de entrada | Passe todas as variáveis entre `{}` |

## Exercício de aula

Use apenas o caso fictício abaixo.

> *Paciente fictício, 58 anos, relata falta de ar ao subir escadas há duas semanas e cansaço frequente, sem dor no peito. Faz uso de medicação para pressão há cinco anos.*

1. Adapte o `template_langchain.py`: acrescente à classe `FichaEducacional` o campo `medicacoes_em_uso` e execute a extração no caso acima.
2. Crie uma segunda cadeia que receba a ficha estruturada e gere um **resumo para o estudante**, em linguagem simples, com aviso de que não é diagnóstico.
3. Discuta em um parágrafo: qual a vantagem de usar saída estruturada em vez de texto livre em um sistema de informação em saúde, e que cuidados de validação seriam necessários?
