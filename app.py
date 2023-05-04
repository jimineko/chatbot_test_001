
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": st.secrets.AppSettings.prompt_setting}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.8
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    # 入力欄を消去
    st.session_state["user_input"] = ""


# チャットボットの出力結果をmarp形式のマークダウンファイルに変換する関数
def convert(slides):
    header_str = """---
marp: true
_theme: gaia
paginate: true
backgroundColor: #f5f5f5"
"""

    output_str = header_str + slides
    return output_str

# ユーザーインターフェイスの構築
# タイトル＆サイト説明を記載
st.title("教えて！ニャンコ先生")
st.image("nyanko.jpg")
st.write("ニャンコ先生が美容業界に関するお題について、プレゼン資料を自動生成してくれるWebサービスです。")

# ユーザー入力欄を作成
user_input_title = st.text_input("スライドの題名を入力してください。", key="user_input_title", placeholder="例：東京と大阪の違いから見るネイルサロンのトレンドと今後の展望")
user_input_content = st.text_area("どのようなスライドを作成したいか入力してください。", key="user_input_content", placeholder="例：東京と大阪のそれぞれの地域でのネイルサロンのトレンドについて説明する。また、その差異から、今後の大阪でのネイルサロン運営におけるトレンド分析を行なってください。")
text_contents=""

# ユーザー入力の確定ボタン
if st.button("プレゼン資料の作成開始"):
    st.write("🐈：礼は七辻屋の饅頭でいいぞ！少々待つのじゃ(右上のRunningが消えるまで)")
    # ユーザー入力を結合
    st.session_state["user_input"] = "#スライドの題名:" + user_input_title + "¥r¥n" + "#スライドの内容:" + user_input_content + "¥r¥n"
    communicate()

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        if message["role"]=="assistant":
            st.write(message["content"])
            text_contents=convert(message["content"])

# 出力結果のダウンロードボタン
# st.download_button('Download Result', text_contents)
st.download_button(label="Download", data=text_contents, file_name="slide.md")
