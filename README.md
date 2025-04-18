
---

# 💰 Financial-Chatbot  
> **Finance RAG + LLM + AI Agent Assistant Chatbot**  
> **Development Period**: 2025.03.11~2025.09.01

---

## 🎯 프로젝트 목표  

1. **재무 정보에 대한 쉽고 빠른 접근**  
   - 사용자가 경제 관련 뉴스 및 재무 관련 질문을 하면 즉시 관련된 정보를 제공.  

2. **AI 기반 자동화된 금융 비서**  
   - RAG (Retrieval-Augmented Generation)와 LLM (Large Language Model)을 활용하여 개인 맞춤형 금융 상담 및 정보 제공.  

3. **비용 효율적인 AI 서비스 구축**  
   - 성능과 비용을 모두 고려한 모델 및 인프라 설계.  

---

## ⚙️ 기술 스택 및 모델 구성  

| 목적                     | 사용 기술 (모델)                  | 비고                         |
|------------------------|------------------------------|----------------------------|
| **벡터 데이터베이스**       | FAISS                         | 빠른 데이터 검색용               |
| **LLM (대형 언어 모델)**  | OpenAI GPT or Upstage         | 자연어 이해 및 응답 생성          |
| **임베딩 모델**           | Upstage                       | 한국어 임베딩 및 비용 절감 목적     |

---

## ✅ 기대 효과  

- **실시간 금융 정보 및 상담 제공**  
- **AI 기반 맞춤형 금융 정보 서비스**  
- **비용 대비 높은 성능의 챗봇 시스템 구축**  

---
## 1차 성능 테스트 (25/3/20)
![image](https://github.com/user-attachments/assets/a55ddf37-5a59-4eaf-8062-46da75fa903d)
> 다양한 양자화 방식 중 성능이 괜찮은 8bit와 IVFSQ 기법을 도입하여 테스트케이스 100개 쿼리를 던져 테스트를 진행한 결과임.
> 현재 LLM 모델을 upstage를 쓰고 있는데 OpenAI로도 써보고 평가를 해봐야 응답속도 개선 가능 유무를 판단할 수 있을 것이라는 결론을 지음.
--- 
## 2차 성능 테스트 (25/3/25)
![image](https://github.com/user-attachments/assets/0f77b24f-a50c-45eb-8c82-1c939111971e)
> 질문지 160개로 테스트를 실시함. 8bits 방법이 이상하게 많이 걸렸는데 특정 질문에 응답 속도가 너무 느려져서 저런 결과가 나온 듯. 원래는 ivfsq와 비슷하게 나왔음.
> 여기서 분석할만한 것이 그냥 "재정렬"이라는 Ai agent를 활용해 문서 재정렬하는 시간을 없애는게 속도 측면 개선에 더 도움 될 것 같다는 생각이 들었다. 이전의 경북대 학사제공 AI 서비스도 이 기법을 적용하려다가 응답 시간만 늦어지고 별다른 효과를 못 본 기억이 있어서 그냥 검색한 문서 반환하는 과정 자체를 strict 하게 구현하는 것이 나을 것 같다. 현재 BM25도 적용하지 않은 말 그대로 dense방식만을 적용한 상태이기 때문에 개선할 필요가 있다고 본다.
