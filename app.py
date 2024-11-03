import streamlit as st
import requests

# エンドポイントのURL
url = 'https://olumybzbkw5phnjmqiruqtk47q0jltfl.lambda-url.ap-northeast-1.on.aws/'

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

            # responseオブジェクト全体を表示
            st.write("APIレスポンス全体 (responseオブジェクト):")
            st.write(response)  # responseオブジェクトをそのまま表示

            if response.status_code == 200:
                # 正常にレスポンスが返された場合にJSONを解析
                data = response.json()
                suggestions = data.get('suggestions', [])

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
