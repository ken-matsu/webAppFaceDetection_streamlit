import streamlit as st
import requests
import io
from PIL import Image, ImageDraw, ImageFont

st.title("顔認識アプリ")

subscription_key = "c89d891d7278422394b6498db023583e"
assert subscription_key

face_api_url = 'https://20210825ken.cognitiveservices.azure.com/face/v1.0/detect'

#画像を入れる場所の作成
uploaded_file = st.file_uploader("Chose an image...", type = "jpg")
if uploaded_file is not None:
    img = Image.open(uploaded_file)

    with io.BytesIO() as output:
        img.save(output, format="JPEG")
        binary_img = output.getvalue() #バイナリーデータを取得
    headers = {
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": subscription_key
    }
    params = {
        "returnFaceID": "ture",
        "returnFaceAttributes": "age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise"
    }

    res = requests.post(face_api_url, params=params, headers=headers, data = binary_img)
    results = res.json()
    font = ImageFont.truetype("arial.ttf", 64)

    for result in results:
        rect = result['faceRectangle']
        draw = ImageDraw.Draw(img)
        draw.rectangle([(rect["left"], rect["top"]), (rect["left"]+rect["width"], rect["top"]+rect["height"])], fill =None, outline = "green", width = 5)
        
        text_gender = "sex: "+result['faceAttributes']["gender"]
        text_age = "age: "+str(int(result['faceAttributes']["age"])) 
        size_gender = font.getsize(text_gender)
        size_age = font.getsize(text_age)
        imagesize = img.size
        if rect["top"]-(size_gender[1]*2) < 0:
            draw.text((rect["left"], rect["top"]+(size_gender[1]*2)), text_gender, font=font, fill="white", stroke_width=5, stroke_fill="black" )
            draw.text((rect["left"], rect["top"]+size_gender[1]), text_age, font=font, fill="white", stroke_width=5, stroke_fill="black" )
        elif rect["left"] + size_gender[0] > imagesize[0]:
            hami = rect["left"] + size_gender[0] - imagesize[0]
            draw.text((rect["left"] - hami, rect["top"]-(size_gender[1]*2)), text_gender, font=font, fill="white", stroke_width=5, stroke_fill="black" )
            draw.text((rect["left"] - hami, rect["top"]-size_gender[1]), text_age, font=font, fill="white", stroke_width=5, stroke_fill="black" )        
        else:
            draw.text((rect["left"], rect["top"]-(size_gender[1]*2)), text_gender, font=font, fill="white", stroke_width=5, stroke_fill="black" )
            draw.text((rect["left"], rect["top"]-size_gender[1]), text_age, font=font, fill="white", stroke_width=5, stroke_fill="black" )


    st.image(img, caption = "Uploaded Image.", use_column_width=True)




#↓勉強用↓
#import pandas as pd
#import numpy as np
#st.write("データフレーム")
#st.write(
#    pd.DataFrame({
#        "1st column": [1, 2, 3, 4],
#        "2nd column": [10, 20, 30, 40]
#    })
#)

#"""
## My 1st App
### マジックコマンド
#こんな感じでマジックコマンドを使用できる。Markdown対応。
#"""

#if st.checkbox("Show DataFrame"):
#    chart_df = pd.DataFrame(
#        np.random.randn(20, 3),
#        columns = ["a", "b", "c"]
#    )
#    st.line_chart(chart_df)