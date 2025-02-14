

import os
import PyPDF2
import traceback
import json




def read_file(file):
    if file.name.endwith(".pdf"):
        try:
            pdf_content=PyPDF2.PdfFileReader(file)
            text=""
            for page in pdf_content.pages:
                text=page.extract_text()
            return text
        
        except:
            raise Exception("ERROR! Cannot read the pdf file.")
        
    elif file.name.endwith(".txt"):
        return file.read().decode("utf-8")

    else:
        raise Exception("UNSUPPORTED FILE FORMAT! Only .pdf and .txt files supported.")
    

def get_table_data(qstring):
    try:
        # convert to dictionary
        dict = json.loads(qstring)
        quiz_data_table=[]

        for key, value in dict.items():
            qno = key
            mcq=value["mcq"]
            options=" || ".join(
                [f"{option} -> {option_value}" for option, option_value in value["options"].items()]
            )

            correct_answer = value["correct_answer"]
            quiz_data_table.append({"Question No.": qno, "MCQ": mcq, "Choices": options, "Correct": correct_answer})
        
        return quiz_data_table

    except Exception as exc:
        traceback.print_exception(type(exc), exc, exc.__traceback__)
        return False





