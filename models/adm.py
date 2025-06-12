from sqlalchemy import Column, Integer, String, Text
from core.database import Base
class adm(Base):
    __tablename__ ='adm' 
    
    idadm = Column(Integer, primary_key=True, index=True, autoincrement=True)
    senhaadm = Column(String(255), nullable=False, unique=True)
    nomeadm = Column(String(255), nullable=False, unique=True,index=True)
