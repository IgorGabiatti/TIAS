# Tutorial 1 – OpenRouter com Python (terminal)

**IA aplicada à Saúde – Sistemas de Informação (8º semestre)**

Neste tutorial você vai chamar modelos de linguagem pelo terminal usando a **OpenRouter**, um serviço que dá acesso a vários modelos com uma única chave e um único endpoint, compatível com a API da OpenAI. Ao final, você terá um chat de terminal funcionando e um modelo (`template_openrouter.py`) para adaptar ao seu caso.

**Tempo estimado:** 60 a 90 minutos.

---

## Antes de começar

- **Python 3.10 ou superior.** Confira com `python --version` (em alguns sistemas, `python3 --version`).
- **Conta e chave da OpenRouter.** Crie a conta em openrouter.ai e gere uma chave em *Settings → Keys*. A chave começa com `sk-or-`. Se a opção existir na sua conta, defina um **limite de crédito** para a chave.
- **Custos.** Cada chamada consome créditos, conforme o modelo e o tamanho do texto. Alguns modelos têm variante gratuita, identificada por `:free` no nome, com limites de uso. Confira no catálogo.

> **Regra de ouro em saúde:** use apenas **casos fictícios**. Nunca envie dados reais de pacientes (nome, CPF, prontuário, exames) a um serviço externo. Isso é questão de ética e de LGPD. As respostas dos modelos são **material de estudo e não substituem avaliação profissional**.

---

## Passo 1 – Criar a pasta e o ambiente virtual

```bash
mkdir tutorial_openrouter
cd tutorial_openrouter
python -m venv .venv
```

Ative o ambiente:

```bash
# Linux ou macOS
source .venv/bin/activate

# Windows (cmd ou PowerShell)
.venv\Scripts\activate
```

Instale as bibliotecas:

```bash
pip install openai python-dotenv
```

- `openai`: o cliente que vamos apontar para a OpenRouter (ela é compatível com essa biblioteca).
- `python-dotenv`: lê a chave de um arquivo `.env`, para não deixá-la no código.

## Passo 2 – Guardar a chave com segurança

Crie o arquivo `.env` na pasta do projeto:

```
OPENROUTER_API_KEY=sk-or-cole-sua-chave-aqui
MODELO=openai/gpt-4o-mini
```

Crie também o `.gitignore`, para nunca publicar a chave:

```
.env
.venv/
__pycache__/
```

> **Atenção:** se a chave não for informada ao cliente, a biblioteca `openai` procura a variável `OPENAI_API_KEY`. Se houver uma chave antiga da OpenAI no seu computador, ela seria enviada à OpenRouter e daria erro `401`. Por isso, **sempre valide a chave antes de criar o cliente**, como nos exemplos abaixo.

## Passo 3 – Primeira chamada

Crie o arquivo `01_ola.py`:

```python
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise SystemExit("Defina OPENROUTER_API_KEY no arquivo .env")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

resposta = client.chat.completions.create(
    model=os.getenv("MODELO", "openai/gpt-4o-mini"),
    messages=[
        {"role": "user", "content": "Explique em duas frases o que é triagem em saúde."}
    ],
)

print(resposta.choices[0].message.content)
print("Tokens usados:", resposta.usage.total_tokens if resposta.usage else "n/d")
```

Execute:

```bash
python 01_ola.py
```

**O que aconteceu:** só três configurações separam este código de uma chamada direta à OpenAI: a **`base_url`** (endereço da OpenRouter), a **chave** e o **nome do modelo** no formato `empresa/modelo`. O texto da resposta fica em `resposta.choices[0].message.content`.

## Passo 4 – Papel do sistema e parâmetros

Crie `02_sistema.py`. Aqui definimos o comportamento do modelo por meio da mensagem de papel `system` e controlamos a resposta com parâmetros:

