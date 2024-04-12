import streamlit as st
st.set_page_config(layout="wide",page_title="DataDialect: Bridging Databases and users")
from streamlit_option_menu import option_menu
from langchain_utils import invoke_chain


with st.sidebar:
    selected_tab = option_menu(None, ["Home", "Add Environment Variables", "Connecting to Database", "Add Table Descriptions", "Add Few Shots Example", "Chatbot"],
                            icons=['house', 'cloud-upload', "list-task",'cloud-upload','cloud-upload', 'gear'],
                            menu_icon="cast", default_index=0,)

if selected_tab == 'Home':
    st.markdown("<h1 style='font-family: Georgia, serif; text-align: center;'>DataDialect: Bridging Databases and Users</h1>", unsafe_allow_html=True)
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
        DataDialect is a powerful tool designed to bridge the gap between databases and users. 
        With its intuitive interface and robust features, DataDialect allows users to seamlessly 
        interact with and analyze their data, enabling better decision-making and insights.
                   we've journeyed through the process of enhancing NL2SQL models using LangChain,
        showcasing how to transform natural language queries into precise SQL commands. This exploration
        not only highlights the power of LangChain in making database queries more accessible but also 
        underscores the broader impact of integrating advanced NLP techniques for intuitive data interaction.
        """

    # Define the image URL
    image_url = "C:/Users/DELL/PycharmProjects/NL2SQL/chatbot.jpg"

    # Layout the title, description, and image horizontally using columns
    col1, col2 = st.columns([1, 3])

    # Title
    with col1:
        # Image
        st.image(image_url, use_column_width=True)

    # Description paragraph
    with col2:
        st.markdown(f"<p class='description'>{description_text}</p>", unsafe_allow_html=True)

    st.image("C:/Users/DELL/PycharmProjects/NL2SQL/final2.png", use_column_width=True)

if selected_tab == "Add Environment Variables":
    st.markdown("<h1 style='font-family: Georgia, serif; text-align: center;'>Add Environment Variables</h1>", unsafe_allow_html=True)


    # Define the content of the description paragraph
    description_text = """
            To configure your DataDialect application properly, you need to set up environment variables. These variables will contain sensitive information such as database credentials and API keys. Follow the steps below to create a .env file and populate it with the necessary variables:
            """

    # Define the image URL
    image_url = "C:/Users/DELL/PycharmProjects/NL2SQL/env.png"

    # Layout the title, description, and image horizontally using columns

    # st.markdown(f"<p class='description'>{description_text}</p>", unsafe_allow_html=True)
    # st.image(image_url, use_column_width=True)

    st.markdown("<h1 style='font-family: Georgia, serif; font-size: 35px;'>1. Create a .env File</h1>", unsafe_allow_html=True)
    st.subheader("First, create a file named .env in your project directory. This file will store your environment variables securely.")
    st.markdown("<h1 style='font-family: Georgia, serif; font-size: 30px;'>2. Define Database Connection Variables</h1>",
                unsafe_allow_html=True)
    st.subheader("Add the following variables to your .env file to specify the connection details for your database:")
    st.image("C:/Users/DELL/PycharmProjects/NL2SQL/dbname.png", use_column_width=True)
    st.subheader("Replace 'your_database_username', 'your_database_password', 'your_database_host', and 'your_database_name' with your actual database credentials.")
    st.markdown("<h1 style='font-family: Georgia, serif; font-size: 30px;'>3. Generate API Keys</h1>", unsafe_allow_html=True)
    st.subheader("DataDialect relies on external APIs for certain functionalities. You'll need to generate API keys for the following services:")
    st.subheader("OpenAI API Key")
    st.subheader("Visit the OpenAI website to create an account and generate an API key. Once you have your API key, add it to your .env file:")
    st.image("C:/Users/DELL/PycharmProjects/NL2SQL/openai.png", use_column_width=True)
    st.subheader("LangSmith API Key")
    st.subheader("LangSmith provides advanced NLP capabilities for DataDialect. Sign up for an account on the LangSmith website and obtain your API key. Then, add it to your .env file:")
    st.image("C:/Users/DELL/PycharmProjects/NL2SQL/langsmith.png", use_column_width=True)
    st.markdown("<h1 style='font-family: Georgia, serif; font-size: 30px;'>4. Configure Additional Settings</h1>",
                unsafe_allow_html=True)
    st.subheader("You may need to configure additional settings based on your specific requirements. For example, if you're using LangSmith's tracing feature, you can enable it by setting the following variable:")
    st.image("C:/Users/DELL/PycharmProjects/NL2SQL/tracing.png", use_column_width=True)
    st.markdown("<h1 style='font-family: Georgia, serif; font-size: 30px;'>5. Save the .env File</h1>",
                unsafe_allow_html=True)
    st.subheader("Once you've added all the necessary variables to your .env file, save it. Make sure not to share this file publicly or include it in your version control system, as it contains sensitive information.")

elif selected_tab == "Connecting to Database":
    st.markdown("<h1 style='font-family: Georgia, serif; text-align: center;'>Connecting to Database</h1>", unsafe_allow_html=True)
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
    description_text = """
                To utilize the full functionality of DataDialect, you need to establish a connection to your database. Follow the steps below to ensure a successful connection:
                With the environment variables configured, you can now establish a connection to your database using DataDialect. Ensure that your database server is running and accessible from your network.
                Once you've configured the database connection settings, it's essential to test the connection to verify that DataDialect can communicate with your database successfully. Run a test script or use DataDialect's built-in connection testing functionality to confirm that the connection is working as expected.
                """

    # Define the image URL
    image_url = "C:/Users/DELL/PycharmProjects/NL2SQL/contable.jpg"

    # Layout the title, description, and image horizontally using columns
    col1, col2 = st.columns([1, 3])

    # Title
    with col1:
        # Image
        st.image(image_url, use_column_width=True)

    # Description paragraph
    with col2:
        st.markdown(f"<p class='description'>{description_text}</p>", unsafe_allow_html=True)


elif selected_tab == "Add Table Descriptions":
    st.markdown("<h1 style='font-family: Georgia, serif; text-align: center;'>Add Table Description</h1>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Get the filename
        filename = uploaded_file.name

        # Save the uploaded file to the same directory as the Streamlit app
        with open(filename, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("File uploaded successfully.")

    st.markdown(
        "<h1 style='font-family: Georgia, serif; font-size: 35px'> 1. Prepare Table Description CSV</h1>",
        unsafe_allow_html=True)
    st.markdown("<h1 style='font-family: Georgia, serif; font-size: 25px;  font-weight: normal;'> Table Name: The name of the database table.</h1>", unsafe_allow_html=True)
    st.markdown(
        "<h1 style='font-family: Georgia, serif; font-size: 25px;  font-weight: normal;'> Description: A brief description or comment for each field, providing additional context or information.</h1>",
        unsafe_allow_html=True)

    st.markdown(
        "<h1 style='font-family: Georgia, serif; font-size: 35px'>2. Save CSV File</h1>",
        unsafe_allow_html=True)
    st.markdown(
        "<h1 style='font-family: Georgia, serif; font-size: 25px;  font-weight: normal;'> Save the CSV file with an appropriate name, such as table_description.csv, in a location accessible to your DataDialect application.</h1>",
        unsafe_allow_html=True)

    st.markdown(
        "<h1 style='font-family: Georgia, serif; font-size: 35px'> 3. Upload CSV File</h1>",
        unsafe_allow_html=True)
    st.markdown(
        "<h1 style='font-family: Georgia, serif; font-size: 25px;  font-weight: normal;'> Once you've prepared the CSV file, use the file uploader provided in DataDialect to upload the table_description.csv file.</h1>",
        unsafe_allow_html=True)




elif selected_tab == "Add Few Shots Example":
    st.markdown("<h1 style='font-family: Georgia, serif; text-align: center;'>Add Few Shots Examples</h1>", unsafe_allow_html=True)
    st.markdown(
        "<h1 style='font-family: Georgia, serif; font-size: 25px;  font-weight: normal;'> To provide users with a better understanding of how to use DataDialect, you can include a few sample Python files demonstrating various usage scenarios. Follow the steps below to add these example files:</h1>",
        unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Python File", type=["py"])

    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Get the filename
        filename = uploaded_file.name

        # Save the uploaded file to the same directory as the Streamlit app
        with open(filename, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("File uploaded successfully.")

    st.markdown(
        "<h1 style='font-family: Georgia, serif; font-size: 35px'>Structure of Example Files</h1>",
        unsafe_allow_html=True)

    st.image("C:/Users/DELL/PycharmProjects/NL2SQL/egfew.png", use_column_width=True)


elif selected_tab == "Chatbot":
    # Chatbot interface
    st.markdown("<h1 style='font-family: Georgia, serif; text-align: center;'>DataDialect: Bridging Databases and Users</h1>", unsafe_allow_html=True)

    # Set a default model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.spinner("Generating response..."):
            with st.chat_message("assistant"):
                response = invoke_chain(prompt, st.session_state.messages)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
