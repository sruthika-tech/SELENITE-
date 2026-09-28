from datetime import datetime
from sqlalchemy import String,Integer,Boolean,DateTime,ForeignKey,Text,Float
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.database import Base
class Career(Base):
    __tablename__='careers'; id:Mapped[int]=mapped_column(primary_key=True); slug:Mapped[str]=mapped_column(String(100),unique=True,index=True); name:Mapped[str]=mapped_column(String(150)); category:Mapped[str]=mapped_column(String(80)); description:Mapped[str]=mapped_column(Text); level:Mapped[str]=mapped_column(String(50)); skills=relationship('CareerSkill',cascade='all, delete-orphan'); tools=relationship('CareerTool',cascade='all, delete-orphan')
class Skill(Base):
    __tablename__='skills'; id:Mapped[int]=mapped_column(primary_key=True); slug:Mapped[str]=mapped_column(String(100),unique=True,index=True); name:Mapped[str]=mapped_column(String(120)); category:Mapped[str]=mapped_column(String(80)); difficulty:Mapped[str]=mapped_column(String(40)); description:Mapped[str]=mapped_column(Text)
class Tool(Base):
    __tablename__='tools'; id:Mapped[int]=mapped_column(primary_key=True); slug:Mapped[str]=mapped_column(String(100),unique=True,index=True); name:Mapped[str]=mapped_column(String(120)); category:Mapped[str]=mapped_column(String(80)); difficulty:Mapped[str]=mapped_column(String(40)); description:Mapped[str]=mapped_column(Text)
class CareerSkill(Base):
    __tablename__='career_skills'; id:Mapped[int]=mapped_column(primary_key=True); career_id:Mapped[int]=mapped_column(ForeignKey('careers.id')); skill_id:Mapped[int]=mapped_column(ForeignKey('skills.id')); priority:Mapped[str]=mapped_column(String(30),default='Core')
class CareerTool(Base):
    __tablename__='career_tools'; id:Mapped[int]=mapped_column(primary_key=True); career_id:Mapped[int]=mapped_column(ForeignKey('careers.id')); tool_id:Mapped[int]=mapped_column(ForeignKey('tools.id'))
class User(Base):
    __tablename__='users'; id:Mapped[int]=mapped_column(primary_key=True); name:Mapped[str]=mapped_column(String(120)); email:Mapped[str]=mapped_column(String(200),unique=True,index=True); password_hash:Mapped[str]=mapped_column(String(255)); target_career:Mapped[str|None]=mapped_column(String(100)); level:Mapped[str]=mapped_column(String(50),default='Beginner'); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class UserSkill(Base):
    __tablename__='user_skills'; id:Mapped[int]=mapped_column(primary_key=True); user_id:Mapped[int]=mapped_column(ForeignKey('users.id')); skill_id:Mapped[int]=mapped_column(ForeignKey('skills.id')); level:Mapped[int]=mapped_column(Integer,default=0)
class Progress(Base):
    __tablename__='progress'; id:Mapped[int]=mapped_column(primary_key=True); user_id:Mapped[int]=mapped_column(ForeignKey('users.id')); career_slug:Mapped[str]=mapped_column(String(100)); phase_index:Mapped[int]=mapped_column(Integer); completed:Mapped[bool]=mapped_column(Boolean,default=False); updated_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
class Job(Base):
    __tablename__='jobs'; id:Mapped[int]=mapped_column(primary_key=True); title:Mapped[str]=mapped_column(String(200)); company:Mapped[str]=mapped_column(String(150)); location:Mapped[str]=mapped_column(String(150)); kind:Mapped[str]=mapped_column(String(50)); skills:Mapped[str]=mapped_column(Text); experience:Mapped[str]=mapped_column(String(80)); posted:Mapped[str]=mapped_column(String(40)); source_url:Mapped[str]=mapped_column(Text); demo:Mapped[bool]=mapped_column(Boolean,default=True)
class Event(Base):
    __tablename__='events'; id:Mapped[int]=mapped_column(primary_key=True); title:Mapped[str]=mapped_column(String(200)); kind:Mapped[str]=mapped_column(String(80)); location:Mapped[str]=mapped_column(String(120)); date:Mapped[str]=mapped_column(String(50)); url:Mapped[str]=mapped_column(Text); free:Mapped[bool]=mapped_column(Boolean,default=True); demo:Mapped[bool]=mapped_column(Boolean,default=True)
class News(Base):
    __tablename__='news'; id:Mapped[int]=mapped_column(primary_key=True); title:Mapped[str]=mapped_column(String(250)); source:Mapped[str]=mapped_column(String(120)); category:Mapped[str]=mapped_column(String(80)); published:Mapped[str]=mapped_column(String(80)); summary:Mapped[str]=mapped_column(Text); url:Mapped[str]=mapped_column(Text); demo:Mapped[bool]=mapped_column(Boolean,default=True)
class MarketTrend(Base):
    __tablename__='market_trends'; id:Mapped[int]=mapped_column(primary_key=True); role:Mapped[str]=mapped_column(String(120)); skill:Mapped[str]=mapped_column(String(120)); region:Mapped[str]=mapped_column(String(100)); period:Mapped[str]=mapped_column(String(50)); demand_index:Mapped[float]=mapped_column(Float); sample_size:Mapped[int]=mapped_column(Integer); source:Mapped[str]=mapped_column(Text)
class Resume(Base):
    __tablename__='resumes'; id:Mapped[int]=mapped_column(primary_key=True); user_id:Mapped[int]=mapped_column(ForeignKey('users.id')); target_role:Mapped[str]=mapped_column(String(120)); text:Mapped[str]=mapped_column(Text); analysis:Mapped[str]=mapped_column(Text); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class Notification(Base):
    __tablename__='notifications'; id:Mapped[int]=mapped_column(primary_key=True); user_id:Mapped[int]=mapped_column(ForeignKey('users.id')); title:Mapped[str]=mapped_column(String(200)); body:Mapped[str]=mapped_column(Text); read:Mapped[bool]=mapped_column(Boolean,default=False); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
