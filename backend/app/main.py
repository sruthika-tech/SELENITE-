from fastapi import FastAPI,Depends,HTTPException,Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import Base,engine,get_db
from app.models import *
from app.schemas.core import Register,Login,ProgressIn,SkillIn,ResumeIn,ChatIn
from app.seed import seed,PHASES,MAP
from app.auth import hash_password,verify_password,token_for,current_user
from app.services.intelligence import roadmap,analyze_resume,answer
app=FastAPI(title='Selenite Career Intelligence API',version='2.0.0')
app.add_middleware(CORSMiddleware,allow_origins=['*'],allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
@app.on_event('startup')
def startup(): seed()
@app.get('/')
def root(): return {'name':'Selenite','version':'2.0.0','status':'online','docs':'/docs'}
@app.get('/health')
def health(): return {'status':'healthy'}
@app.post('/api/auth/register')
def register(x:Register,db:Session=Depends(get_db)):
 if db.query(User).filter(User.email==x.email).first(): raise HTTPException(409,'Email already registered')
 u=User(name=x.name,email=x.email,password_hash=hash_password(x.password),target_career=x.target_career,level=x.level);db.add(u);db.commit();db.refresh(u);return {'access_token':token_for(u),'token_type':'bearer','user':{'id':u.id,'name':u.name,'email':u.email,'target_career':u.target_career,'level':u.level}}
@app.post('/api/auth/login')
def login(x:Login,db:Session=Depends(get_db)):
 u=db.query(User).filter(User.email==x.email).first()
 if not u or not verify_password(x.password,u.password_hash): raise HTTPException(401,'Invalid email or password')
 return {'access_token':token_for(u),'token_type':'bearer','user':{'id':u.id,'name':u.name,'email':u.email,'target_career':u.target_career,'level':u.level}}
@app.get('/api/me')
def me(u:User=Depends(current_user)): return {'id':u.id,'name':u.name,'email':u.email,'target_career':u.target_career,'level':u.level}
@app.get('/api/careers')
def careers(search:str|None=None,db:Session=Depends(get_db)):
 q=db.query(Career)
 if search:q=q.filter(or_(Career.name.ilike(f'%{search}%'),Career.category.ilike(f'%{search}%')))
 return [{'slug':c.slug,'name':c.name,'category':c.category,'description':c.description,'level':c.level} for c in q.all()]
@app.get('/api/careers/{slug}')
def career(slug:str,db:Session=Depends(get_db)):
 c=db.query(Career).filter_by(slug=slug).first()
 if not c: raise HTTPException(404,'Career not found')
 skills=[db.get(Skill,x.skill_id) for x in c.skills];tools=[db.get(Tool,x.tool_id) for x in c.tools]
 return {'slug':c.slug,'name':c.name,'category':c.category,'description':c.description,'level':c.level,'skills':[s.name for s in skills],'tools':[t.name for t in tools],'roadmap':roadmap(c.slug)}
@app.get('/api/skills')
def skills(search:str|None=None,db:Session=Depends(get_db)):
 q=db.query(Skill)
 if search:q=q.filter(Skill.name.ilike(f'%{search}%'))
 return [{'slug':s.slug,'name':s.name,'category':s.category,'difficulty':s.difficulty,'description':s.description} for s in q.all()]
@app.get('/api/tools')
def tools(search:str|None=None,db:Session=Depends(get_db)):
 q=db.query(Tool)
 if search:q=q.filter(Tool.name.ilike(f'%{search}%'))
 return [{'slug':t.slug,'name':t.name,'category':t.category,'difficulty':t.difficulty,'description':t.description} for t in q.all()]
@app.get('/api/roadmaps/{career_slug}')
def get_roadmap(career_slug:str): return {'career':career_slug,'phases':roadmap(career_slug)}
@app.get('/api/progress')
def get_progress(u:User=Depends(current_user),db:Session=Depends(get_db)):
 rows=db.query(Progress).filter_by(user_id=u.id).all();return [{'career_slug':r.career_slug,'phase_index':r.phase_index,'completed':r.completed} for r in rows]
@app.post('/api/progress')
def set_progress(x:ProgressIn,career_slug:str=Query(...),u:User=Depends(current_user),db:Session=Depends(get_db)):
 r=db.query(Progress).filter_by(user_id=u.id,career_slug=career_slug,phase_index=x.phase_index).first()
 if not r:r=Progress(user_id=u.id,career_slug=career_slug,phase_index=x.phase_index,completed=x.completed);db.add(r)
 else:r.completed=x.completed
 db.commit();return {'ok':True}
@app.post('/api/me/skills')
def add_skill(x:SkillIn,u:User=Depends(current_user),db:Session=Depends(get_db)):
 s=db.query(Skill).filter_by(slug=x.skill_slug).first()
 if not s: raise HTTPException(404,'Skill not found')
 r=db.query(UserSkill).filter_by(user_id=u.id,skill_id=s.id).first()
 if not r:r=UserSkill(user_id=u.id,skill_id=s.id);db.add(r)
 r.level=max(0,min(5,x.level));db.commit();return {'ok':True}
@app.get('/api/me/skills')
def myskills(u:User=Depends(current_user),db:Session=Depends(get_db)):
 rows=db.query(UserSkill,Skill).join(Skill,UserSkill.skill_id==Skill.id).filter(UserSkill.user_id==u.id).all();return [{'slug':s.slug,'name':s.name,'level':r.level} for r,s in rows]
@app.get('/api/jobs')
def jobs(q:str|None=None,location:str|None=None,kind:str|None=None,db:Session=Depends(get_db)):
 rows=db.query(Job)
 if q:rows=rows.filter(or_(Job.title.ilike(f'%{q}%'),Job.skills.ilike(f'%{q}%')))
 if location:rows=rows.filter(Job.location.ilike(f'%{location}%'))
 if kind:rows=rows.filter(Job.kind.ilike(f'%{kind}%'))
 return [vars_out(j,['id','title','company','location','kind','skills','experience','posted','source_url','demo']) for j in rows.all()]
@app.get('/api/events')
def events(db:Session=Depends(get_db)): return [vars_out(e,['id','title','kind','location','date','url','free','demo']) for e in db.query(Event).all()]
@app.get('/api/news')
def news(db:Session=Depends(get_db)): return [vars_out(n,['id','title','source','category','published','summary','url','demo']) for n in db.query(News).all()]
@app.get('/api/market')
def market(role:str|None=None,region:str|None=None,db:Session=Depends(get_db)):
 q=db.query(MarketTrend)
 if role:q=q.filter(MarketTrend.role.ilike(f'%{role}%'))
 if region:q=q.filter(MarketTrend.region.ilike(f'%{region}%'))
 return [vars_out(x,['role','skill','region','period','demand_index','sample_size','source']) for x in q.all()]
@app.get('/api/skill-gap')
def gap(u:User=Depends(current_user),db:Session=Depends(get_db)):
 c=u.target_career or 'soc-analyst'; required=MAP.get(c,[]); have=[s.name for r,s in db.query(UserSkill,Skill).join(Skill,UserSkill.skill_id==Skill.id).filter(UserSkill.user_id==u.id).all()]; return {'career':c,'required':required,'current':have,'missing':[x for x in required if x.lower() not in [h.lower() for h in have]]}
@app.post('/api/resume/analyze')
def resume(x:ResumeIn,u:User=Depends(current_user),db:Session=Depends(get_db)):
 required=MAP.get(x.target_role,MAP['soc-analyst']); result=analyze_resume(x.text,x.target_role,required); db.add(Resume(user_id=u.id,target_role=x.target_role,text=x.text,analysis=str(result)));db.commit();return result
@app.post('/api/ai/chat')
def chat(x:ChatIn,u:User=Depends(current_user)): return answer(x.message,u.target_career or 'soc-analyst',[])
@app.get('/api/notifications')
def notifications(u:User=Depends(current_user),db:Session=Depends(get_db)): return [vars_out(n,['id','title','body','read','created_at']) for n in db.query(Notification).filter_by(user_id=u.id).all()]
def vars_out(obj,fields): return {f:getattr(obj,f) for f in fields}
from app.services.connectors import refresh_news
@app.post('/api/admin/news/refresh')
def admin_news_refresh(db:Session=Depends(get_db)):
    return {'added':refresh_news(db)}
