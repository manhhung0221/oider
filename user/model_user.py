from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
Base = declarative_base()
class User(Base):
    __tablename__ = 'user_reg'

    phone_number = Column(String(20), primary_key=True, nullable=False)
    password = Column(String(255), nullable=False)
    broker_id = Column(Integer, nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)
