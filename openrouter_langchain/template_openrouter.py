"""
Template – Chat de terminal com OpenRouter
IA aplicada à Saúde – Sistemas de Informação

Como usar:
  1. Siga o Tutorial 1 (ambiente virtual, .env com OPENROUTER_API_KEY).
  2. Procure os comentários "TODO (aluno)" e complete cada um.
  3. Execute:  python template_openrouter.py

Regra de ouro: use apenas casos FICTÍCIOS. Nunca envie dados reais de pacientes.
"""

import os

from dotenv import load_dotenv
from openai import APIError, AuthenticationError, OpenAI, RateLimitError

# ---------------------------------------------------------------------------
# 1) CONFIGURAÇÃO
# ---------------------------------------------------------------------------
load_dotenv()

BASE_URL = "https://openrouter.ai/api/v1"
MODELO = os.getenv("MODELO", "openai/gpt-4o-mini")

# TODO (aluno) 1: escreva o prompt de sistema do SEU assistente.
# Defina: quem ele é, para quem responde, o que NÃO deve fazer (diagnosticar,
# prescrever) e como deve agir diante de sinais de alerta.
SISTEMA = (
    "Você é um assistente educacional de saúde digital. "
    "Responda em português, de forma clara e breve. "
    "Você não faz diagnósticos nem indica tratamentos."
)

# TODO (aluno) 2: ajuste os parâmetros e observe o efeito nas respostas.
TEMPERATURA = 0.2
MAX_TOKENS = 400


# ---------------------------------------------------------------------------
# 2) CLIENTE
# ---------------------------------------------------------------------------
def criar_cliente() -> OpenAI:
    """Valida a chave e cria o cliente apontado para a OpenRouter."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise SystemExit("Defina OPENROUTER_API_KEY no arquivo .env")
    return OpenAI(base_url=BASE_URL, api_key=api_key)


# ---------------------------------------------------------------------------
# 3) CHAMADA AO MODELO
# ---------------------------------------------------------------------------
def perguntar(client: OpenAI, historico: list[dict]) -> str:
    """Envia o histórico ao modelo e devolve o texto da resposta."""
    try:
        resposta = client.chat.completions.create(
            model=MODELO,
            messages=historico,
            temperature=TEMPERATURA,
            max_tokens=MAX_TOKENS,
        )
        return resposta.choices[0].message.content or ""
    except AuthenticationError:
        return "[erro] Chave inválida. Confira o arquivo .env."
    except RateLimitError:
        return "[erro] Limite de uso atingido. Aguarde e tente de novo."
    except APIError as erro:
        return f"[erro] Falha na API: {erro}"


# ---------------------------------------------------------------------------
# 4) PROGRAMA PRINCIPAL
# ---------------------------------------------------------------------------
def main() -> None:
    client = criar_cliente()
    historico = [{"role": "system", "content": SISTEMA}]

    print(f"Modelo: {MODELO}")
    print("Comandos: 'sair' encerra | '/limpar' reinicia a conversa\n")

    while True:
        entrada = input("Você: ").strip()
        if not entrada:
            continue
        if entrada.lower() in ("sair", "exit"):
            break

        # TODO (aluno) 3: implemente o comando "/limpar", que apaga o histórico
        # mantendo apenas a mensagem de sistema.
        if entrada == "/limpar":
            print("(comando ainda não implementado)\n")
            continue

        historico.append({"role": "user", "content": entrada})
        texto = perguntar(client, historico)
        historico.append({"role": "assistant", "content": texto})
        print(f"\nAssistente: {texto}\n")

        # TODO (aluno) 4: salve a conversa em um arquivo "conversa.txt"
        # (uma linha por mensagem) ao final de cada resposta.


if __name__ == "__main__":
    main()
