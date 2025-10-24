RAG 챗봇 (Streamlit · LangChain · FAISS)

## 실행 방법 (로컬)
1) Python 3.10+ 권장, 가상환경 생성 후 활성화
```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .\\.venv\\Scripts\\Activate.ps1
```
2) 의존성 설치
```bash
pip install -r "03. Streamlit/requirements.txt"
```
3) OpenAI API Key 설정
- PowerShell
```bash
$env:OPENAI_API_KEY="sk-..."
```
4) 앱 실행
```bash
streamlit run "03. Streamlit/rag_app.py"
```

## 사용 방법
- 사이드바에서 API Key, 모델, 파라미터 설정
- PDF/TXT 파일 업로드 → "인덱스 생성/갱신" 클릭
- 챗 입력창에 질문 입력 → 근거 문서와 함께 답변 확인

## 배포 (Streamlit Cloud)
1) GitHub 저장소에 본 프로젝트 업로드
2) Streamlit Cloud에서 New app → Repo/Branch 선택
3) App file path: `03. Streamlit/rag_app.py`
4) Secrets 설정: `OPENAI_API_KEY = sk-...`
5) Deploy

## 제출물 패키징
- 소스 코드와 데이터, 보고서를 다음 명명 규칙으로 압축
  - `이름_중간고사_코드.zip`
- 포함 항목
  - `03. Streamlit/rag_app.py`, `03. Streamlit/requirements.txt`
  - `docs/midterm_report_template.md`(완성본 대체)
  - RAG에 사용하는 파일(예시 PDF 등)
  - 배포된 Streamlit 링크(보고서 및 루트 `DEPLOY_LINK.txt`)

## 폴더 구조(주요)
```
03. Streamlit/
  ├─ rag_app.py
  └─ requirements.txt
docs/
  └─ midterm_report_template.md
```





