from user.model_user import User
from sqlalchemy.orm import sessionmaker
from manage_engine import engine_public
Session = sessionmaker(bind=engine_public)
session = Session()
# Tạo một instance mới của class User
new_user = User(phone_number='0359052501',broker_id='00001')
new_user.set_password('manhhung')  # Mật khẩu sẽ được băm trong hàm set_password

# Tiếp theo, bạn sẽ thêm new_user vào session và commit để lưu trữ trong cơ sở dữ liệu
session.add(new_user)
session.commit()


