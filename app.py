import streamlit as st
import requests
import re
import json
import time


# 共通設定
MAX_RETRIES = 3
RETRY_DELAY = 5  # リトライ間隔（秒）

# サイドバーでアプリを選択
st.sidebar.title("アプリ選択")
app_selection = st.sidebar.radio("アプリを選択してください", ["キャリアカウンセラーアプリ", "教育提案アプリ"])

col1, col2, col3 = st.columns([1, 2, 1])  # 中央列を少し広めに設定




if app_selection == "キャリアカウンセラーアプリ":
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

elif app_selection == "教育提案アプリ":
    st.title("教育提案アプリ　LinkedInとAidemyから研修を検索してきます")
    
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
                    st.write(response.txt)
                    
                    # レスポンス全体を表示（デバッグ用）
                    st.write("### レスポンス内容")
                    st.code(response.text, language="json")

                    # 正規表現でコース情報を抽出
                    course_pattern = re.compile(r'{.*?}')  # {}で囲まれた部分を抽出
                    courses_raw = course_pattern.findall(response.text)

                    if courses_raw:
                        for course_str in courses_raw:
                            try:
                                # JSON形式に変換
                                course = json.loads(course_str)
                                
                                # 各コース情報を表示
                                with st.container():
                                    st.markdown("---")  # 区切り線
                                    st.markdown(f"### 提供元: {course.get('提供元', '不明')}")
                                    st.markdown(f"**コース名**: {course.get('コース名', '不明')}")
                                    st.markdown(f"**内容**: {course.get('内容', '不明')}")
                            except json.JSONDecodeError:
                                st.warning("コース情報の解析中にエラーが発生しました。")
                    else:
                        st.warning("該当するコースが見つかりませんでした。")

                except Exception as e:
                    st.error(f"リクエストエラー: {e}")
