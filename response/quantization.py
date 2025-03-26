
import faiss
import numpy as np
from time import time

# 원본 벡터 (dense_doc_vectors)의 차원 확인
d = dense_doc_vectors.shape[1]  # 벡터의 차원
n = dense_doc_vectors.shape[0]  # 벡터의 개수

# 1. 기본 IndexFlatL2 (양자화 없음 - 비교 기준)
index_flat = faiss.IndexFlatL2(d)
index_flat.add(dense_doc_vectors)

# 2. 스칼라 양자화 (8비트)
index_scalar_8bit = faiss.IndexScalarQuantizer(d, faiss.ScalarQuantizer.QT_8bit)
index_scalar_8bit.train(dense_doc_vectors)  # 먼저 학습 과정 수행
index_scalar_8bit.add(dense_doc_vectors)

# 6. IVFSQ (Inverted File + Scalar Quantization)
index_ivfsq = faiss.IndexIVFScalarQuantizer(quantizer, d, nlist, faiss.ScalarQuantizer.QT_8bit)
index_ivfsq.train(dense_doc_vectors)
index_ivfsq.add(dense_doc_vectors)
index_ivfsq.nprobe = 10  # 검색 시 확인할 클러스터 수
