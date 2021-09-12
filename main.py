import streamlit as st
from PIL import Image

import cv2
import numpy as np

import tempfile

#適応的2値化処理
def threshold(src, ksize=3, c=2):
    
    # 局所領域の幅
    d = int((ksize-1)/2)

    # 画像の高さと幅
    h, w = src.shape[0], src.shape[1]
    
    # 出力画像用の配列（要素は全て255）
    dst = np.empty((h,w))
    dst.fill(255)
    
    # 局所領域の画素数
    N = ksize**2

    for y in range(0, h):
        for x in range(0, w):
            # 局所領域内の画素値の平均を計算し、閾値に設定
            t = np.sum(src[y-d:y+d+1, x-d:x+d+1]) / N

            # 求めた閾値で二値化処理
            if(src[y][x] < t - c): dst[y][x] = 0
            else: dst[y][x] = 255

    return dst
    

st.title('スマホで撮影した書類写真をくっきりと白黒化するWebアプリ！')
'''
## 影がかかっている写真であってもクッキリとした白黒画像に変換できる

スマホで書類の写真を撮影する際に、影がかかってしまうことがある。
通常の白黒化処理では特定の画素が「この閾値より黒っぽかったら黒！」と決め打ちするため、影のかかった部分は黒として判定されてしまい、下の添付画像のように汚くなってしまうことが頻繁にある。
そのような写真であっても、適応的二値化処理を用いることで、影を取り除いたクッキリとした白黒画像が生成される。

適応的二値化処理（AdaptiveThreshold）とは白か黒かの閾値を固定せず、画素ごとに自分の周囲の画素を参考にして白か黒かを判断する二値化処理のことで、陰影を取り除くのに適している。
'''
st.image("siroku.jpg",caption ="一般的な白黒化",use_column_width=True)
st.image("sirokuro.jpg",caption ="適応的2値化処理を用いた白黒化",use_column_width=True)


uploaded_file = st.file_uploader("jpg画像を選択してください",type = "jpg")
if uploaded_file is not None:
    #img = Image.open(uploaded_file)#imgはPillow型
    #uploaded_fileをcv2.imreadで読み取れるようにする処理
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    #検索の受け売りなので、どうしてtempfileを使うとuploaded_fileをcv2.imreadしたときにエラーがでなくなるのかわからない
    img = cv2.imread(tfile.name)
    #一度cv2.imwriteを使わないと、st.imageしたときにエラーが出る
    cv2.imwrite('temp.jpg',img)
    st.image('temp.jpg',caption ="アップロードされた画像",use_column_width=True)
    #これも検索の受け売り。なぜcv2.imwriteしてから指定した'temp.jpg'をst.imageするとうまくいくのかわからない
    st.title("↓に白黒化画像が表示されます")
    # グレースケール変換
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)#grayはopenCV型
    # 方法1
    dst = threshold(gray, ksize=11, c=13)
    cv2.imwrite('temporary.jpg', dst)
    st.image('temporary.jpg',caption ="適応的2値化処理で白黒化された画像",use_column_width=True)





