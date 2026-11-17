"""
Template – LangChain + OpenRouter (conversa e extração estruturada)
IA aplicada à Saúde – Sistemas de Informação

Como usar:
  1. Siga o Tutorial 2 (ambiente virtual, .env com OPENROUTER_API_KEY).
  2. Procure os comentários "TODO (aluno)" e complete cada um.
  3. Execute:  python template_langchain.py

Regra de ouro: use apenas casos FICTÍCIOS. Nunca envie dados reais de pacientes.
As respostas são material de estudo e não substituem avaliação profissional.
"""

import os
from typing import List, Literal, Optional

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

load_dotenv()


# ---------------------------------------------------------------------------
# 1) MODELO
# ---------------------------------------------------------------------------
def criar_modelo(temperatura: float = 0.2, max_tokens: int = 500) -> ChatOpenAI:
    """Valida a chave e cria o modelo apontado para a OpenRouter."""
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


# ---------------------------------------------------------------------------
# 2) CONVERSA (prompt + modelo + parser, com histórico)
# ---------------------------------------------------------------------------
# TODO (aluno) 1: escreva o prompt de sistema do SEU assistente.
SISTEMA = (
    "Você é um assistente educacional de saúde digital. "
    "Responda em português, de forma clara e breve. "
    "Você não faz diagnósticos nem indica tratamentos."
)


def criar_cadeia_conversa():
    prompt = ChatPromptTemplate.from_messages([
        ("system", SISTEMA),
        MessagesPlaceholder("historico"),
        ("human", "{pergunta}"),
    ])
    return prompt | criar_modelo() | StrOutputParser()


def conversar() -> None:
    cadeia = criar_cadeia_conversa()
    historico: list = []
    print("Conversa iniciada. Digite 'voltar' para retornar ao menu.\n")

    while True:
        pergunta = input("Você: ").strip()
        if pergunta.lower() == "voltar":
            return
        if not pergunta:
            continue

        resposta = cadeia.invoke({"historico": historico, "pergunta": pergunta})
        historico.append(HumanMessage(content=pergunta))
        historico.append(AIMessage(content=resposta))
        print(f"\nAssistente: {resposta}\n")


# ---------------------------------------------------------------------------
# 3) EXTRAÇÃO ESTRUTURADA
# ---------------------------------------------------------------------------
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
    # TODO (aluno) 2: acrescente o campo "medicacoes_em_uso" (lista de textos)
    # com uma boa descrição. A descrição orienta o modelo na extração.


def extrair(relato: str) -> FichaEducacional:
    llm = criar_modelo(temperatura=0.0)
    extrator = llm.with_structured_output(FichaEducacional, method="function_calling")
    return extrator.invoke(relato)


# TODO (aluno) 3: crie uma segunda cadeia, "resumir_ficha(ficha)", que receba a
# ficha estruturada e gere um resumo em linguagem simples para o estudante,
# terminando com um aviso de que não é diagnóstico.
# Dica: use ChatPromptTemplate com uma variável {ficha_json} e passe
# ficha.model_dump_json() ao invocar a cadeia.


def extrair_dados() -> None:
    print("Cole um relato FICTÍCIO em uma única linha (ou 'voltar'):\n")
    relato = input("Relato: ").strip()
    if not relato or relato.lower() == "voltar":
        return

    try:
        ficha = extrair(relato)
    except Exception as erro:  # modelo sem suporte a tool calling, chave inválida etc.
        print(f"[erro] {erro}")
        return

    print("\nDados extraídos:")
    print(ficha.model_dump_json(indent=2))
    print()


# ---------------------------------------------------------------------------
# 4) PROGRAMA PRINCIPAL
# ---------------------------------------------------------------------------
def main() -> None:
    while True:
        print("=== Menu ===")
        print("1) Conversar")
        print("2) Extrair dados estruturados de um relato fictício")
        print("0) Sair")
        opcao = input("Opção: ").strip()

        if opcao == "1":
            conversar()
        elif opcao == "2":
            extrair_dados()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.\n")


if __name__ == "__main__":
    main()
