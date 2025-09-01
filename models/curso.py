from sqlalchemy import Column, Integer, String, Text
from core.database import Base
class Cursos(Base):
    __tablename__ ='cursos' 
    
    idcursos = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nomecursos = Column(String(255), nullable=False)
    descricaocursos = Column(Text,nullable=False,index=True)
