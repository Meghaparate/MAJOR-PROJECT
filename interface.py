import streamlit as st
import PyPDF2
import subprocess
from nbconvert import PythonExporter
import nbformat
import os
import pyperclip
from io import BytesIO
import clipboard
text_input=""
text_contents=""
def execute_notebook():
    notebook_path = "C:/Users/prash/Downloads/Summarization using openai(1).ipynb"
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb_contents = nbformat.read(f, as_version=4)
    exporter = PythonExporter()
    source_code, _ = exporter.from_notebook_node(nb_contents)
    # Save the converted Python script
    script_path = 'C:/Users/prash/Downloads/temp_script1.py'
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(source_code)
    # Execute the Python script using subprocess
    result = subprocess.run(['python', script_path], capture_output=True, text=True)
    return result.stdout
        
def read_text_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        st.error(f"File not found at: {file_path}")
        #return ""
    except Exception as e:
        st.error(f"Error reading file: {e}")
        #return ""

col1, col2 = st.columns(2)
with col1:
    st.title("Indian Legal Text Summarization for Long Documents")
    st.write("This Summarizer is trained on 7000+ Supreme Court documents and their abstractive summaries. It utilizes OpenAI's LLM to effectively summarize, capturing the essence of the document without any token limitations.")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    if uploaded_file is not None:
        st.success("PDF file successfully uploaded!")
        file_path = getattr(uploaded_file, "name", None)
        with open("C:/Users/prash/Downloads/temp_file_path.txt", "w") as temp_file:
            temp_file.write(file_path)       
    summarize_button=st.button("Summarize")
    
with col2:
    st.title("Generated Summary")
    if(summarize_button):
        if uploaded_file is None:
            st.error("Upload the file")
        else:
            text_contents=execute_notebook()
    text_input = st.text_area("Summary will be displayed here", value=text_contents, height=400)
    
    st.download_button(
        label="Download",
        data=text_input,
        file_name="downloaded_text.txt",
        key="download_button"
    )
    session_state = st.session_state
    session_state.text_input = text_input
    if 'user_input' not in session_state:
        session_state.user_input = text_input  
    
        
