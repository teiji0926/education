import streamlit as st
import requests
import json

# APIエンドポイントのURL
url = 'https://53u1zlkx3h.execute-api.ap-northeast-1.amazonaws.com/stage1/education_test'

# キャリア目標の入力
career_goal = st.text_input('キャリア目標を入力してください:', 'AIエンジニア')

# コースを推薦するボタン
if st.button('コースを推薦する'):
    if career_goal:
        try:
            # APIリクエストを送信
            response = requests.get(url, params={'career_goal': career_goal})

            # ステータスコードを表示
            st.write(f"ステータスコード: {response.status_code}")

            # レスポンス内容をそのまま表示して確認
            st.write("APIレスポンス内容:")
            st.text(response.text)

            if response.status_code == 200:
                try:
                    # JSONレスポンスをデコードして表示
                    data = response.json()
                    if isinstance(data, list):
                        for course in data:
                            # 各コース情報をきれいに表示
                            st.subheader(course.get('コース名', 'コース名不明'))
                            st.write(f"提供元: {course.get('提供元', '不明')}")
                            st.write(f"内容: {course.get('内容', '不明')}")
                            st.markdown("---")
                    else:
                        st.error("レスポンスがリスト形式ではありません。")
                except json.JSONDecodeError:
                    st.error("レスポンスがJSON形式ではありません。内容:")
                    st.text(response.text)
            else:
                st.error(f"エラー: ステータスコードが {response.status_code} です。")
        except Exception as e:
            st.error(f"リクエストエラー: {e}")
    else:
        st.warning('キャリア目標を入力してください。')
