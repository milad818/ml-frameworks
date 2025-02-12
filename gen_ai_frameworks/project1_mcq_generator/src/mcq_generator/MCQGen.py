import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv

from src.mcq_generator.utils import read_file, get_table_data
from src.mcq_generator.logger import logging

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain


# fetch and load the environment variables via .env file
load_dotenv()

# access the variables
key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(openai_api_key=key, model_name="gpt-3.5-turbo", temperature=0.7)

# input prompt template
quiz_prompt_template = """
Input Text: {text}
Given the piece of text above, I would like to ask you to create a quiz of {number} mutiple-choice \
questions for {area} participants. It is necessary that the questions are suitable for {level} level \
and not repeated. It is also important that the response is as in JSON format below.
### JSON RESPONSE
{response_json}
"""

qgen_prompt = PromptTemplate(
    input_variables=["text", "area", "number", "level", "response_json"],
    template=quiz_prompt_template
)

quiz_chain=LLMChain(llm=llm,
                    prompt=qgen_prompt,
                    output_key="quiz",
                    verbose=True)


eval_prompt_template = """
Now as a professional or a grammarian, given the multiple-choice quiz for {area} participants, evaluate the quiz \
and provide a thorough analysis of it. Be aware that you can only use 45 words maximum. If necessary, \
update the quiz questions which need to be changed so that it fits student's capabilities.
QUIZ:
{quiz}

"""

qeval_prompt = PromptTemplate(
    input_variables=["area", "quiz"],
    template=eval_prompt_template
)

eval_chain = LLMChain(llm=llm,
                      prompt=qeval_prompt,
                      output_key="evaluation",
                      verbose=True)


gen_eval_chain=SequentialChain(
    chains=[quiz_chain, eval_chain],
    input_variables=["text", "number", "area", "level", "response_json"],
    output_variables=["quiz", "evaluation"],
    verbose=True
)