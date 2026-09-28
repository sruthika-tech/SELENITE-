from pydantic import BaseModel,EmailStr
class Register(BaseModel): name:str; email:EmailStr; password:str; target_career:str|None=None; level:str='Beginner'
class Login(BaseModel): email:EmailStr; password:str
class ProgressIn(BaseModel): phase_index:int; completed:bool
class SkillIn(BaseModel): skill_slug:str; level:int=1
class ResumeIn(BaseModel): target_role:str; text:str
class ChatIn(BaseModel): message:str
