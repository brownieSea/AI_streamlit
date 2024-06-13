import streamlit as st
from PIL import Image

# 사이드바 화면 (화면 분할)
st.sidebar.title("SideBar")
st.sidebar.subheader("login")
userID = st.sidebar.text_input("ID : ", value="streamlit", max_chars=15)
userPW = st.sidebar.text_input("PW : ", value="12345", max_chars=15, type='password')

st.sidebar.subheader("SelectBox")
sel_opt = ["진주 귀걸이를 한 소녀", '별이 빛나는 밤에', '절규', '월하정인']
user_opt = st.sidebar.selectbox("Favorite Picture : ", sel_opt, index=None, placeholder="Choose favorite pic...")
# st.sidebar.write("Choosed : ", user_opt)

# 메인화면
st.title("스트림릿의 사이드바")
folder = 'data/'
image_files = ['Vermeer.png', 'Gogh.png', 'Munch.png', 'ShinYoonbok.png']

#선택한 항목에 맞는 이미지 파일
if user_opt:
    sel_img_index = sel_opt.index(user_opt)
    img_file = image_files[sel_img_index]
    img_local = Image.open(f'{folder}{img_file}')
    st.subheader(f"{user_opt}")
    st.image(img_local, caption=user_opt)
else:
    st.header("좌측 메뉴에서 그림을 선택해주세요")
