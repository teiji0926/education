import streamlit as st
import requests
import json

# エンドポイントのURL
url = 'https://olumybzbkw5phnjmqiruqtk47q0jltfl.lambda-url.ap-northeast-1.on.aws/'

# キャリア目標の入力
career_goal = st.text_input('キャリア目標を入力してください:', 'AIエンジニア')

# コースを推薦するボタン
if st.button('コースを推薦する'):
    if career_goal:
        try:
            response = requests.get(url, params={'career_goal': career_goal})

            # ステータスコードを表示
            st.write(f"ステータスコード: {response.status_code}")

            # レスポンス全体を表示（デバッグ用）
            st.write("APIレスポンス全体:")
            st.json(response.json())

            if response.status_code == 200:
                # レスポンスをJSONとしてロード
                data = response.json()
                suggestions = data.get('suggestions', [])

                # 'suggestions' がリスト形式かを確認して処理
                if isinstance(suggestions, list) and suggestions:
                    # 各コース情報を表示
                    for course in suggestions:
                        with st.container():
                            st.subheader(course.get('コース名', 'コース名不明'))
                            st.write(f"提供元: {course.get('提供元', '不明')}")
                            st.write(f"内容: {course.get('内容', '不明')}")
                            st.markdown("---")  # 区切り線
                else:
                    st.error("コース情報が見つかりませんでした。")
            else:
                st.error(f"APIリクエストに失敗しました。ステータスコード: {response.status_code}")
        except Exception as e:
            st.error(f"リクエストエラー: {e}")
    else:
        st.warning('キャリア目標を入力してください。')
