from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from langchain_openai.embeddings import AzureOpenAIEmbeddings
from langchain_community.vectorstores import Chroma


def get_examples_from_personalised_file():
    try:
        from personalised_examples import examples
        return examples
    except ImportError:
        raise FileNotFoundError("The file 'personalised_example.py' is missing or has no 'examples' variable.")


demo_examples = [
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
        "input": "Retrieve the names of employees who report to employee number 1002.",
        "query": "SELECT firstName, lastName FROM employees WHERE reportsTo = 1002;"
    },
    {
        "input": "List all products with a stock quantity less than 7000.",
        "query": "SELECT productName, quantityInStock FROM products WHERE quantityInStock < 7000;"
    },
    {
     'input':"what is price of `1968 Ford Mustang`",
     "query": "SELECT `buyPrice`, `MSRP` FROM products  WHERE `productName` = '1968 Ford Mustang' LIMIT 1;"
    }
]


def get_example_selector(AZURE_API_KEY, AZURE_ENDPOINT, AZURE_API_VERSION, OPENAI_API_KEY):
    embeddings = None
    if AZURE_API_KEY and AZURE_ENDPOINT:
        embeddings = AzureOpenAIEmbeddings(
            azure_deployment="Text-Analytics",
            api_key=AZURE_API_KEY,
            azure_endpoint=AZURE_ENDPOINT,
            api_version=AZURE_API_VERSION
        )
    elif OPENAI_API_KEY:
        embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

    try:
        examples = get_examples_from_personalised_file()
    except Exception as e:
        examples = demo_examples

    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples,
        embeddings,
        Chroma,
        k=2,
        input_keys=["input"],
    )

    return example_selector