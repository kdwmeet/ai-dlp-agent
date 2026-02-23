import os 
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_classic.prompts import ChatPromptTemplate
from app.config import MODEL_NAME, SYSTEM_PROMPT

load_dotenv()

def analyze_content(text_content):
    """이메일 본문 및 첨부파일 텍스트를 분석하여 정보 유출 리스크 평가"""
    llm = ChatOpenAI(model=MODEL_NAME, reasoning_effort="low")

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "발송 대기 중인 콘텐츠:\n{content}")
    ])

    chain = prompt | llm
    result_text = chain.invoke({"content": text_content}).content

    try:
        return json.loads(result_text)
    except:
        return {"error": "보안 분석 결과 파싱 실패", "raw": result_text}