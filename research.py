import os
from dotenv import load_dotenv
from langchain_community.utilities.sql_database import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,FewShotChatMessagePromptTemplate, PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from langchain.memory import ChatMessageHistory

# Load variables from .env file into the environment
load_dotenv()

# Access the environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
langchain_tracing_v2 = os.getenv("LANGCHAIN_TRACING_V2")

db_user = "root"
db_password = "root"
db_host = "localhost"
db_name = "classicmodels"

db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")
# print(db.dialect)
# print(db.get_usable_table_names())
# print(db.table_info)


llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
# generate_query = create_sql_query_chain(llm, db)
# query = generate_query.invoke({"question": "what is price of `1968 Ford Mustang`"})
# "what is price of `1968 Ford Mustang`"
# print(query)


execute_query = QuerySQLDataBaseTool(db=db)
# execute_query.invoke(query)


answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)

rephrase_answer = answer_prompt | llm | StrOutputParser()

# chain = (
#         RunnablePassthrough.assign(query=generate_query).assign(
#             result=itemgetter("query") | execute_query
#         )
#         | rephrase_answer
# )

# print(chain.invoke({"question": "How many orders are there"}))

examples = [
    {
        "input": "List all customers in France with a credit limit over 20,000.",
        "query": "SELECT * FROM customers WHERE country = 'France' AND creditLimit > 20000;"
    },
    {
        "input": "Get the highest payment amount made by any customer.",
        "query": "SELECT MAX(amount) FROM payments;"
    },
    {
        "input": "Show product details for products in the 'Motorcycles' product line.",
        "query": "SELECT * FROM products WHERE productLine = 'Motorcycles';"
    },
    {
        "input": "Retrieve the names of employees who report to employee number 1002",
        "query": "SELECT firstName, lastName FROM employees WHERE reportsTo = 1002;"
    },
    {
        "input": "List all products with a stock quantity less than 7000",
        "query": "SELECT productName, quantityInStock FROM products WHERE quantityInStock < 7000;"
    },
    {
        "input": "what is the price of '1960 Ford Mustang",
        "query": "SELECT 'buyPrice', 'MSRP' FROM products WHERE 'productName' = '1960 Ford Mustang' LIMIT 1;"
    },
]


example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}\nSQLQuery:"),
        ("ai", "{query}"),
    ]
)
# few_shot_prompt = FewShotChatMessagePromptTemplate(
#     example_prompt=example_prompt,
#     examples=examples,
#     # input_variables=["input","top_k"],
#     input_variables=["input"],
# )
# print(few_shot_prompt.format(input1="How many products are there?"))

vectorstore = Chroma()
vectorstore.delete_collection()
example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    OpenAIEmbeddings(),
    vectorstore,
    k=2,
    input_keys=["input"],
)
# print(example_selector.select_examples({"input": "how many employees we have?"}))

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    example_selector=example_selector,
    input_variables=["input", "top_k"],
)
# print(few_shot_prompt.format(input="How many products are there?"))

# final_prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", "You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to run. Unless otherwise specificed.\n\nHere is the relevant table info: {table_info}\n\nBelow are a number of examples of questions and their corresponding SQL queries."),
#         few_shot_prompt,
#         ("human", "{input}"),
#     ]
# )
# print(final_prompt.format(input="How many products are there?", table_info="some table info"))

# generate_query = create_sql_query_chain(llm, db, final_prompt)
# chain = (
#         RunnablePassthrough.assign(query=generate_query).assign(
#             result=itemgetter("query") | execute_query
#         )
#         | rephrase_answer
# )
# print(chain.invoke({"question": "How many csutomers with credit limit more than 50000"}))

from operator import itemgetter
from langchain.chains.openai_tools import create_extraction_chain_pydantic
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List
import pandas as pd


def get_table_details():
    # Read the CSV file into a DataFrame
    table_description = pd.read_csv("Dynamic_table.csv")
    table_docs = []

    # Iterate over the DataFrame rows to create Document objects
    table_details = ""
    for index, row in table_description.iterrows():
        table_details = table_details + "Table Name:" + row['Table'] + "\n" + "Table Description:" + row['Description'] + "\n\n"

    return table_details


class Table(BaseModel):
    """Table in SQL database."""

    name: str = Field(description="Name of table in SQL database.")


# table_names = "\n".join(db.get_usable_table_names())
table_details = get_table_details()
# print(table_details)

table_details_prompt = f"""Return the names of ALL the SQL tables that MIGHT be relevant to the user question. \
The tables are:

{table_details}

Remember to include ALL POTENTIALLY RELEVANT tables, even if you're not sure that they're needed."""

table_chain = create_extraction_chain_pydantic(Table, llm, system_message=table_details_prompt)
# tables = table_chain.invoke({"input": "give me details of customer and their order count"})
# print(tables)


def get_tables(tables: List[Table]) -> List[str]:
    tables = [table.name for table in tables]
    return tables


select_table = {"input": itemgetter("question")} | create_extraction_chain_pydantic(Table, llm, system_message=table_details_prompt) | get_tables
# print(select_table.invoke({"question": "give me details of customer and their order count"}))

# chain = (
#     RunnablePassthrough.assign(table_names_to_use=select_table) |
#     RunnablePassthrough.assign(query=generate_query).assign(
#         result=itemgetter("query") | execute_query
#     ) | rephrase_answer)
# print(chain.invoke({"question": "How many customers with order count more than 5"}))


history = ChatMessageHistory()
final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
         "You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to run. Unless otherwise specificed.\n\nHere is the relevant table info: {table_info}\n\nBelow are a number of examples of questions and their corresponding SQL queries. Those examples are just for referecne and hsould be considered while answering follow up questions"),
        few_shot_prompt,
        MessagesPlaceholder(variable_name="messages"),
        ("human", "{input}"),
    ]
)
# print(final_prompt.format(input="How many products are there?", table_info="some table info", messages=[]))
generate_query = create_sql_query_chain(llm, db, final_prompt)

chain = (
        RunnablePassthrough.assign(table_names_to_use=select_table) |
        RunnablePassthrough.assign(query=generate_query).assign(
            result=itemgetter("query") | execute_query
        )
        | rephrase_answer
)

# question = "How many customers with order count more than 5"
# response = chain.invoke({"question": question, "messages": history.messages})
# print(response)
# history.add_user_message(question)
# history.add_ai_message(response)
#
# response = chain.invoke({"question": "Can you list there names?","messages":history.messages})
# print(response)




