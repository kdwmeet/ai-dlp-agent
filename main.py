import streamlit as st
import tempfile
import os
from langchain_community.document_loaders import PyPDFLoader
from app.dlp_agent import analyze_content

st.set_page_config(page_title="AI DLP Agent", layout="wide")

st.title("AI 기반 기업 정보유출 감시 에이전트")
st.caption("외부로 발송되는 이메일 본문과 첨부파일을 실시간 스캔하여 기밀 유출을 차단합니다.")
st.divider()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("메일 발송 시뮬레이터")
    email_body = st.text_area(
        "이메일 본문",
        height=200,
        placeholder="수신자: 외부업체 (external@vendor.com)\n내용을 입력하세요."
    )

    uploaded_file = st.file_uploader("첨부파일 (PDF 또는 TXT)", type=["pdf","txt"])
    send_btn = st.button("메일 발송 (보안 스캔 수행)", type="primary", width="stretch")

with col2:
    st.subheader("보안 스캔 리포트")
    
    if send_btn:
        if not email_body and not uploaded_file:
            st.warning("발송할 내용이나 첨부파일을 입력해주세요.")

        else:
            with st.spinner("AI 보안 에이전트가 콘텐츠를 스캔 중입니다..."):
                content_to_scan = f"[이메일 본문]\n{email_body}\n\n"

                # 첨부파일이 있을 경우 텍스트 추출하여 합침
                if uploaded_file:
                    suffix = ".pdf" if uploaded_file.name.endswith(".pdf") else ".txt"
                    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name
                    
                    try:
                        if suffix == ".pdf":
                            loader = PyPDFLoader(tmp_path)
                            pages = loader.load()
                            file_text = "\n".join([page.page_content for page in pages[:5]]) # 빠른 검사를 위해 5페이지만
                        else:
                            with open(tmp_path, "r", encoding="utf-8") as f:
                                file_text = f.read()
                        content_to_scan += f"[첨부파일 내용]\n{file_text}"
                    except Exception as e:
                        content_to_scan += f"\n파일 읽기 오류: {str(e)}"
                    finally:
                        os.remove(tmp_path)
                
                # AI 분석 실행
                result = analyze_content(content_to_scan)

                if "error" in result:
                    st.error("보안 분석 중 오류가 발생했습니다.")
                    st.write(result["raw"])
                else:
                    action = result.get("action", "")

                    if action == "BLOCK":
                        st.error("🚫 발송 차단 (BLOCK)")
                    elif action == "WARN":
                        st.warning("⚠️ 발송 경고 (WARN - 부서장 승인 필요)")
                    else:
                        st.success("✅ 발송 승인 (PASS)")
                        
                        st.divider()
                        st.write(f"**탐지된 카테고리:** {result.get('category')}")
                        st.write(f"**탐지된 핵심 내용:** {result.get('detected_content')}")
                        st.info(f"**보안 조치 사유:** {result.get('reason')}")