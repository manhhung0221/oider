import streamlit as st
from login import login_user, logout_user  # Giả sử đây là nơi bạn định nghĩa các hàm login_user và logout_user
from app_st.app_OI_reTicker import OI

# Kiểm tra xem người dùng đã đăng nhập hay chưa
def main():
    # Kiểm tra nếu người dùng đã đăng nhập, chuyển hướng họ đến ứng dụng
    if 'logged_in' in st.session_state and st.session_state['logged_in']:
        st.set_page_config(layout="wide")
        OI()
    else:
        login_user()  # Hiển thị form đăng nhập nếu chưa đăng nhập
        
if __name__ == "__main__":
    main()
