import streamlit as st

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import ChatMessage

from dotenv import load_dotenv
load_dotenv()

# handle streaming conversation
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

# Function to extract text from an PDF file
from pdfminer.high_level import extract_text

def get_pdf_text(filename):
    raw_text = extract_text(filename)
    return raw_text

# document preprocess
def process_uploaded_file(uploaded_file):
    # Load document if file is uploaded
    if uploaded_file is not None:
        # loader - PDF에서 텍스트 추출
        raw_text = get_pdf_text(uploaded_file)

        # splitter - 텍스트를 청크로 분할
        # splitter
        text_splitter = CharacterTextSplitter(
        separator = "\n\n",
       chunk_size = 1000,
       chunk_overlap  = 200,
       length_function = len
        )
        all_splits = text_splitter.create_documents([raw_text])

        print("총 " + str(len(all_splits)) + "개의 passage")
        
        # storage - 벡터 스토어 생성
        vectorstore = FAISS.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())
               
        return vectorstore, raw_text
    return None

# generate response using RAG technic
def generate_response(query_text, vectorstore, callback):

    # retriever - 관련 문서 검색
    docs_list = vectorstore.similarity_search(query_text, k=3)
    docs = ""
    for i, doc in enumerate(docs_list):
        docs += f"'문서{i+1}':{doc.page_content}\n"
        
    # generator - ChatOpenAI 모델 생성
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, streaming=True, callbacks=[callback])
    
    # chaining - 프롬프트와 함께 LLM 호출
    rag_prompt = [
        SystemMessage(
            content="너는 문서에 대해 질의응답을 하는 '문서봇'이야. 주어진 문서를 참고하여 사용자의 질문에 답변을 해줘. 문서에 내용이 정확하게 나와있지 않으면 대답하지 마."
        ),
        HumanMessage(
            content=f"질문:{query_text}\n\n{docs}"
        ),
    ]

    response = llm(rag_prompt)

    return response.content
    


def generate_summarize(raw_text, callback):
    # ChatOpenAI 모델 생성
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0,
        streaming=True,
        callbacks=[callback]
    )
    
    # 요약 프롬프트
    system_message = SystemMessage(content="""당신은 문서 요약 전문가입니다. 
    주어진 문서의 핵심 내용을 간결하고 이해하기 쉽게 요약해주세요.
    중요한 포인트들을 빠뜨리지 않으면서도 핵심만 추려서 설명해주세요.""")
    
    human_message = HumanMessage(content=f"""
    다음 문서를 요약해주세요:
    
    {raw_text[:4000]}  # 토큰 제한을 고려하여 일부만 사용
    
    위 문서의 주요 내용을 한국어로 요약해주세요.
    """)
    
    response = llm([system_message, human_message])
    
    return response.content


# page title
st.set_page_config(page_title='🦜🔗 문서 기반 요약 및 QA 챗봇')
st.title('🦜🔗 문서 기반 요약 및 QA 챗봇')

# file upload
uploaded_file = st.file_uploader('Upload an document', type=['pdf'])

# file upload logic
if uploaded_file:
    vectorstore, raw_text = process_uploaded_file(uploaded_file)
    if vectorstore:
        st.session_state['vectorstore'] = vectorstore
        st.session_state['raw_text'] = raw_text
        
# chatbot greatings
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        ChatMessage(
            role="assistant", content="안녕하세요! 저는 문서에 대한 이해를 도와주는 챗봇입니다. 어떤게 궁금하신가요?"
        )
    ]

# conversation history print 
for msg in st.session_state.messages:
    st.chat_message(msg.role).write(msg.content)
    
# message interaction
if prompt := st.chat_input("'요약'이라고 입력해보세요!"):
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())
        
        if prompt == "요약":
            response = generate_summarize(st.session_state['raw_text'],stream_handler)
            st.session_state["messages"].append(
                ChatMessage(role="assistant", content=response)
            )
        
        else:
            response = generate_response(prompt, st.session_state['vectorstore'], stream_handler)
            st.session_state["messages"].append(
                ChatMessage(role="assistant", content=response)
            )