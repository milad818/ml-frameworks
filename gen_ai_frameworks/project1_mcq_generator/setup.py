
from setuptools import find_packages, setup

# The setup() function is used to define the metadata and dependencies of a Python package.

setup(
    name= "mcq_generator",
    version="0.0.1",
    author="Milad Zakhireh",
    author_email="eng.zakhireh@gmail.com",
    install_requires=["openai","langchain", "streamlit", "python-dotenv", "PyPDF2"],
    packages=find_packages()
)

