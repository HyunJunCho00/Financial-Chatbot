import time
from tabulate import tabulate
import numpy as np


# 테스트할 인덱스 선택
llm = ChatUpstage(api_key=upstage_api_key)
# AI Agent 클래스 정의
class AIAgent:
    def __init__(self, model):
        self.model = model  # Upstage API 사용

    def rank_documents(self, query, docs):
        """상위 2개 문서만 LLM을 활용해 재정렬 (벡터 유사도 기반 우선 필터링)"""
        if len(docs) <= 2:
            return docs  # 문서가 2개 이하이면 그대로 반환

        # 배치 프롬프트 적용 (한 번의 LLM 호출로 여러 문서 평가)
        prompt = f"다음 문서들이 질문과 얼마나 관련 있는지 1~10점으로 평가하세요.\n"
        for i, doc in enumerate(docs[:3]):  # 상위 3개 문서만 평가
            prompt += f"{i+1}. 문서: {doc}\n"
        prompt += f"\n각 문서의 점수를 숫자로만 반환하세요:"

        response = self.model.invoke([HumanMessage(content=prompt)]).content.strip()
        scores = [float(s) if s.replace('.', '', 1).isdigit() else 5.0 for s in response.split()]

        # 점수 순으로 정렬 후 상위 2개 선택
        ranked_docs = sorted(zip(docs[:3], scores), key=lambda x: x[1], reverse=True)
        return [doc for doc, _ in ranked_docs[:2]]
# AI Agent 생성
ai_agent = AIAgent(llm)

test_indices = {
    "Flat (원본)": index_flat,
    "스칼라 양자화 (8bit)": index_scalar_8bit,
    "IVFSQ": index_ivfsq,
}

def get_upstage_answer(context, query):
    messages = [
        SystemMessage(content="The question must be answered detailed, and the answer must contain only the information contained in the document"),
        HumanMessage(content=f"{context}\n\n질문: {query}\n답변:")
    ]
    response = llm.invoke(messages)
    return response.content

# 평균 시간 저장 딕셔너리
average_times = {name: {"search": 0, "ranking": 0, "response": 0, "total": 0} for name in test_indices.keys()}

# 100개 질문 실행
for query in query_list:
    results_summary = []
    query_vector = np.array(embeddings.embed_query(query)).astype('float32').reshape(1, -1)

    for name, index in test_indices.items():
        t0 = time.time()
        D, I = index.search(query_vector, 3)
        t1 = time.time()
        search_time = (t1 - t0) * 1000

        retrieved_docs = []
        source_info = []
        for i in range(len(I[0])):
            if I[0][i] < len(metadata_list):
                doc = metadata_list[I[0][i]]
                title = doc.get("title", "제목 없음")
                date = doc.get("date", "날짜 없음")
                summary = doc.get("summary", "요약 없음")
                url = doc.get("url", "#")
                retrieved_docs.append(f"{title} ({date})\n{summary}")
                source_info.append(f"[{title}]({url})")

        t2 = time.time()
        retrieved_docs = ai_agent.rank_documents(query, retrieved_docs)
        t3 = time.time()
        ranking_time = (t3 - t2) * 1000

        context = "\n\n".join(retrieved_docs)
        t4 = time.time()
        answer = get_upstage_answer(context, query)
        t5 = time.time()
        response_time = (t5 - t4) * 1000

        total_time = search_time + ranking_time + response_time

        # 평균 시간 누적
        average_times[name]["search"] += search_time
        average_times[name]["ranking"] += ranking_time
        average_times[name]["response"] += response_time
        average_times[name]["total"] += total_time

        results_summary.append([query, name, f"{search_time:.2f} ms", f"{ranking_time:.2f} ms", f"{response_time:.2f} ms", f"{total_time:.2f} ms", answer, "\n".join(source_info)])

    headers = ["질문", "인덱스 방식", "검색 시간(ms)", "재정렬 시간(ms)", "응답 시간(ms)", "총 시간(ms)", "AI 답변", "출처 (기사 제목 및 URL)"]
    print(tabulate(results_summary, headers=headers, tablefmt="grid"))

# 평균 시간 출력
print("\n[100개 질문에 대한 평균 소요 시간]")
summary_avg = []
for name, times in average_times.items():
    summary_avg.append([name, f"{times['search']/100:.2f} ms", f"{times['ranking']/100:.2f} ms", f"{times['response']/100:.2f} ms", f"{times['total']/100:.2f} ms"])
headers_avg = ["인덱스 방식", "평균 검색 시간(ms)", "평균 재정렬 시간(ms)", "평균 응답 시간(ms)", "평균 총 시간(ms)"]
print(tabulate(summary_avg, headers=headers_avg, tablefmt="grid"))
