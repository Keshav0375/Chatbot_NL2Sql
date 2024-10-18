from langchain_community.utilities.sql_database import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain.memory import ChatMessageHistory

from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser

from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI

from table_details import table_func as select_table
from prompts import initialize_prompts

import streamlit as st


# @st.cache_resource
def get_chain(AZURE_API_KEY, AZURE_ENDPOINT, AZURE_API_VERSION, OPENAI_API_KEY, db_user, db_password, db_host, db_name):
    print("Creating chain")

    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")
    # llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    if AZURE_API_KEY and AZURE_ENDPOINT and AZURE_API_VERSION:
        llm = AzureChatOpenAI(
            deployment_name="slideoo-chat-1",
            temperature=1,
            max_tokens=4000,
            azure_endpoint=AZURE_ENDPOINT,
            api_key=AZURE_API_KEY,
            api_version=AZURE_API_VERSION,
        )
        print("Using Azure OpenAI")
    elif OPENAI_API_KEY:
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0
        )
        print("Using OpenAI")
    else:
        raise ValueError("No valid API key provided for OpenAI or Azure")
    final_prompt, answer_prompt = initialize_prompts(AZURE_API_KEY, AZURE_ENDPOINT, AZURE_API_VERSION, OPENAI_API_KEY)
    generate_query = create_sql_query_chain(llm, db, final_prompt)
    execute_query = QuerySQLDataBaseTool(db=db)
    rephrase_answer = answer_prompt | llm | StrOutputParser()
    # chain = generate_query | execute_query
    chain = (
        RunnablePassthrough.assign(table_names_to_use=select_table(AZURE_API_KEY, AZURE_ENDPOINT, AZURE_API_VERSION, OPENAI_API_KEY)) |
        RunnablePassthrough.assign(query=generate_query).assign(
            result=itemgetter("query") | execute_query
        )
        | rephrase_answer
    )

    return chain


def create_history(messages):
    history = ChatMessageHistory()
    for message in messages:
        if message["role"] == "user":
            history.add_user_message(message["content"])
        else:
            history.add_ai_message(message["content"])
    return history


def invoke_chain_data_dialect(question,messages, AZURE_API_KEY, AZURE_ENDPOINT, AZURE_API_VERSION, OPENAI_API_KEY, db_user, db_password, db_host, db_name):
    chain = get_chain(AZURE_API_KEY, AZURE_ENDPOINT, AZURE_API_VERSION, OPENAI_API_KEY, db_user, db_password, db_host, db_name)
    history = create_history(messages)
    response = chain.invoke({"question": question, "top_k": 3, "messages": history.messages})
    history.add_user_message(question)
    history.add_ai_message(response)
    return response


