import faiss
import pickle
# -----------------------------
# FAISS에 데이터 저장 및 임베딩
# -----------------------------

#  Upstage 임베딩 객체 생성
embeddings = UpstageEmbeddings(
    api_key=upstage_api_key,
    model="solar-embedding-1-large"
)

#  임베딩할 텍스트 준비 및 메타데이터 생성
# 텍스트 준비 및 메타데이터 생성 (본문만 임베딩)
# 텍스트 준비 및 메타데이터 생성 (본문만 임베딩)
texts = []
metadata_list = []

# 본문만 임베딩하도록 수정
for i, article in enumerate(articles_data):
    # 만약 body_chunks가 이미 리스트라면 split_text를 거치지 않음
    if isinstance(article['body_chunks'], list):  
        for chunk in article['body_chunks']:
            texts.append(chunk)  # 본문만 텍스트에 저장
            
            metadata = {
                "id": f"article-{i}",
                "title": article['title'],
                "date": article['date'],
                "summary": article['summary'],
                "url": article['url']
            }
            metadata_list.append(metadata)
    else:
        # 본문이 문자열이면 분리하여 처리
        split_chunks = text_splitter.split_text(article['body_chunks'])
        for chunk in split_chunks:
            texts.append(chunk)  # 본문만 텍스트에 저장
            
            metadata = {
                "id": f"article-{i}",
                "title": article['title'],
                "date": article['date'],
                "summary": article['summary'],
                "url": article['url']
            }
            metadata_list.append(metadata)

# 텍스트 수 확인
print(len(texts))
# # Upstage로 임베딩하기
dense_doc_vectors = np.array(embeddings.embed_documents(texts)).astype('float32')  # 임베딩
