from sqlalchemy import Column, Integer, String, Text
from core.database import Base
class usuario(Base):
    __tablename__ ='usuario' 
    
    idusuario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nomeusuario = Column(String(255), nullable=False, index=True)
    