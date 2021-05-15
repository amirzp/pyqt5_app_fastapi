from sqlalchemy import Boolean, Column, Integer, String
# from sqlalchemy.orm import relationship
from database.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String)
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=True)
    password = Column(String, index=True)

    # items = relationship("ContactModel", back_populates="owner")
