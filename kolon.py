import streamlit as st
from langchain_core.messages.chat import ChatMessage
from langchain_openai import ChatOpenAI
from langchain_teddynote.prompts import load_prompt
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os, time

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_teddynote import logging
from kolon_retriever import create_retriever
from kolon_sidebar import sidebar

total_start_time = time.time();  start_time = time.time()

st.set_page_config(page_title = "코오롱", page_icon = "📚", layout = "wide", initial_sidebar_state="expanded", )

# API KEY 정보로드
load_dotenv()
logging.langsmith('[Project] PDF-RAG')

# 캐시 디렉토리 생성
if not os.path.exists('.cache'):
    os.mkdir('.cache')
# 파일 업르도 전용 폴더
if not os.path.exists('.cache/files'):
    os.mkdir('.cache/files')
if not os.path.exists('.cache/embeddings'):
    os.mkdir('.cache/embeddings')

st.write('## :orange[[PDF 입찰공고문 정보 추출]]')

# 대화기록을 저장하기 위한 용도로 생성
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'chain' not in st.session_state:
    st.session_state['chain'] = None

clear_btn, uploaded_file, threshold, search_k, selected_model = sidebar()
    
# 이전 대화를 출력
def print_messages():
    for chat_message in st.session_state['messages']:
        st.chat_message(chat_message.role).write(chat_message.content)

# 새로운 메시지 추가
def add_message(role, message):
    st.session_state['messages'].append(ChatMessage(role=role, content=message))


# 파일을 캐시 저장 (시간이 오래 걸리는 작업을 처리할 예정)
@st.cache_resource(show_spinner='업로드한 파일을 처리 중입니다...')
def embed_file(file):
    if isinstance(file, str):  # 기본 파일 경로
        file_path = file
    else:  # 업로드된 파일
        file_content = file.read()
        file_path = f'./.cache/files/{file.name}'
        with open(file_path, 'wb') as f:
            f.write(file_content)

    return create_retriever(file_path, search_k)


# 체인 생성
def create_chain(retriever, model_name='gpt-4o-mini'):    
    # 단계 6: 프롬프트 생성(Create Prompt)
    prompt = load_prompt('kolon_rag_eng.yaml', encoding='utf-8')

    # 단계 7: 언어모델(LLM) 생성
    # 모델(LLM) 을 생성합니다.
    # st.sidebar.write(f'model_name: {model_name}')
    llm = ChatOpenAI(model_name=model_name, temperature=0)

    # 단계 8: 체인(Chain) 생성
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain


# 파일이 업로드 되었을 때
if uploaded_file:
    retriever = embed_file(uploaded_file)
    chain = create_chain(retriever, model_name=selected_model)
    st.session_state['chain'] = chain

# 초기화 벼튼을 누르면..
if clear_btn:
    st.session_state['messages'] = []

# 이전 대화 기록 출력
print_messages()


# 사용자 입력
user_input = st.chat_input("질문을 입력하세요")
# 경고 메시지를 띄우기 위한 빈 영역
warning_msg = st.empty()

if user_input:    
    chain = st.session_state['chain']
    if chain is not None:
        st.chat_message('user').write(user_input)

        response = chain.stream(user_input)
        with st.chat_message('assistant'):
            container = st.empty()
            ai_answer = ''
            for token in response:
                ai_answer += token
                container.markdown(ai_answer)

        add_message('user', user_input)
        add_message('assistant', ai_answer)
    else:
        warning_msg.error('파일을 업로드 해주세요.')
