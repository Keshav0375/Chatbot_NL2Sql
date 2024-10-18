import streamlit as st
st.set_page_config(layout="wide",page_title="DataDialect: Bridging Databases and users")
from streamlit_option_menu import option_menu
from langchain_utils_datadialect import invoke_chain_data_dialect
import os
from examples import get_example_selector

with st.sidebar:
    selected_tab = option_menu(None, ["Home", "Add Environment Variables", "Connecting to Database", "Add Table Descriptions", "Add Few Shots Example", "Chatbot"],
                            icons=['house', 'cloud-upload', "list-task",'cloud-upload','cloud-upload', 'gear'],
                            menu_icon="cast", default_index=0,)
if "AZURE_API_KEY" not in st.session_state:
    st.session_state["AZURE_API_KEY"] = ""
if "AZURE_ENDPOINT" not in st.session_state:
    st.session_state["AZURE_ENDPOINT"] = ""
if "AZURE_API_VERSION" not in st.session_state:
    st.session_state["AZURE_API_VERSION"] = ""
if "OPENAI_API_KEY" not in st.session_state:
    st.session_state["OPENAI_API_KEY"] = ""
if "LANGCHAIN_API_KEY" not in st.session_state:
    st.session_state["LANGCHAIN_API_KEY"] = ""
if "LANGCHAIN_TRACING_V2" not in st.session_state:
    st.session_state["LANGCHAIN_TRACING_V2"] = ""
if "db_user" not in st.session_state:
    st.session_state["db_user"] = ""
if "db_password" not in st.session_state:
    st.session_state["db_password"] = ""
if "db_host" not in st.session_state:
    st.session_state["db_host"] = ""
if "db_name" not in st.session_state:
    st.session_state["db_name"] = ""

if selected_tab == 'Home':
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap" rel="stylesheet">
        <h1 style='font-family: "Great Vibes", cursive; text-align: center; font-size: 100px;'>
            DataDialect: Bridging Databases and Users
        </h1>
        """, unsafe_allow_html=True)
    st.markdown("""
        <style>
            .description {
                font-family: Georgia, serif;
                text-align: justify;
                padding: 10px;
                font-size: 25px;
            }
        </style>
        """, unsafe_allow_html=True)

    # Define the content of the description paragraph
    description_text = """
        Welcome to DataDialect – a solution designed to make database interaction seamless through natural language.
        This project enables users to connect their databases, provide API keys, define table details, and share 
        example queries. Once set up, you can effortlessly chat with your database, leveraging cutting-edge NLP 
        technology to generate precise SQL queries. DataDialect transforms the way you interact with data, empowering
        you with quick and accurate insights through simple, conversational prompts. It's database querying made intuitive
        and accessible for everyone!
        """

    # Define the image URL
    image_url = "C:/Users/DELL/PycharmProjects/NL2SQL/Chatbot_NL2Sql/Helper_images/chatbot.jpg"

    # Layout the title, description, and image horizontally using columns
    col1, col2 = st.columns([1, 3])

    # Title
    with col1:
        # Image
        st.image(image_url, use_column_width=True)

    # Description paragraph
    with col2:
        st.markdown(f"<p class='description'>{description_text}</p>", unsafe_allow_html=True)

    st.image("C:/Users/DELL/PycharmProjects/NL2SQL/Chatbot_NL2Sql/Helper_images/best_front.png", use_column_width=True)

if selected_tab == "Add Environment Variables":
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
        <h1 style='font-family: "Playfair Display", serif; text-align: center; font-size: 70px;'>
            Add Environment Variables
        </h1>
        """, unsafe_allow_html=True)
    main_text = """
        <p style='font-family: "Merriweather", serif; font-size: 30px; text-align: center; line-height: 1.6;'>
            Welcome to DataDialect's Configuration page! <br>
        </p>
        """

    # Display the enhanced text
    st.markdown(main_text, unsafe_allow_html=True)
    # Define the content of the description paragraph
    description_text = """
        <p style='font-family: "Merriweather", serif; font-size: 20px; text-align: justify; line-height: 1.6;'>
            Here, you'll set up the necessary <strong>environment variables</strong> to ensure smooth operation of your application.
            These variables typically contain sensitive data such as API keys, and other configuration details.
            You have the option to provide either an <strong>OpenAI API Key</strong> or an <strong>Azure API Key</strong>. 
            If both keys are entered, the system will default to using <strong>Azure</strong>.
            <br><br>
            Kindly fill in the required values below to proceed with your configuration:
        </p>
        """
    st.markdown(description_text, unsafe_allow_html=True)
    # Input fields for environment variables

    st.session_state["AZURE_API_KEY"] = st.text_input("Azure API Key", value=st.session_state.get("AZURE_API_KEY", ""),
                                                      type="password")
    st.session_state["AZURE_ENDPOINT"] = st.text_input("Azure OpenAI Endpoint",
                                                       value=st.session_state.get("AZURE_ENDPOINT", ""))
    st.session_state["AZURE_API_VERSION"] = st.text_input("Azure API Version",
                                                          value=st.session_state.get("AZURE_API_VERSION", ""))

    st.session_state["LANGCHAIN_API_KEY"] = st.text_input("LangChain API Key",
                                                          value=st.session_state.get("LANGCHAIN_API_KEY", ""),
                                                          type="password")
    st.session_state["LANGCHAIN_TRACING_V2"] = st.text_input("LangChain Tracing (Optional)",
                                                             value=st.session_state.get("LANGCHAIN_TRACING_V2", ""))

    # Apply button to confirm
    if st.button("Set Environment Variables"):

        st.success("Environment variables set successfully for the session!")



