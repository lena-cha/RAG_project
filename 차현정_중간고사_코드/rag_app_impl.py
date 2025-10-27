import os
import io
from typing import List, Tuple
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from pdfminer.high_level import extract_text

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS


# ----------------------------
# Page & Theme
# ----------------------------
st.set_page_config(
    page_title="AI in South Korea 🇰🇷 OpenAI’s Economic Blueprint RAG Chat-bot",
    page_icon="📌",
    layout="wide",
)

st.markdown(
    """
<style>
  .main { background: #f6fbf9; }
  .app-title {
    background: linear-gradient(90deg, #00704a, #2d8659);
    color: white; padding: 16px 24px; border-radius: 10px; font-weight: 700;
    display:flex; align-items:center; gap:10px; margin-bottom:16px;
  }
  .pill { display:inline-block; padding:2px 8px; border-radius:999px; background:#e8f5f0; color:#00704a; font-size:12px; margin-left:8px;}
  .card { background:white; padding:16px; border-radius:12px; border-left:4px solid #00704a; box-shadow:0 2px 6px rgba(0,0,0,0.06); color:#00704a; }
  .hint { color:#2d8659; font-size:13px; }
  .footer { text-align:center; color:#2d8659; margin-top:24px; }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="app-title">
  <span style="font-size:26px">[AI in South Korea] OpenAI’s Economic Blueprint RAG Chat-bot</span>
  <span class="pill">LangChain · FAISS · OpenAI</span>
</div>
""",
    unsafe_allow_html=True,
)


# ----------------------------
# Helpers
# ----------------------------
def load_api_key() -> str:
    load_dotenv(override=False)
    api_key = os.getenv("OPENAI_API_KEY", "")
    if "openai_api_key" in st.session_state and st.session_state.openai_api_key:
        api_key = st.session_state.openai_api_key
    return api_key


def load_deploy_link() -> str:
    """Load deployed app URL from env or DEPLOY_LINK.txt at repo root."""
    link = os.getenv("STREAMLIT_DEPLOY_URL") or os.getenv("DEPLOY_URL") or ""
    if link:
        return link.strip()
    try:
        path = Path(__file__).resolve().parent.parent / "DEPLOY_LINK.txt"
        if path.exists():
            content = path.read_text(encoding="utf-8").strip()
            return content
    except Exception:
        pass
    return ""


def read_uploaded_file(file) -> Tuple[str, str]:
    """
    Returns (text, source_name)
    Supports PDF and TXT.
    """
    filename = file.name
    name_lower = filename.lower()
    raw_bytes = file.read()

    if name_lower.endswith(".pdf"):
        try:
            text = extract_text(io.BytesIO(raw_bytes))
        except Exception as e:
            raise RuntimeError(f"PDF 파싱 실패: {e}")
    elif name_lower.endswith(".txt"):
        try:
            text = raw_bytes.decode("utf-8", errors="ignore")
        except Exception:
            text = raw_bytes.decode("cp949", errors="ignore")
    else:
        raise RuntimeError("지원하지 않는 파일 형식입니다. PDF 또는 TXT만 업로드하세요.")

    text = text.strip()
    if not text:
        raise RuntimeError("파일에서 텍스트를 추출하지 못했습니다.")
    return text, filename


def chunk_documents(texts_with_sources: List[Tuple[str, str]], chunk_size: int, chunk_overlap: int) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
    )
    docs: List[Document] = []
    for text, source in texts_with_sources:
        for chunk in splitter.split_text(text):
            docs.append(Document(page_content=chunk, metadata={"source": source}))
    return docs


def build_vectorstore(docs: List[Document], api_key: str) -> FAISS:
    embeddings = OpenAIEmbeddings(api_key=api_key)
    vs = FAISS.from_documents(docs, embeddings)
    return vs


def format_context(docs: List[Document]) -> str:
    blocks = []
    for i, d in enumerate(docs, start=1):
        src = d.metadata.get("source", "unknown")
        blocks.append(f"[문서 {i}] (출처: {src})\n{d.page_content}")
    return "\n\n".join(blocks)


def generate_answer(query: str, retrieved_docs: List[Document], api_key: str, model: str, temperature: float) -> str:
    context_text = format_context(retrieved_docs)
    system_prompt = (
        "당신은 업로드된 문서를 바탕으로 정확하고 간결하게 답변하는 RAG 전문가입니다. "
        "다음 규칙을 따르세요: 1) 문서 내용에서 근거를 찾아 요약하여 답변, 2) 모르면 모른다고 말하기, "
        "3) 필요하면 관련 근거를 bullet로 인용(파일명 포함), 4) 허구 정보 금지."
    )

    user_prompt = (
        "질문:\n" + query + "\n\n" +
        "다음은 검색된 관련 문서 내용입니다. 이를 바탕으로 답변하세요:\n\n" + context_text
    )

    llm = ChatOpenAI(model=model, temperature=temperature, api_key=api_key)
    res = llm.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ])
    return res.content if hasattr(res, "content") else str(res)


