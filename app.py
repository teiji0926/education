import streamlit as st
import requests
import re

# APIエンドポイントのURL
url = 'https://53u1zlkx3h.execute-api.ap-northeast-1.amazonaws.com/stage1/education_test'

# キャリア目標の入力
career_goal = st.text_input('キャリア目標を入力してください:', 'AIエンジニア')
st.text('検索には30秒くらいかかります。気長にお待ちください。')
st.text('503エラーの時は再検索してください')

# コースを推薦するボタン
if st.button('コースを推薦する'):
    if career_goal:
        try:
            # APIリクエストを送信
            response = requests.get(url, params={'career_goal': career_goal})

            # ステータスコードを表示
            st.write(f"ステータスコード: {response.status_code}")

            if response.status_code == 200:
                # '''json''' タグを削除してリストの形式だけを表示する
                cleaned_text = re.sub(r"```json|```", "", response.text.strip())

                # 各コース情報を個別に表示
                courses = re.findall(r"{.*?}", cleaned_text)  # 各コース情報を抽出
                for course_str in courses:
                    course_info = eval(course_str)  # 文字列を辞書に変換
                    st.write(f"提供元: {course_info.get('提供元', '不明')}")
                    st.write(f"コース名: {course_info.get('コース名', '不明')}")
                    st.write(f"内容: {course_info.get('内容', '不明')}")
                    st.markdown("---")  # 区切り線
            else:
                st.error(f"エラー: ステータスコードが {response.status_code} です。")
        except Exception as e:
            st.error(f"リクエストエラー: {e}")
    else:
        st.warning('キャリア目標を入力してください。')
