import streamlit as st
import time
import random
import json
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

with open('talor.json') as talor_file:
  file_contents = talor_file.read()
des_dict = json.loads(file_contents)

st.set_page_config(
    page_title="塔罗牌",
    page_icon="🔮",
    layout="centered",
)

st.write("## 塔罗牌占卜小游戏 🔮")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    请抽取卡牌， 来探寻自己吧 ❤️
"""
)

def add_message(role, content, delay=0.05):
    with st.chat_message(role):
        message_placeholder = st.empty()
        full_response = ""

        for chunk in list(content):
            full_response += chunk + ""
            time.sleep(delay)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

def get_card_number():
    return random.randint(1, 21)

def get_card_situation():
    return random.randint(0, 1)

def format_result(card_name, card_situation):
    return "翻出的塔罗牌为" + card_name + "-" + f"{ '正位' if card_situation == 1 else '倒位'}"

if st.button('请抽取塔罗牌'):
    result_arr = []
    
    for i in range(5):
        card_num = get_card_number()
        card_situation = get_card_situation()
        card_info = des_dict[f"{card_num}"]
        print(card_info)
        card_name = card_info['name']
        print(card_name)
        if card_situation == 0:
            card_desc = card_info['downDes']
        else:
            card_desc = card_info['upDes']
        add_message("assistant", format_result(card_name, card_situation))
        result_arr.append(card_desc)

    with st.spinner('加载解读中，请稍等 ......'):
        response = openai.ChatCompletion.create(
            model="gpt35",
            messages = [{"role":"system","content":"你是一位 Tarot cards 占卜师，采用 Taro Cross Spread 解读，你的任务是根据牌中展示的含义，解读被占卜者的过去，现状和未来。你的解答应基于对塔罗牌的理解，同时也要尽可能地展现出乐观和积极的态度，引导被占卜者朝着积极的方向发展。"},
                        {"role":"user","content":f"""
                            A位代表过去的状况，对应的牌展示的含义是：{result_arr[0]},
                            B位代表现在的状况，对应的牌展示的含义是：{result_arr[1]},
                            C位代表将来的状况，对应的牌展示的含义是：{result_arr[2]},
                            D位代表周遭的状况，对应的牌展示的含义是：{result_arr[3]},
                            E位代表应该怎么做，对应的牌展示的含义是：{result_arr[4]},"""
                        }],
            temperature=0.7,
            max_tokens=500,
            top_p=0.95,
            frequency_penalty=0.5,
            presence_penalty=0.1,
            stop=None)
    add_message("assistant", response.choices[0].message.content)
    time.sleep(0.1)
