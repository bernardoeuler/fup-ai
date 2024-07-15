from dotenv import load_dotenv
import streamlit as st
from llm import generate_code

load_dotenv()

def create_input_result(key_id: int):
  if key_id == 0:
    c1, c2 = box.columns(2)
  elif key_id > 0:
    c1, c2, c3 = box.columns([0.46, 0.46, .08], vertical_alignment="bottom")

  input_key = f"input_{key_id}"
  result_key = f"result_{key_id}"
  
  if f"_{input_key}" in st.session_state:
    load_value(input_key)
  
  if f"_{result_key}" in st.session_state:
    load_value(result_key)

  st.session_state["input_fields"][input_key] = c1.text_input("Input:", help="", key=input_key, on_change=store_value, args=[input_key])
  st.session_state["result_fields"][result_key] = c2.text_input("Resultado:", help="", key=result_key, on_change=store_value, args=[result_key])

  if key_id > 0:
    delete_key = f"delete_{key_id}"
    c3.button("❌", key=delete_key, use_container_width=True, on_click=delete_field, args=[key_id])

  if key_id not in st.session_state["fields"]:
    st.session_state["fields"].append(key_id)

  llm_params["inputs"].append(st.session_state["input_fields"][input_key])
  llm_params["outputs"].append(st.session_state["result_fields"][result_key])  

def store_value(key):
  st.session_state[f"_{key}"] = st.session_state[key]

def load_value(key):
  st.session_state[key] = st.session_state[f"_{key}"]

def add_new_row():
  fields = st.session_state["fields"]
  st.session_state["fields"].append(fields[-1] + 1)

def render_inputs_results():
  for key_id in st.session_state["fields"]:
    create_input_result(key_id)

  box.button("Adicionar input", on_click=add_new_row)
  
  box.write("")
  box.write("")

def delete_field(key_id: int):
  st.session_state["input_result_rows"] -= 1

  del st.session_state["input_fields"][f"input_{key_id}"]
  del st.session_state["result_fields"][f"result_{key_id}"]

  if key_id in st.session_state["fields"]:
    index = st.session_state["fields"].index(key_id)
    del st.session_state["fields"][index]
  
def render_code(code: str):
  st.write("#### Código gerado com sucesso!")

  with st.container():
    st.code(code)

    st.write("")

    file_name = st.text_input("Nome do arquivo:", key="file_name").strip()

    if file_name == "":
      file_name = "codigo.py"

    if not file_name.endswith(".py"):
      file_name += ".py"

    st.write("")

    c1, c2 = st.columns([1, 6])

    c1.download_button("Baixar", data=code, file_name=file_name, mime="text/x-python", type="primary")
    c2.button("Voltar", on_click=reload_page, type="secondary", args=["main"])
  
def reload_page(page: str, data = None):
  if page == "main":
    st.session_state["page"] = "main"
  elif page == "code":
    code = generate_code(llm_params=data)
    st.session_state["page"] = "code"
    st.session_state["code"] = code

if "page" not in st.session_state:
  st.session_state["page"] = "main"

if "code" not in st.session_state:
  st.session_state["code"] = ""

if "input_result_rows" not in st.session_state:
  st.session_state["input_result_rows"] = 1

if "fields" not in st.session_state:
  st.session_state["fields"] = [0]

if "input_fields" not in st.session_state:
  st.session_state["input_fields"] = dict(input_0="")

if "result_fields" not in st.session_state:
  st.session_state["result_fields"] = dict(result_0="")

if st.session_state["page"] == "main":
  if "_rules" in st.session_state:
    load_value("rules")
  
  if "_problem" in st.session_state:
    load_value("problem")

  st.title("FUP AI")
  st.write("Seu assisente nas atividades do portal AME na disciplina de Fundamentos de Programação.")

  box = st.container(border=True)

  llm_params = dict(rules="", problem="", inputs=list(), outputs=list())

  llm_params["rules"] = box.text_area("Regras para a resolução:", height=200, help="", key="rules", on_change=store_value, args=["rules"])
  llm_params["problem"] = box.text_area("Enunciado:", height=100, help="", key="problem", on_change=store_value, args=["problem"])

  render_inputs_results()
  print("Estado input:", st.session_state["input_fields"])
  print("Estado result:", st.session_state["result_fields"])

  box.button("Gerar código", type="primary", on_click=reload_page, args=["code", llm_params])
  
elif st.session_state["page"] == "code":  
  code = st.session_state["code"]
  render_code(code)