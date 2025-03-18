# -----------------------------
# 크롤링된 데이터 저장용 리스트
# -----------------------------

# 텍스트 분리기 초기화
class CharacterTextSplitter:
    def __init__(self, chunk_size=850, chunk_overlap=100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text):
        chunks = []
        if len(text) <= self.chunk_size:
            return [text]

        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunk = text[i:i + self.chunk_size]
            if chunk:
                chunks.append(chunk)
        return chunks

text_splitter = CharacterTextSplitter(chunk_size=850, chunk_overlap=100)
titles=[]
dates=[]
summaries=[]
body_chunks=[]
urls=[]
for article in articles_data:
  if isinstance(article['body_chunks'], str):  # 분리된 본문이 str
      split_chunks = text_splitter.split_text(article['body_chunks'])  # 본문 덩어리마다 850자씩 분리
      body_chunks.extend(split_chunks)  # 분리된 텍스트들을 body_chunks에 추가
      titles.extend([article['title']] * len(split_chunks))  # 분리된 각 본문에 제목을 추가
      dates.extend([article['date']] * len(split_chunks))  # 분리된 각 본문에 날짜를 추가
      summaries.extend([article['summary']] * len(split_chunks))  # 분리된 각 본문에 요약을 추가
      urls.extend([article['url']] * len(split_chunks))  # 분리된 각 본문에 URL을 추가
  else:
    titles.append(article['title'])
    dates.append(article['date'])
    summaries.append(article['summary'])
    body_chunks.append(article['body_chunks'])
    urls.append(article['url'])
