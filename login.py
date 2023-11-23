import streamlit as st
from user.verify_user import verify_user

# Giả sử bạn đã có hàm verify_user như đã xây dựng ở trên

# Phần đăng nhập
def login_user():
    
    with st.form("login_form"):
        phone_number = st.text_input("Phone Number")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")
        
        if login_button:
            # Xác thực người dùng
            if verify_user(phone_number, password):
                # Nếu xác thực thành công, thiết lập session state
                st.session_state['logged_in'] = True
                st.session_state['phone_number'] = phone_number
                st.success("Logged in successfully!")
                st.experimental_rerun()
                
            else:
                st.error("Invalid phone number or password")

# Phần đăng xuất
def logout_user():
    if 'logged_in' in st.session_state:
        del st.session_state['logged_in']
        del st.session_state['phone_number']
    st.info("Logged out successfully!")

# # Trong main của ứng dụng
# if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
#     login_user()  # Hiển thị form đăng nhập nếu chưa đăng nhập
# else:
#     # Hiển thị nội dung của ứng dụng
#     st.write(f"Welcome, user {st.session_state['phone_number']}!")

#     if st.button("Logout"):
#         logout_user()  # Xử lý khi người dùng nhấn nút đăng xu
