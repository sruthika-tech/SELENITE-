import re
from app.seed import PHASES,MAP

def roadmap(career, done=None):
 phases=PHASES.get(career,PHASES['soc-analyst']); done=done or []
 return [{'index':i,'name':p,'completed':i in done} for i,p in enumerate(phases)]
def skill_gap(required,user_skills):
 have={x.lower() for x in user_skills}; return [x for x in required if x.lower() not in have]
def analyze_resume(text,target,required):
 low=text.lower(); found=[s for s in required if s.lower() in low]; missing=[s for s in required if s.lower() not in low]
 return {'target_role':target,'found_skills':found,'missing_skills':missing,'projects_suggested':[f'Build a {target} lab using {missing[0]}' if missing else f'Build a portfolio project for {target}'],'note':'Keyword analysis is a development MVP, not an ATS score.'}
def answer(message,career,skills):
 m=message.lower(); required=MAP.get(career,MAP['soc-analyst'])
 if 'next' in m or 'learn' in m: return {'answer':f'For {career.replace("-"," ")}, focus next on {", ".join(required[:3])}. Then practice with a small lab and track it in your roadmap.','links':[{'label':'Open roadmap','path':'roadmap.html'}]}
 if 'gap' in m: return {'answer':f'Your target role is {career.replace("-"," ")}. Compare your current skills against: {", ".join(required)}. Missing skills should become roadmap priorities.','links':[{'label':'Open skills','path':'skills.html'}]}
 return {'answer':f'Selenite can help with {career.replace("-"," ")} by connecting careers, skills, tools, roadmaps, opportunities and progress. Ask me what to learn next, what skills you are missing, or how to prepare for a role.','links':[{'label':'Explore careers','path':'careers.html'}]}