elif selected_tab == "Connecting to Database":
    st.markdown("""
            <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
            <h1 style='font-family: "Playfair Display", serif; text-align: center; font-size: 70px;'>
                Connecting to Database
            </h1>
            """, unsafe_allow_html=True)
    description_text = """
            <p style='font-family: "Merriweather", serif; font-size: 30px; text-align: justify; line-height: 1.6;'>
                To utilize <strong>DataDialect</strong>, you need to establish a connection to your database. 
                Ensure your database server is running and accessible, then configure your database credentials including host, username, password, and database name.
                <br>
                Kindly fill in the required values below to proceed with your configuration:
            </p>
            """

    # Define the image URL
    image_url = "C:/Users/DELL/PycharmProjects/NL2SQL/Chatbot_NL2Sql/Helper_images/contable.jpg"

    # Layout the title, description, and image horizontally using columns
    col1, col2 = st.columns([1, 3])

    # Title
    with col1:
        # Image
        st.image(image_url, use_column_width=True)

    # Description paragraph
    with col2:
        st.markdown(description_text, unsafe_allow_html=True)

    st.session_state["db_user"] = st.text_input("Database User", value=st.session_state.get("db_user", ""))
    st.session_state["db_password"] = st.text_input("Database Password", value=st.session_state.get("db_password", ""),
                                                    type="password")
    st.session_state["db_host"] = st.text_input("Database Host", value=st.session_state.get("db_host", ""))
    st.session_state["db_name"] = st.text_input("Database Name", value=st.session_state.get("db_name", ""))
    if st.button("Set Environment Variables"):

        st.success("Database variables set successfully for the session!")



