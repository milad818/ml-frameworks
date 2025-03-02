import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcq_generator.utils import read_file, get_data_table
import streamlit as st
# from langchain.callbacks import get_openai_callback 
from langchain_community.callbacks.manager import get_openai_callback
from src.mcq_generator.MCQGen import gen_eval_chain
from src.mcq_generator.logger import logging



# Load json file
# with open("D:\\Work and Education\\Computer Engineering\\1---gihub\\ml-frameworks\\gen_ai_frameworks\\project1_mcq_generator\\response.json", "r") as file:
with open("response.json", "r") as file:
    RESPONSE_JSON = json.load(file)
    print(RESPONSE_JSON)

# Choose title for the application
st.title("Multiple-Choice Quiz Generator")

# We will have to also create a form 
with st.form("user_inpiuts"):
    # Upload file
    ulfile = st.file_uploader("Upload a file - PDF or Text")    

    # Inputs
    #No. of MCQs
    number = st.number_input("No of MCQs", min_value=3, max_value=50)

    # Topic of the MCQ
    area = st.text_input("Enter Topic", max_chars=20)

    # Level
    level = st.text_input("Difficulty Level of Questions", max_chars=20, placeholder="Intermadiate")

    # Buttons
    button = st.form_submit_button("Create MCQs")

    # It is necessary to check if the button is clicked and all the fields are filled...
    # Therefore, below we validate the inputs in some sense.
    if button and ulfile is not None and number and area and level:
        with st.spinner("loading..."):
            try:
                text=read_file(ulfile)
                # set up token usage tracking in Langchain (i.e., cost of API call)
                with get_openai_callback() as cb:
                    response = gen_eval_chain(
                        {
                        "text": text,
                        "number": number,
                        "area": area,
                        "level": level,
                        "response_json": json.dumps(RESPONSE_JSON)
                        }
                    )

            except Exception as exc:
                traceback.print_exception(type(exc), exc, exc.__traceback__)
                st.error("Error")

            else:
                print(f"Total Tokens: {cb.total_tokens}")
                print(f"Completion Token: {cb.completion_tokens}")
                print(f"Prompt Token: {cb.prompt_tokens}")
                print(f"Total Cost: {cb.total_cost}")
                print(f"Reasoning Error: {cb.reasoning_tokens}")
                # Check if response is of type dict and extract quiz data from the response
                if isinstance(response, dict):
                    # Extract data
                    quiz = response.get("quiz", None)   # If "quiz" does not exist, it assigns None instead of raising a KeyError
                    print("This is quiz:", quiz)
                    if quiz is not None:
                        table_data = get_data_table(quiz)
                        print("This is table data", table_data)
                        # exit()
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index+1
                            st.table(df)
                            # ALSO display the evaluation on the quiz
                            st.text_area(label="Evaluation", value=response["evaluation"])
                        else:
                            st.error("There is error in the data table!")
                
                else:
                    st.write(response)



