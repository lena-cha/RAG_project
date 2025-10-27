from pathlib import Path
import shutil

src_app = Path(__file__).resolve().parents[1] / "03. Streamlit" / "rag_app.py"
dst_app = Path(__file__).resolve().parent / "rag_app_impl.py"
if src_app.exists():
    shutil.copyfile(src_app, dst_app)

src_req = Path(__file__).resolve().parents[1] / "03. Streamlit" / "requirements.txt"
dst_req = Path(__file__).resolve().parent / "requirements.txt"
if src_req.exists():
    shutil.copyfile(src_req, dst_req)

src_doc = Path(__file__).resolve().parents[1] / "docs" / "midterm_report_template.md"
dst_doc_dir = Path(__file__).resolve().parent / "docs"
dst_doc_dir.mkdir(parents=True, exist_ok=True)
dst_doc = dst_doc_dir / "midterm_report_template.md"
if src_doc.exists():
    shutil.copyfile(src_doc, dst_doc)

src_link = Path(__file__).resolve().parents[1] / "DEPLOY_LINK.txt"
dst_link = Path(__file__).resolve().parent / "DEPLOY_LINK.txt"
if src_link.exists():
    shutil.copyfile(src_link, dst_link)

print("study 폴더에 제출용 파일이 준비되었습니다. 실행은 'streamlit run rag_app_impl.py' 를 사용하세요.")


