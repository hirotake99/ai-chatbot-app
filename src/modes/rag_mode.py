import os
import openai
from elasticsearch import Elasticsearch

def get_es_client():
    """
    Elasticsearch クライアントを作成する。
    """
    return Elasticsearch(
        cloud_id=os.getenv('ES_CLOUD_ID'),
        api_key=os.getenv('ES_API_KEY')
    )

def query_elasticsearch(query, index="documents"):
    """
    Elasticsearch に対してクエリを実行し、マッチした文書の内容を返します。
    """
    es = get_es_client()

    # multi_match クエリを使用して複数フィールドを検索する
    search_query = {
        "multi_match": {
            "query": query,
            "fields": ["title", "content"]
        }
    }

    # クエリDSLを body パラメータに含める
    res = es.search(index=index, body={"query": search_query})
    hits = res.get("hits", {}).get("hits", [])
    results = [hit["_source"].get("content", "") for hit in hits]
    return results

def embed_text(text, model="text-embedding-ada-002"):
    """
    OpenAI Embedding API を利用して、入力テキストからベクトルを取得します。
    """
    response = openai.Embedding.create(input=text, model=model)
    embedding = response['data'][0]['embedding']
    return embedding

def upload_document_vector(document, doc_id=None, index="documents"):
    """
    ドキュメントをベクトル埋め込みとともに Elastic Cloud のデータベースへアップロードします。

    ※ Elasticsearch 側で embedding フィールドのマッピング（dense_vector）が設定済みであることが前提です。
    """
    emb = embed_text(document)
    es = get_es_client()

    doc_body = {
        "content": document,
        "embedding": emb
    }

    return es.index(index=index, id=doc_id, document=doc_body)

def rag_with_elastic(query, conversation_history):
    """
    ユーザーのクエリに基づいて Elasticsearch から関連ドキュメントを取得し、
    そのコンテキストとともに OpenAI に問い合わせる RAG 機能を提供します。
    """
    index = "documents"

    # Elasticsearch から関連ドキュメントを取得
    docs = query_elasticsearch(query, index=index)

    # 取得したドキュメントの内容をコンテキストにまとめる
    context = "\n\n".join(docs) if docs else "関連ドキュメントは見つかりませんでした。"

    # 会話履歴と共にプロンプトを組み立てる
    messages = []
    for entry in conversation_history:
        messages.append({"role": "user", "content": entry["user"]})
        messages.append({"role": "assistant", "content": entry["bot"]})

    prompt = f"以下の文書から情報を取得しました:\n{context}\n\nユーザーからの質問:\n{query}"
    messages.append({"role": "user", "content": prompt})

    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=500
    )

    return response.choices[0].message['content']