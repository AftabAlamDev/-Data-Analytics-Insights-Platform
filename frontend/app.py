import os
os.environ["OBJC_DISABLE_INITIALIZE_FORK_SAFETY"] = "YES"

import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_groq import ChatGroq
import os

st.set_page_config(page_title="Data Analytics & Chatbot", layout="wide", page_icon="📊")

st.title("📊 Data Analytics & Insights Platform")

# Sidebar for configuration and upload
with st.sidebar:
    st.header("⚙️ Configuration")
    groq_api_key = st.text_input("Groq API Key", type="password", help="Get your API key from https://console.groq.com/")
    
    st.header("📂 Data Upload")
    uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        # Fix for Streamlit PyArrow serialization issues on mixed type or object columns
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str)
            
        st.sidebar.success("File uploaded successfully!")
        
        # Create Tabs for EDA and Chatbot
        tab1, tab2 = st.tabs(["📈 Exploratory Data Analysis (EDA)", "💬 Chat with Data"])
        
        with tab1:
            st.header("Exploratory Data Analysis")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Rows", f"{df.shape[0]:,}")
            with col2:
                st.metric("Total Columns", f"{df.shape[1]:,}")
            with col3:
                st.metric("Missing Values", f"{df.isna().sum().sum():,}")
                
            st.subheader("Data Preview")
            st.dataframe(df.head(), use_container_width=True)
            
            st.subheader("Summary Statistics")
            st.dataframe(df.describe(include='all'), use_container_width=True)
            
            col_types, col_missing = st.columns(2)
            with col_types:
                st.subheader("Column Types")
                st.dataframe(df.dtypes.astype(str).reset_index().rename(columns={"index": "Column", 0: "Type"}), use_container_width=True, hide_index=True)
            
            with col_missing:
                st.subheader("Missing Values")
                missing_df = df.isna().sum().reset_index()
                missing_df.columns = ["Column", "Missing Count"]
                st.dataframe(missing_df[missing_df["Missing Count"] > 0], use_container_width=True, hide_index=True)
            
            st.subheader("Data Visualizations")
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
            if len(numeric_cols) > 0:
                selected_col = st.selectbox("Select a numeric column to visualize its distribution", numeric_cols)
                if selected_col:
                    fig, ax = plt.subplots(figsize=(10, 4))
                    sns.histplot(df[selected_col], kde=True, ax=ax, color='skyblue')
                    plt.title(f"Distribution of {selected_col}")
                    st.pyplot(fig)
            else:
                st.info("No numeric columns available for visualization.")
                
        with tab2:
            st.header("Chat with your Dataset")
            st.markdown("Ask anything about your dataset, and the AI agent will write and run Pandas code to find the answer!")
            
            if not groq_api_key:
                st.warning("⚠️ Please enter your Groq API Key in the sidebar to use the chatbot feature.")
            else:
                # Initialize chat history
                if "messages" not in st.session_state:
                    st.session_state.messages = []

                # Display chat messages from history on app rerun
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

                # React to user input
                if prompt := st.chat_input("E.g., What is the average of the sales column?"):
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    with st.chat_message("user"):
                        st.markdown(prompt)

                    with st.chat_message("assistant"):
                        try:
                            # Initialize LLM
                            llm = ChatGroq(
                                groq_api_key=groq_api_key,
                                model_name="llama-3.1-8b-instant", 
                                temperature=0
                            )
                            # Create Pandas Agent
                            agent = create_pandas_dataframe_agent(
                                llm, 
                                df, 
                                verbose=True,
                                allow_dangerous_code=True,
                                max_iterations=15,
                                handle_parsing_errors=True
                            )
                            
                            with st.spinner("Analyzing data to find the answer..."):
                                # Ensure we pass string input explicitly
                                response = agent.invoke(prompt)
                                response_text = response.get("output", str(response))
                                st.markdown(response_text)
                                st.session_state.messages.append({"role": "assistant", "content": response_text})
                        except Exception as e:
                            st.error(f"Agent encountered an error: {str(e)}")

    except Exception as e:
        st.error(f"An error occurred while processing the file: {str(e)}")
else:
    st.info("👋 Welcome! Please upload a dataset from the sidebar to get started.")