```python
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise SystemExit("Defina OPENROUTER_API_KEY no arquivo .env")

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

SISTEMA = (
    "Você é um assistente educacional para estudantes de Sistemas de Informação. "
    "Explique conceitos de saúde digital de forma clara e objetiva, em português. "
    "Você não faz diagnósticos nem indica tratamentos. "
    "Se a pergunta pedir isso, oriente a procurar um profissional de saúde."
)

resposta = client.chat.completions.create(
    model=os.getenv("MODELO", "openai/gpt-4o-mini"),
    messages=[
        {"role": "system", "content": SISTEMA},
        {"role": "user", "content": "O que é um prontuário eletrônico e por que a interoperabilidade importa?"},
    ],
    temperature=0.2,   # menor = respostas mais previsíveis
    max_tokens=300,    # limite de tamanho da resposta
)

print(resposta.choices[0].message.content)
```

Experimente trocar `temperature` (por exemplo, 0.0 e 1.0) e compare as respostas.

## Passo 5 – Chat no terminal com histórico

O modelo **não guarda memória** entre chamadas. Quem mantém a conversa é o seu programa, reenviando o histórico a cada pergunta. Crie `03_chat.py`:

```python
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise SystemExit("Defina OPENROUTER_API_KEY no arquivo .env")

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
MODELO = os.getenv("MODELO", "openai/gpt-4o-mini")

historico = [
    {"role": "system", "content": "Você é um assistente educacional de saúde digital. Responda em português, de forma breve."}
]

print("Chat iniciado. Digite 'sair' para encerrar.\n")
while True:
    pergunta = input("Você: ").strip()
    if pergunta.lower() in ("sair", "exit"):
        break
    if not pergunta:
        continue

    historico.append({"role": "user", "content": pergunta})
    resposta = client.chat.completions.create(model=MODELO, messages=historico)
    texto = resposta.choices[0].message.content

    historico.append({"role": "assistant", "content": texto})
    print(f"\nAssistente: {texto}\n")
```

Teste a memória: pergunte "O que é HL7?" e depois "E o FHIR, como se relaciona com ele?". A segunda pergunta só faz sentido por causa do histórico.

## Passo 6 – Resposta em streaming

Em vez de esperar a resposta inteira, exibimos o texto à medida que ele é gerado. Crie `04_stream.py`:

```python
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise SystemExit("Defina OPENROUTER_API_KEY no arquivo .env")

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

stream = client.chat.completions.create(
    model=os.getenv("MODELO", "openai/gpt-4o-mini"),
    messages=[{"role": "user", "content": "Liste 3 benefícios da telemedicina."}],
    stream=True,
)

for pedaco in stream:
    if pedaco.choices and pedaco.choices[0].delta.content:
        print(pedaco.choices[0].delta.content, end="", flush=True)
print()
```

## Passo 7 – Explorar o catálogo de modelos

Crie `05_modelos.py`. Ele consulta a lista de modelos e filtra por um termo:

```python
import os
import sys
import httpx
from dotenv import load_dotenv

load_dotenv()
termo = sys.argv[1].lower() if len(sys.argv) > 1 else ""

resposta = httpx.get(
    "https://openrouter.ai/api/v1/models",
    headers={"Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY', '')}"},
    timeout=30,
)
resposta.raise_for_status()
modelos = resposta.json()["data"]

encontrados = [m for m in modelos if termo in m["id"].lower()]
print(f"{len(encontrados)} modelo(s) encontrado(s)\n")
for m in encontrados[:20]:
    preco = m.get("pricing", {}).get("prompt", "n/d")
    print(f"{m['id']:<55} preço por token de entrada: {preco}")
```

Execute, por exemplo:

```bash
python 05_modelos.py gemini
python 05_modelos.py free
```

Use esta lista para escolher os modelos dos próximos passos. O nome exato (o *slug*) precisa ser copiado como aparece aqui, e o catálogo muda com o tempo.

## Passo 8 – Comparar dois modelos

