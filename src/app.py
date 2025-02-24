from flask import Flask
import streamlit as st
from modes.natural_language_mode import chat_with_bot
from modes.image_mode import process_image_and_query
from modes.audio_mode import process_audio_and_query
from modes.rag_mode import rag_with_elastic, upload_document_vector
import threading

app = Flask(__name__)


def main():
    st.title("AI Chatbot Application")

    mode = st.sidebar.selectbox("Select Mode", ["自然言語モード", "画像モード", "音声モード"])

    if mode == "自然言語モード":
        # セッションステートに会話履歴用のリストが無い場合は初期化
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []
                # 会話履歴リセットボタン
        if st.button("履歴のリセット"):
            st.session_state["chat_history"] = []
        # RAG機能のオンオフ選択トグル
        use_rag = st.checkbox("RAG機能を有効化", value=False)

        # RAG機能がオンの場合、ドキュメントアップロードUIを表示
        if use_rag:
            st.subheader("ドキュメントアップロード")
            document_text = st.text_area("アップロードするドキュメントの内容を入力してください")
            if st.button("アップロード"):
                res = upload_document_vector(document_text)
                st.write("アップロード結果:", res)

        # 会話履歴を表示
        user_input = st.text_input("あなたの質問を入力してください:")
        if st.button("送信"):
            if use_rag:
                response = rag_with_elastic(user_input, st.session_state["chat_history"])
            else:
                response = chat_with_bot(user_input, st.session_state["chat_history"])
            # 会話履歴に追記
            st.session_state["chat_history"].append({"user": user_input, "bot": response})

        if st.session_state["chat_history"]:
            for entry in st.session_state["chat_history"]:
                st.write("あなた: ", entry["user"])
                st.write("ボット: ", entry["bot"])
                st.markdown("---")

    elif mode == "画像モード":
        uploaded_file = st.file_uploader("画像をアップロードしてください:", type=["jpg", "jpeg", "png"])
        user_query = st.text_input("質問を入力してください:")
        if st.button("送信"):
            if uploaded_file is not None:
                response = process_image_and_query(uploaded_file, user_query)
                st.write("ボットの応答:", response)

    elif mode == "音声モード":
        if 'conversation_history' not in st.session_state:
            st.session_state.conversation_history = []
        if st.button("音声チャット開始"):
            process_audio_and_query()
        if st.session_state.conversation_history:
            for message in st.session_state.conversation_history:
                st.write(message)


if __name__ == "__main__":
    main()