# ----------------------------
# Sidebar Controls
# ----------------------------
with st.sidebar:
    st.markdown("### ⚙️ 설정")
    api_key_input = st.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="sk-...",
        help="환경변수 OPENAI_API_KEY 또는 여기 입력 (저장 안 됨)",
    )
    if api_key_input:
        st.session_state.openai_api_key = api_key_input

    model = st.selectbox("모델", ["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini"], index=0)
    temperature = st.slider("창의성 (temperature)", 0.0, 1.0, 0.2, 0.1)
    chunk_size = st.slider("청크 크기", 200, 2000, 800, 50)
    chunk_overlap = st.slider("청크 중첩", 0, 400, 120, 10)
    top_k = st.slider("검색 문서 수 (k)", 1, 10, 4, 1)

    st.markdown("---")
    clear_btn = st.button("🗑️ 인덱스/대화 초기화")


# ----------------------------
# Session State
# ----------------------------
if clear_btn:
    for key in ["vectorstore", "docs_info", "messages"]:
        if key in st.session_state:
            del st.session_state[key]

if "messages" not in st.session_state:
    st.session_state.messages = []  # list of (role, content)


# ----------------------------
# Upload & Index Build
# ----------------------------
st.markdown("#### 1) 문서 업로드")
st.markdown('<div class="card">PDF 또는 TXT 파일을 업로드하면 벡터 인덱스를 생성합니다.</div>', unsafe_allow_html=True)

uploads = st.file_uploader(
    "파일 업로드 (다중 선택 가능)",
    type=["pdf", "txt"],
    accept_multiple_files=True,
)

api_key = load_api_key()

build_col1, build_col2 = st.columns([1, 3])
with build_col1:
    build_clicked = st.button("🧠 인덱스 생성/갱신")
with build_col2:
    st.markdown("<span class=hint>업로드 후 인덱스 생성 버튼을 눌러주세요.</span>", unsafe_allow_html=True)

if build_clicked:
    if not api_key:
        st.error("OpenAI API Key가 필요합니다. 사이드바에 입력하거나 환경변수 설정하세요.")
    elif not uploads:
        st.error("최소 1개 이상의 파일을 업로드하세요.")
    else:
        try:
            texts_with_sources: List[Tuple[str, str]] = []
            for f in uploads:
                text, src = read_uploaded_file(f)
                texts_with_sources.append((text, src))

            docs = chunk_documents(texts_with_sources, chunk_size, chunk_overlap)
            vs = build_vectorstore(docs, api_key)
            st.session_state.vectorstore = vs
            st.session_state.docs_info = {
                "num_files": len(uploads),
                "num_chunks": len(docs),
                "files": [f.name for f in uploads],
            }
            st.success("인덱스 생성 완료! 이제 질문을 입력하세요.")
        except Exception as e:
            st.error(f"인덱스 생성 실패: {e}")


# ----------------------------
# Index Status
# ----------------------------
st.markdown("#### 2) 인덱스 상태")
status_container = st.container()
with status_container:
    if "vectorstore" in st.session_state:
        info = st.session_state.get("docs_info", {})
        st.markdown(
            f"- 인덱스 상태: ✅ 준비됨  "+
            f"- 파일 수: {info.get('num_files', 0)}  "+
            f"- 청크 수: {info.get('num_chunks', 0)}"
        )
        if info.get("files"):
            st.caption("업로드 파일: " + ", ".join(info["files"]))
    else:
        st.markdown("- 인덱스 상태: ⏳ 아직 생성되지 않음")


# ----------------------------
# Chat Interface
# ----------------------------
st.markdown("#### 3) 챗봇")
chat_container = st.container()

with chat_container:
    for role, content in st.session_state.messages:
        with st.chat_message(role):
            st.markdown(content)

    user_input = st.chat_input("업로드한 문서에 대해 질문하세요…")

    if user_input:
        if "vectorstore" not in st.session_state:
            st.error("먼저 파일을 업로드하고 인덱스를 생성하세요.")
        elif not api_key:
            st.error("OpenAI API Key가 필요합니다.")
        else:
            st.session_state.messages.append(("user", user_input))
            with st.chat_message("user"):
                st.markdown(user_input)

            try:
                retriever = st.session_state.vectorstore.as_retriever(search_kwargs={"k": top_k})
                # LangChain retrievers use .invoke() in recent versions
                retrieved_docs: List[Document] = retriever.invoke(user_input)

                with st.spinner("답변 생성 중…"):
                    answer = generate_answer(user_input, retrieved_docs, api_key, model, temperature)

                with st.chat_message("assistant"):
                    st.markdown(answer)
                    with st.expander("참조 문서 보기"):
                        for i, d in enumerate(retrieved_docs, start=1):
                            src = d.metadata.get("source", "unknown")
                            st.markdown(f"**문서 {i}** · {src}")
                            st.write(d.page_content[:800] + ("…" if len(d.page_content) > 800 else ""))

                st.session_state.messages.append(("assistant", answer))
            except Exception as e:
                err_msg = f"오류가 발생했습니다: {e}"
                with st.chat_message("assistant"):
                    st.error(err_msg)
                st.session_state.messages.append(("assistant", err_msg))


st.markdown("---")
st.markdown(
    "<div class=footer>© RAG Chatbot Demo · Streamlit · LangChain · FAISS</div>",
    unsafe_allow_html=True,
)


