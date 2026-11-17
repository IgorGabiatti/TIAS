
# Orientações para os tutoriais de OpenRouter e LangChain
# [Github Prof.º Alexandre Zamberlan](https://github.com/alexandrezamberlan)

## Tutoriais

Os tutoriais estão disponíveis em:

    - tutorial_1_openrouter.md com template_openrouter.py, e
    - tutorial_2_langchain.md com template_langchain.py.

### Tutorial 1 (OpenRouter) 
    - 9 passos: ambiente virtual, chave em .env, primeira chamada, prompt de sistema e parâmetros, chat com histórico, streaming, consulta ao catálogo de modelos, comparação entre dois modelos e modelo de reserva (opcional). Traz também o tratamento de erros, uma tabela de problemas comuns e um exercício de aula.

### Tutorial 2 (LangChain)
    - 8 passos: conexão com a OpenRouter, invoke, prompt template e cadeias (prompt | llm | parser), chat com histórico, streaming, saída estruturada com Pydantic e um agente simples com uma ferramenta de cálculo de IMC (opcional). Também tem tabela de problemas e exercício.

Os templates já funcionam como chat ou menu de terminal e trazem comentários TODO (aluno) com as partes a completar.

Todos os exemplos usam casos fictícios, com o aviso de LGPD e de que as respostas não são diagnóstico.

### Atenção:

    - Nomes dos modelos: o padrão openai/gpt-4o-mini e o catálogo mudam com o tempo. O passo 7 do Tutorial 1 ensina  a copiar o nome exato.
    - create_agent e with_structured_output: o primeiro exige LangChain 1.x. Os dois exigem um modelo com suporte a chamada de ferramentas.
    - Escolha de projeto: no LangChain foi usado ChatOpenAI apontando para a OpenRouter, por ser a forma mais simples. Existe também o pacote langchain-openrouter. 
    
    