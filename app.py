import streamlit as st
import google.generativeai as genai
import os

st.title('YouTube Video Title & Description Generator')

st.write('Paste your video script or summary below:')

user_input = st.text_area('Script or Summary', height=200)

api_key = st.text_input('Enter your Gemini API Key', type='password')

generate = st.button('Generate')

title = ''
description = ''

if generate and user_input and api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
You are a YouTube content strategist. Given the following video script or summary, generate:
1. A catchy, keyword-rich YouTube video title (max 70 characters, avoid clickbait, maximize curiosity and clarity, include main keyword).
2. An SEO-optimized YouTube video description (1-2 paragraphs, include relevant keywords, a call to action, and 2-3 relevant hashtags at the end).

Script/Summary:
{user_input}

Respond in this format:
Title: <your title here>
Description: <your description here>
"""
        response = model.generate_content(prompt)
        # Parse response
        if response and response.text:
            lines = response.text.split('\n')
            title_line = next((l for l in lines if l.lower().startswith('title:')), '')
            desc_lines = [l for l in lines if not l.lower().startswith('title:')]
            title = title_line.replace('Title:', '').strip()
            description = '\n'.join([l.replace('Description:', '').strip() for l in desc_lines if l.strip()])
        else:
            title = 'No response from Gemini API.'
            description = ''
    except Exception as e:
        title = 'Error generating content.'
        description = str(e)

st.subheader('Generated Title')
st.write(title)

st.subheader('Generated Description')
st.write(description) 