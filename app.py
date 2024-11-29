import streamlit as st
import requests
import re
import json
import time


# 共通設定
MAX_RETRIES = 3
RETRY_DELAY = 5  # リトライ間隔（秒）
col1, col2, col3 = st.columns([1, 2, 1]) 

# セッションステートでページを管理
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'  # 初期状態はホームページ

# ページの切り替え用関数
def switch_page(page_name):
    st.session_state['page'] = page_name
    st.experimental_rerun()

# ページの切り替え用関数
def switch_page(page_name):
    st.session_state['page'] = page_name  # 状態を更新

# ホームページ
if st.session_state['page'] == 'home':
    st.title("アプリへようこそ！")
    st.write("以下からアプリを選択してください。")
    
    # キャリアカウンセラーアプリへのリンク
    if st.button("キャリアカウンセラーアプリ"):
        switch_page('career')

    # 教育提案アプリへのリンク
    if st.button("教育提案アプリ"):
        switch_page('education')

# キャリアカウンセラーアプリ
elif st.session_state['page'] == 'career':
    st.title("キャリアカウンセラーアプリ")
    #ホームページへの戻りボタンの使い方修正
    if st.button("ホームに戻る"):
        switch_page('home')  # `on_click`ではなく直接呼び出す
        st.experimental_rerun()  # ページリロード

    st.title("キャリアカウンセラーアプリ")
    with col2:
        st.image(
        "https://th.bing.com/th/id/OIP.Y23nBpZxgajNoKec58O0twHaHa?w=202&h=202&c=7&r=0&o=5&pid=1.7",  
        use_column_width=True)
        
    # Lambda 関数のエンドポイント URL
    counselor_url = 'https://pg2galxz0c.execute-api.ap-northeast-1.amazonaws.com/stage1/'

    # 会話履歴を保持するためのセッションステート
    if 'conversation_history' not in st.session_state:
        st.session_state['conversation_history'] = []

    # これまでの会話履歴を表示
    st.write("### 会話履歴")
    for chat in st.session_state['conversation_history']:
        with st.chat_message(chat["role"]):
            st.write(chat["content"])

    # ユーザーの質問を入力
    career_question = st.text_input('キャリアに関する相談を入力してください:', 'ここを消して入力：例）5年後もなくならない仕事ができるようになりたい')

    # 相談するボタン
    if st.button('相談する'):
        if career_question:
            # ユーザーの入力を履歴に追加
            st.session_state['conversation_history'].append({"role": "user", "content": career_question})

            # AIの応答を処理
            with st.spinner('相談内容を処理中です...'):
                try:
                    # Lambda 関数にリクエストを送信
                    response = requests.post(
                        url=counselor_url,
                        json={
                            "conversation_history": st.session_state['conversation_history'],
                            "user_input": career_question
                        },
                        headers={"Content-Type": "application/json"}
                    )

                    if response.status_code == 200:
                        # Lambdaからの応答を取得
                        result = response.json()

                        # AIの応答を履歴に追加
                        st.session_state['conversation_history'].append({"role": "assistant", "content": result["response"]})
                        st.rerun()
                    else:
                        st.error(f"エラー: ステータスコード {response.status_code}")

                except Exception as e:
                    st.error(f"リクエストエラー: {e}")

elif st.session_state['page'] == 'education':
    st.title("教育提案アプリ　LinkedInとAidemyから研修を検索してきます")
    #ホームページへの戻りボタンの使い方修正
    if st.button("ホームに戻る"):
        switch_page('home')  # `on_click`ではなく直接呼び出す
        st.experimental_rerun()  # ページリロード
    
    with col2:
        st.image(
            "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi8vyJho9t80345AD_apyUqcEZ_buav7VArC19VWGSX3j_xeKrs3J1pAYjHqKKP_gfsctyC3uya943aZK53aqBnxlb-yHo-Np1CcxFK6Drzwd0q3uvOU4MgHuwvLOiVy7vmP2JkRRBLfm1g/s800/searchbox14.png",  
            use_column_width=True
        )
    st.text('検索には30秒くらいかかります。気長にお待ちください。')
    st.text('503エラーの時は再検索してください')

    # APIエンドポイントのURL
    education_url = 'https://53u1zlkx3h.execute-api.ap-northeast-1.amazonaws.com/stage1/education_test'

    # キャリア目標の入力
    career_goal = st.text_input('キャリア目標を入力してください:', 'ここを消して入力：例）AIエンジニア')

    # コースを推薦するボタン
    if st.button('コースを推薦する'):
        if career_goal:
            with st.spinner('検索中...しばらくお待ちください。'):
                try:
                    # APIリクエストを送信
                    response = requests.get(education_url, params={'career_goal': career_goal})

                    # レスポンスを正規表現で解析
                    pattern = r'{\s*"提供元":\s*"(.*?)",\s*"コース名":\s*"(.*?)",\s*"内容":\s*"(.*?)"\s*}'
                    matches = re.findall(pattern, response.text)

                    if matches:
                        # コース情報をきれいに表示
                        for match in matches:
                            provider, course_name, description = match
                            with st.container():
                                st.markdown("---")  # 区切り線
                                st.markdown(f"### 提供元: {provider}")
                                st.markdown(f"**コース名**: {course_name}")
                                st.markdown(f"**内容**: {description}")
                    else:
                        st.write(response)
                        st.warning("該当するコースが見つかりませんでした。")

                except Exception as e:
                    st.error(f"リクエストエラー: {e}")

