from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate

def generate_code(llm_params: dict[str, str | list]):
  llm = GoogleGenerativeAI(model="gemini-pro")

  prompt = PromptTemplate.from_template("You are an expert in Python and can solve all problems with it, taking an input and printing an output. I will give you a problem that has to be solved with Python code, and you should or not use functions based on the problem statement and the rules, you MUST follow them strictily. I will also give, as an example, inputs and the expected outputs as a Python tuple, the inputs and outputs will match if their position in the their tuples are equal. You also need to verify the type (int, float, str...) of the inputs and outputs and implement it in the code. You need to write and test the code until it solves the problem. When you find the answer, return it without syntax highlighting. Besides that, DON'T put any text inside the \"input()\" function, DON'T unpack an input into multiple variables in a single line, instead, create one variable for each input that I will provide, also pay attention to the number of decimal places of the output and round the numbers using the \"round()\" function to fit it if needed. The rules you MUST follow are {rules}. The problem statement is {problem}. The inputs are: {inputs}. The outputs are: {outputs}. Use loops and do not use lists.")

  model = prompt | llm

  code = model.invoke(llm_params)

  code_file_lines = code.split("\n")

  if len(code_file_lines) > 0:
    if code_file_lines[0] == "```python" or code_file_lines[-1] == "```":
      del code_file_lines[0]
      del code_file_lines[-1]

  code_formatted = "\n".join(code_file_lines)

  return code_formatted