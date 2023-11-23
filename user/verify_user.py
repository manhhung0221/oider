import logging
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from manage_engine import engine_public
from user.model_user import User

# Cấu hình logging
logging.basicConfig(filename='user_verification.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Tạo một session factory, được gắn với engine
session_factory = sessionmaker(bind=engine_public)
# Tạo một scoped session
ScopedSession = scoped_session(session_factory)

def verify_user(phone_number, password):
    session = ScopedSession()  # Tạo một session mới
    try:
        # Truy vấn để tìm người dùng dựa trên số điện thoại
        user_to_verify = session.query(User).filter_by(phone_number=phone_number).first()
        # Kiểm tra xem người dùng có tồn tại và mật khẩu có hợp lệ
        if user_to_verify and user_to_verify.verify_password(password):
            return True
        else:
            return False
    except SQLAlchemyError as e:
        # Log lỗi sử dụng logging
        logging.error(f"An error occurred during user verification: {e}")
        return False
    finally:
        ScopedSession.remove()  # Đảm bảo rằng session được loại bỏ sau khi sử dụng

