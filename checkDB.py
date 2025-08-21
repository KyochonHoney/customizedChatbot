import chromadb

# 1. ChromaDB 클라이언트 연결
chroma_client = chromadb.HttpClient(host="localhost", port=8000)

# 2. 현재 존재하는 컬렉션 목록 출력
print("--- 현재 존재하는 컬렉션 목록 (시작) ---")
print(chroma_client.list_collections())
print("--- 현재 존재하는 컬렉션 목록 (끝) ---")

# 3. 'part3' 컬렉션 가져오기 (없으면 생성)
# 이미 컬렉션이 있으니 create_collection 대신 get_or_create_collection 사용!
print("\n--- 'part3' 컬렉션 가져오기 또는 생성 시도 ---")
collection = chroma_client.get_or_create_collection(name="cures1")
print(f"Collection '{collection.name}'에 연결되었습니다.")

# 4. 'part3' 컬렉션에 데이터 추가 (예시)
# 만약 데이터가 없다면 테스트용으로 넣어볼 수 있어요!
# 이미 데이터가 있다면 이 부분은 건너뛰셔도 돼요.
print("\n--- 'part3' 컬렉션에 예시 데이터 추가 시도 ---")
try:
    collection.add(
        documents=["이것은 첫 번째 문서입니다.", "두 번째로 추가하는 문서입니다."],
        metadatas=[{"source": "source1"}, {"source": "source2"}],
        ids=["doc1", "doc2"]
    )
    print("예시 데이터가 성공적으로 추가되었습니다.")
except Exception as e:
    print(f"예시 데이터 추가 실패 또는 이미 존재: {e}")


# 5. 'part3' 컬렉션 안에 있는 모든 데이터 가져오기 및 출력
print(f"\n--- 컬렉션 '{collection.name}'의 모든 데이터 ---")
# .get() 메서드에 limit=None을 주면 컬렉션 내의 모든 항목을 가져와요.
# ids=[], documents=[], metadatas=[], embeddings=[] 중 필요한 항목을 True로 설정하세요.
# 여기서는 문서 내용과 메타데이터, ID를 볼 수 있도록 했습니다.
all_items_in_collection = collection.get(
    ids=None,
    where=None,
    limit=None,
    offset=0,
    where_document=None,
    include=['documents', 'metadatas'] # 문서 내용과 메타데이터를 포함해서 가져와줘!
)

print(f"컬렉션 '{collection.name}'에 총 {len(all_items_in_collection['ids'])}개의 항목이 있습니다.")
for i in range(len(all_items_in_collection['ids'])):
    print(f"  - ID: {all_items_in_collection['ids'][i]}")
    print(f"    문서: {all_items_in_collection['documents'][i]}")
    print(f"    메타데이터: {all_items_in_collection['metadatas'][i]}")
print("--- 컬렉션 데이터 확인 완료 ---")

# 6. 모든 컬렉션 목록 다시 출력 (변화가 없을 수도 있어요)
print("\n--- 현재 존재하는 컬렉션 목록 (최종) ---")
print(chroma_client.list_collections())
print("--- 현재 존재하는 컬렉션 목록 (끝) ---")