Acrescente no `.env` dois modelos escolhidos no passo anterior:

```
MODELO_A=copie-o-slug-do-modelo-A
MODELO_B=copie-o-slug-do-modelo-B
```

Crie `06_comparar.py`:

```python
import os
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
modelos = [os.getenv("MODELO_A"), os.getenv("MODELO_B")]
if not api_key or not all(modelos):
    raise SystemExit("Defina OPENROUTER_API_KEY, MODELO_A e MODELO_B no arquivo .env")

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

PERGUNTA = "Em até 5 linhas, explique o que é a LGPD e por que ela importa para sistemas de saúde."

for modelo in modelos:
    inicio = time.perf_counter()
    resposta = client.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": PERGUNTA}],
        temperature=0.2,
    )
    duracao = time.perf_counter() - inicio
    tokens = resposta.usage.total_tokens if resposta.usage else "n/d"

    print("=" * 70)
    print(f"Modelo: {modelo} | tempo: {duracao:.1f}s | tokens: {tokens}")
    print("-" * 70)
    print(resposta.choices[0].message.content)
print("=" * 70)
```

Compare clareza, correção e tempo. Qual modelo você usaria em um sistema real e por quê?

## Passo 9 (opcional) – Modelo de reserva (fallback)

A OpenRouter aceita uma lista de modelos de reserva: se o primeiro falhar, tenta os seguintes. Com a biblioteca `openai`, esse campo extra vai em `extra_body`:

```python
resposta = client.chat.completions.create(
    model=os.getenv("MODELO_A"),
    extra_body={"models": [os.getenv("MODELO_B")]},
    messages=[{"role": "user", "content": "Defina interoperabilidade em saúde."}],
)
print("Respondeu:", resposta.model)   # mostra qual modelo atendeu de fato
print(resposta.choices[0].message.content)
```

## Tratando erros

Em um programa real, trate as falhas mais comuns:

```python
from openai import APIError, AuthenticationError, RateLimitError

try:
    resposta = client.chat.completions.create(model=MODELO, messages=historico)
except AuthenticationError:
    print("Chave inválida. Confira o OPENROUTER_API_KEY no arquivo .env.")
except RateLimitError:
    print("Limite de uso atingido. Aguarde um pouco e tente de novo.")
except APIError as erro:
    print(f"Erro na API: {erro}")
```

## Problemas comuns

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| `401 Unauthorized` | Chave errada ou ausente. Uma `OPENAI_API_KEY` antiga pode ter sido usada no lugar | Confira o `.env`, valide a chave no código e reinicie o terminal |
| "Model not found" ou erro de modelo | Nome (slug) incorreto ou modelo fora do ar | Rode `05_modelos.py` e copie o nome exato |
| `429` | Muitas chamadas em pouco tempo, ou limite do modelo gratuito | Aguarde, ou use outro modelo |
| Erro de crédito (geralmente `402`) | Saldo insuficiente | Verifique os créditos na conta |
| `ModuleNotFoundError` | Ambiente virtual não ativado ou biblioteca não instalada | Ative o `.venv` e rode `pip install openai python-dotenv` |

## Exercício de aula

Use apenas o caso fictício abaixo.

> *Paciente fictícia, 34 anos, com dor de cabeça há três dias, sem febre, que relata dormir pouco e passar muitas horas no computador.*

1. Adapte o `template_openrouter.py` para um **assistente de orientação educacional** com um *prompt* de sistema escrito por você, que não faça diagnóstico e recomende procurar um profissional quando houver sinais de alerta.
2. Envie o caso fictício a **dois modelos diferentes** e compare as respostas.
3. Responda em um parágrafo: em que aspectos as respostas divergiram e que riscos isso traria em um sistema real de saúde?

## Próximo passo

No **Tutorial 2** você vai usar o **LangChain** sobre a mesma OpenRouter, para montar *prompts* reutilizáveis, encadear etapas, extrair dados estruturados e criar um agente simples.
