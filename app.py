import streamlit as st
import requests
import re
import time


# 共通設定
MAX_RETRIES = 3
RETRY_DELAY = 5  # リトライ間隔（秒）

# サイドバーでアプリを選択
st.sidebar.title("アプリ選択")
app_selection = st.sidebar.radio("アプリを選択してください", ["キャリアカウンセラーアプリ", "教育提案アプリ"])

if app_selection == "キャリアカウンセラーアプリ":
    st.title("キャリアカウンセラーアプリ")

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
    career_question = st.text_input('キャリアに関する相談を入力してください:', '')

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
                    else:
                        st.error(f"エラー: ステータスコード {response.status_code}")

                except Exception as e:
                    st.error(f"リクエストエラー: {e}")

# 教育提案アプリ
elif app_selection == "教育提案アプリ":
    st.title("教育提案アプリ")
    st.text('検索には30秒くらいかかります。気長にお待ちください。')
    st.text('503エラーの時は再検索してください')

    # APIエンドポイントのURL
    education_url = 'https://53u1zlkx3h.execute-api.ap-northeast-1.amazonaws.com/stage1/education_test'

    # キャリア目標の入力
    career_goal = st.text_input('キャリア目標を入力してください:', 'AIエンジニア')

    # コースを推薦するボタン
    if st.button('コースを推薦する'):
        if career_goal:
            with st.spinner('検索中...しばらくお待ちください。'):
                for attempt in range(MAX_RETRIES):
                    try:
                        # APIリクエストを送信
                        response = requests.get(education_url, params={'career_goal': career_goal})

                        # ステータスコードを表示
                        st.write(f"ステータスコード: {response.status_code}")
                        st.write(response.text)

                        # ステータスコードが200（成功）の場合
                        if response.status_code == 200:
                            # '''json''' タグを削除してリストの形式だけを表示する
                            cleaned_text = re.sub(r"```json|```", "", response.text.strip())

                            # 各コース情報を個別に表示
                            courses = re.findall(r"{.*?}", cleaned_text)  # 各コース情報を抽出
                            for course_str in courses:
                                course_info = eval(course_str)  # 文字列を辞書に変換

                                # 各項目を太字で大きめのサイズで強調表示
                                st.markdown(f"<span style='font-size:20px; font-weight:bold;'>提供元: {course_info.get('提供元', '不明')}</span>", unsafe_allow_html=True)
                                st.markdown(f"<span style='font-size:18px; font-weight:bold;'>コース名: {course_info.get('コース名', '不明')}</span>", unsafe_allow_html=True)
                                st.markdown(f"<span style='font-size:16px;'>内容: {course_info.get('内容', '不明')}</span>", unsafe_allow_html=True)
                                st.markdown("<hr>", unsafe_allow_html=True)  # 区切り線
                            break  # 成功したらループを抜ける

                        else:
                            st.warning(f"エラー: ステータスコードが {response.status_code} です。リトライ {attempt + 1} 回目")
                            time.sleep(RETRY_DELAY)  # リトライ間隔

                    except Exception as e:
                        st.error(f"リクエストエラー: {e}")
                        time.sleep(RETRY_DELAY)  # リトライ間隔

                # 最大リトライ回数に達した場合のエラーメッセージ
                else:
                    st.error("リトライしても503エラーが発生しました。後ほど再度お試しください。")

        else:
            st.warning('キャリア目標を入力してください。')
