import streamlit as st
import requests
import re
import time

# 検索時間の注意書きとエラーメッセージについてのメッセージを表示
st.text('検索には30秒くらいかかります。気長にお待ちください。')
st.text('503エラーの時は再検索してください')

# APIエンドポイントのURL
url = 'https://53u1zlkx3h.execute-api.ap-northeast-1.amazonaws.com/stage1/education_test'

# キャリア目標の入力
career_goal = st.text_input('キャリア目標を入力してください:', 'AIエンジニア')

# 最大リトライ回数
MAX_RETRIES = 3
RETRY_DELAY = 5  # リトライ間隔（秒）

# コースを推薦するボタン
if st.button('コースを推薦する'):
    if career_goal:
        for attempt in range(MAX_RETRIES):
            try:
                # APIリクエストを送信
                response = requests.get(url, params={'career_goal': career_goal})

                # ステータスコードを表示
                st.write(f"ステータスコード: {response.status_code}")

                # ステータスコードが200（成功）の場合
                if response.status_code == 200:
                    # '''json''' タグを削除してリストの形式だけを表示する
                    cleaned_text = re.sub(r"```json|```", "", response.text.strip())

                    # 各コース情報を個別に表示
                    courses = re.findall(r"{.*?}", cleaned_text)  # 各コース情報を抽出
                    for course_str in courses:
                        course_info = eval(course_str)  # 文字列を辞書に変換

                        # 元の表示内容を保持しつつ、見やすく表示
                        st.write("提供元:", course_info.get("提供元", "不明"))
                        st.write("コース名:", course_info.get("コース名", "不明"))
                        st.write("内容:", course_info.get("内容", "不明"))

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
