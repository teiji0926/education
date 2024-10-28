import streamlit as st
import requests
import json
import re

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

            if response.status_code == 200:
                # レスポンスをテキストで表示（デバッグ用）
                response_text = response.text

                # 'suggestions'フィールドの抽出
                data = json.loads(response_text)
                suggestions = data.get('suggestions', '')

                # バッククォートで囲まれているJSON部分を抽出
                json_match = re.search(r'```json\n(.*?)\n```', suggestions, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)

                    # シングルクォートをダブルクォートに置き換える
                    json_str = json_str.replace("'", '"')

                    try:
                        # JSON文字列をリストに変換
                        course_list = json.loads(json_str)

                        # 各コース情報を表示
                        for course in course_list:
                            with st.container():
                                st.subheader(course.get('コース名', 'コース名不明'))
                                st.write(f"提供元: {course.get('提供元', '不明')}")
                                st.write(f"内容: {course.get('内容', '不明')}")
                                st.markdown("---")  # 区切り線

                    except json.JSONDecodeError as e:
                        st.error(f"JSONのパースエラー: {e}")
                else:
                    st.error("JSON形式のデータが見つかりませんでした。")
            else:
                st.error(f"APIリクエストに失敗しました。ステータスコード: {response.status_code}")
        except Exception as e:
            st.error(f"リクエストエラー: {e}")
    else:
        st.warning('キャリア目標を入力してください。')
