from sqlalchemy import Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship
from database.database import Base


class ContactModel(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    family = Column(String, index=True)
    phone = Column(String, index=True)
    email = Column(String, index=True)
    user = Column(Integer, ForeignKey("users.id"))

    # owner = relationship("UserModel", back_populates="items")
