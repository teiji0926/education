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
        # APIリクエストを送信
        response = requests.get(url, params={'career_goal': career_goal})
        # ステータスコードを表示
        st.write(f"ステータスコード: {response.status_code}")
        # レスポンス内容をそのまま表示して確認
        st.write("APIレスポンス内容:")
        st.text(response.text)
else:
    st.warning('キャリア目標を入力してください。')
        
