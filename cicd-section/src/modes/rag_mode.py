import os
import openai
from elasticsearch import Elasticsearch
from janome.tokenizer import Tokenizer
from dotenv import load_dotenv

# 現在のスクリプトと同じディレクトリにある .env ファイルのパスを取得
env_path = os.path.join(os.path.dirname(__file__), '.env')
# .env ファイルから環境変数をロード
load_dotenv(dotenv_path=env_path)

def get_es_client():
    """
    Elasticsearch クライアントを作成する。
    """
    return Elasticsearch(
        cloud_id=os.getenv('ES_CLOUD_ID'),
        api_key=os.getenv('ES_API_KEY')
    )

def split_text_into_chunks(text, max_chunk_tokens=200, lang="ja"):
    """
    テキストを指定された単語数（概算トークン数）ごとにチャンクに分割する関数です。

    日本語の場合は、Janome による形態素解析で単語に分割し、
    英語などの場合は単純な空白での分割を行います。

    Parameters:
        text (str): 分割するテキスト
        max_chunk_tokens (int): チャンクあたりの最大トークン数
        lang (str): 言語指定 ("ja" なら日本語、その他なら空白区切り)

    Returns:
        List[str]: チャンクに分割されたテキストのリスト
    """
    if lang == "ja":
        # Janome を用いて日本語を形態素解析
        tokenizer = Tokenizer()
        tokens = [token.surface for token in tokenizer.tokenize(text)]
        # 日本語は空白を入れずに連結するのが一般的
        joiner = ""
    else:
        # 英語などは単純な split() を利用
        tokens = text.split()
        joiner = " "

    chunks = []
    current_chunk = []
    for token in tokens:
        if len(current_chunk) + 1 > max_chunk_tokens:
            chunks.append(joiner.join(current_chunk))
            current_chunk = [token]
        else:
            current_chunk.append(token)
    if current_chunk:
        chunks.append(joiner.join(current_chunk))
    return chunks

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

def upload_document_vector(document, doc_id=None, index="documents", chunk_tokens=200, lang="ja"):
    """
    ドキュメントをチャンク分割して、各チャンクをベクトル埋め込みとともに Elastic Cloud のデータベースへアップロードします。

    ※ Elasticsearch 側で embedding フィールドのマッピング（dense_vector）が設定済みであることが前提です。

    lang 引数により、言語に応じたチャンク分割が行われます（日本語の場合は "ja"）。
    """
    # まず文書をチャンクに分割
    chunks = split_text_into_chunks(document, max_chunk_tokens=chunk_tokens, lang=lang)
    es = get_es_client()
    results = []

    for i, chunk in enumerate(chunks):
        emb = embed_text(chunk)
        doc_body = {
            "content": chunk,
            "embedding": emb
        }
        # doc_id が指定されていれば、各チャンクにユニークなIDを付与する
        chunk_doc_id = f"{doc_id}_{i}" if doc_id else None
        res = es.index(index=index, id=chunk_doc_id, document=doc_body)
        results.append(res)
    return results

def rag_with_elastic(query, conversation_history, chunk_tokens=200, lang="ja"):
    """
    ユーザーのクエリに基づいて Elasticsearch から関連ドキュメントを取得し、
    チャンク分割したコンテキストとともに OpenAI に問い合わせる RAG 機能を提供します。

    lang 引数により、チャンク分割時の言語指定が可能です。
    """
    index = "documents"

    # Elasticsearch から関連ドキュメントを取得
    docs = query_elasticsearch(query, index=index)

    # 各文書をチャンクに分割し、チャンク毎の内容をコンテキストにまとめる
    chunked_docs = []
    for doc in docs:
        chunks = split_text_into_chunks(doc, max_chunk_tokens=chunk_tokens, lang=lang)
        chunked_docs.extend(chunks)

    context = "\n\n".join(chunked_docs) if chunked_docs else "関連ドキュメントは見つかりませんでした。"

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