elif selected_tab == "Add Table Descriptions":
    st.markdown("""
            <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
            <h1 style='font-family: "Playfair Display", serif; text-align: center; font-size: 70px;'>
                Add Table Descriptions
            </h1>
            """, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Get the filename
        filename = "Dynamic_table.csv"
        if os.path.exists(filename):
            os.remove(filename)
            st.warning(f"Existing file {filename} has been deleted.")

        # Save the uploaded file to the same directory as the Streamlit app
        with open(filename, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("File uploaded successfully.")



    st.markdown(
        "<h1 style='font-family: Georgia, serif; font-size: 35px'>Prepare Table Description CSV</h1>",
        unsafe_allow_html=True)
    st.markdown("<h1 style='font-family: Georgia, serif; font-size: 25px;  font-weight: normal;'> Table Name: The name of the database table.</h1>", unsafe_allow_html=True)
    st.markdown(
        "<h1 style='font-family: Georgia, serif; font-size: 25px;  font-weight: normal;'> Description: A brief description or comment for each field, providing additional context or information.</h1>",
        unsafe_allow_html=True)

    st.image("C:/Users/DELL/PycharmProjects/NL2SQL/Chatbot_NL2Sql/Helper_images/sample_csv.jpg", use_column_width=True)


elif selected_tab == "Add Few Shots Example":
    if "personalised_file_uploaded" not in st.session_state:
        st.session_state.personalised_file_uploaded = False
    st.markdown("""
            <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
            <h1 style='font-family: "Playfair Display", serif; text-align: center; font-size: 70px;'>
                Add Few Shots Examples
            </h1>
            """, unsafe_allow_html=True)
    st.markdown(
        "<h1 style='font-family: Georgia, serif; font-size: 25px;  font-weight: normal;'> To provide chatbot with a better understanding of how to use tables, you can include a few sample Python files demonstrating various usage scenarios. Follow the steps below to add these example files:</h1>",
        unsafe_allow_html=True)


    # Display the enhanced text
    uploaded_file = st.file_uploader("Upload Python File", type=["py"])

    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Get the filename
        filename = "personalised_examples.py"
        if os.path.exists(filename):
            os.remove(filename)
            st.warning(f"Existing file {filename} has been deleted.")

        # Save the uploaded file to the same directory as the Streamlit app
        with open(filename, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.session_state.personalised_file_uploaded = True

        st.success("File uploaded successfully.")

    if st.session_state.personalised_file_uploaded:
        try:
            example_selector = get_example_selector(st.session_state.AZURE_API_KEY, st.session_state.AZURE_ENDPOINT, st.session_state.AZURE_API_VERSION, st.session_state.OPENAI_API_KEY)
            st.success("Examples loaded and selector created successfully.")
        except Exception as e:
            print(e)
            st.error(f"Error loading examples or creating selector: {e}")
    else:
        st.warning("Please upload a personalised_example.py file to proceed.")


    st.markdown(
        "<h1 style='font-family: Georgia, serif; font-size: 35px'>Structure of Example Files</h1>",
        unsafe_allow_html=True)

    st.image("C:/Users/DELL/PycharmProjects/NL2SQL/Chatbot_NL2Sql/Helper_images/egfew.png", use_column_width=True)


elif selected_tab == "Chatbot":
    # Chatbot interface

    st.markdown("""
                <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
                <style>
                    /* Style for the chatbot title */
                    h1 {
                        font-family: "Playfair Display", serif;
                        text-align: center;
                        font-size: 70px;
                        color: #4A4A4A; /* Change title color */
                    }
                    /* Style for chat messages */
                    .message {
                        border-radius: 15px; /* Rounded corners for messages */
                        padding: 10px; /* Padding for messages */
                        margin: 5px 0; /* Spacing between messages */
                        max-width: 80%; /* Limit the width of messages */
                        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Shadow for depth */
                    }
                    /* User message styling */
                    .message.user {
                        background-color: #DCF8C6; /* Light green background for user messages */
                        align-self: flex-end; /* Align user messages to the right */
                    }
                    /* Assistant message styling */
                    .message.assistant {
                        background-color: #E8E8E8; /* Light gray background for assistant messages */
                        align-self: flex-start; /* Align assistant messages to the left */
                    }
                    /* Chat input styling */
                    .chat-input {
                        border: 2px solid #4A4A4A; /* Border color for chat input */
                        border-radius: 15px; /* Rounded corners for chat input */
                        padding: 10px; /* Padding for chat input */
                        font-size: 18px; /* Font size for chat input */
                        margin-top: 20px; /* Space above chat input */
                        
                    }
                </style>
                <h1>DataDialect Chatbot</h1>
                """, unsafe_allow_html=True)
    # Set a default model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(f"<div class='message {message['role']}'> {message['content']} </div>", unsafe_allow_html=True)

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(f"<div class='message user'> {prompt} </div>", unsafe_allow_html=True)

        # Display assistant response in chat message container
        with st.spinner("Generating response..."):
            with st.chat_message("assistant"):
                response = invoke_chain_data_dialect(prompt, st.session_state.messages, st.session_state.AZURE_API_KEY, st.session_state.AZURE_ENDPOINT, st.session_state.AZURE_API_VERSION, st.session_state.OPENAI_API_KEY, st.session_state.db_user, st.session_state.db_password, st.session_state.db_host, st.session_state.db_name)
                st.markdown(f"<div class='message assistant'> {response} </div>", unsafe_allow_html=True)

        st.session_state.messages.append({"role": "assistant", "content": response})
