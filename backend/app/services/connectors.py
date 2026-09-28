import os,feedparser,httpx
from sqlalchemy.orm import Session
from app.models import News,Job

def refresh_news(db:Session):
    urls=[x.strip() for x in os.getenv('NEWS_RSS_URLS','').split(',') if x.strip()]
    added=0
    for url in urls:
        try:
            feed=feedparser.parse(url)
            for e in feed.entries[:30]:
                link=getattr(e,'link','')
                title=getattr(e,'title','Cybersecurity advisory')
                if not link or db.query(News).filter(News.url==link).first(): continue
                summary=getattr(e,'summary','')[:1000]
                db.add(News(title=title,source=getattr(feed.feed,'title','RSS'),category='Cybersecurity',published=getattr(e,'published',''),summary=summary,url=link,demo=False));added+=1
        except Exception:
            continue
    db.commit(); return added

def refresh_jobs_json(db:Session,url:str):
    r=httpx.get(url,timeout=15);r.raise_for_status();data=r.json();added=0
    for j in data:
        link=j.get('source_url') or j.get('url')
        if not link or db.query(Job).filter(Job.source_url==link).first(): continue
        db.add(Job(title=j.get('title','Security role'),company=j.get('company',''),location=j.get('location',''),kind=j.get('kind','Full-time'),skills=', '.join(j.get('skills',[])) if isinstance(j.get('skills'),list) else j.get('skills',''),experience=j.get('experience',''),posted=j.get('posted',''),source_url=link,demo=False));added+=1
    db.commit();return added
