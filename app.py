import streamlit as st
import requests

# エンドポイントのURL
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

            # responseオブジェクト全体を表示
            st.write("APIレスポンス全体 (responseオブジェクト):")
            st.write(response.text)  # レスポンスのテキストをそのまま表示

            if response.status_code == 200:
                try:
                    # JSONをリストとして解析
                    data = response.json()
                    if isinstance(data, list) and data:  # リスト形式かどうか確認
                        for course in data:
                            with st.container():
                                st.subheader(course.get('コース名', 'コース名不明'))
                                st.write(f"提供元: {course.get('提供元', '不明')}")
                                st.write(f"内容: {course.get('内容', '不明')}")
                                st.markdown("---")  # 区切り線
                    else:
                        st.error("コース情報が見つかりませんでした。")
                except ValueError:
                    st.error("レスポンスがJSON形式ではありません。内容:")
                    st.text(response.text)
            else:
                # ステータスコードが200以外の場合、エラーメッセージの詳細を表示
                try:
                    error_message = response.json()
                    st.error(f"APIリクエストに失敗しました。ステータスコード: {response.status_code}, エラーメッセージ: {error_message}")
                except ValueError:
                    st.error(f"APIリクエストに失敗しました。ステータスコード: {response.status_code}")
        except requests.Timeout:
            st.error("リクエストがタイムアウトしました。時間をおいて再試行してください。")
        except Exception as e:
            st.error(f"リクエストエラー: {e}")
    else:
        st.warning('キャリア目標を入力してください。')
