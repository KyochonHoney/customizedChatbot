# deleteDB.py  (null/빈 문서 일괄 정리)
from langchain_chroma import Chroma

PERSIST_DIR = "./chroma_huggingface"   # 당신이 쓰는 경로 그대로
COLLECTION  = "cures"                  # 당신이 쓰는 컬렉션명 그대로
BATCH_SIZE  = 200

def is_bad(doc) -> bool:
    if doc is None:
        return True
    if not isinstance(doc, str):
        return True
    s = doc.strip()
    if s == "":
        return True
    low = s.lower()
    return low in {"nan", "none", "null"}

def chunker(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

def main():
    # 임베딩 지정 안 함(삭제/조회만 필요)
    db = Chroma(collection_name=COLLECTION, persist_directory=PERSIST_DIR)

    # ⚠ include에 'ids' 넣지 마세요. ids는 자동 반환됩니다.
    data = db.get(include=["documents"])  # 'ids' 뺌
    ids  = data.get("ids", []) or []
    docs = data.get("documents", []) or []

    total = len(ids)
    print(f"[INFO] total docs: {total}")

    bad_ids = [i for i, d in zip(ids, docs) if is_bad(d)]
    print(f"[INFO] to delete (bad docs): {len(bad_ids)}")

    if not bad_ids:
        print("[INFO] nothing to delete.")
        return

    deleted = 0
    for chunk in chunker(bad_ids, BATCH_SIZE):
        db.delete(ids=chunk)
        deleted += len(chunk)
        print(f"[INFO] deleted {deleted}/{len(bad_ids)}")

    print("[DONE] cleanup complete.")

if __name__ == "__main__":
    main()

