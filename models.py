from datetime import datetime, timezone
from sqlmodel import Field, SQLModel, create_engine
from typing import Optional
import os
from data.catalog import all_skills, CAREER_PATHS
DB_URL=os.getenv('DATABASE_URL','sqlite:///careerx.db')
engine=create_engine(DB_URL,connect_args={'check_same_thread':False} if DB_URL.startswith('sqlite') else {})
def utcnow(): return datetime.now(timezone.utc)
class Skill(SQLModel,table=True):
 id:Optional[int]=Field(default=None,primary_key=True); name:str=Field(index=True); category:str; description:str=''; proficiency:int=0; certificate_path:Optional[str]=None; updated_at:datetime=Field(default_factory=utcnow)
class Career(SQLModel,table=True):
 id:Optional[int]=Field(default=None,primary_key=True); title:str=Field(index=True); level:str; skills:str=''; salary_range:str=''; demand:str='Growing'; resources:str=''
class Roadmap(SQLModel,table=True):
 id:Optional[int]=Field(default=None,primary_key=True); goal:str; steps:str; status:str='active'; updated_at:datetime=Field(default_factory=utcnow)
class Job(SQLModel,table=True):
 id:Optional[int]=Field(default=None,primary_key=True); external_id:str=Field(index=True); title:str; company:str; location:str=''; url:str; source:str=''; remote:bool=False; salary:str=''; posted_at:Optional[str]=None; updated_at:datetime=Field(default_factory=utcnow)
class Application(SQLModel,table=True):
 id:Optional[int]=Field(default=None,primary_key=True); job_id:Optional[int]=None; company:str; title:str; stage:str='Saved'; applied_on:Optional[str]=None; salary:str=''; notes:str=''; follow_up:Optional[str]=None; updated_at:datetime=Field(default_factory=utcnow)
class Resume(SQLModel,table=True):
 id:Optional[int]=Field(default=None,primary_key=True); name:str; template:str; content:str=''; ats_score:int=0; updated_at:datetime=Field(default_factory=utcnow)
class PendingSync(SQLModel,table=True):
 id:Optional[int]=Field(default=None,primary_key=True); table_name:str; record_id:str; operation:str; payload:str; created_at:datetime=Field(default_factory=utcnow)
def init_db():
 SQLModel.metadata.create_all(engine)
 from sqlmodel import Session,select
 with Session(engine) as session:
  existing={(x.name,x.category) for x in session.exec(select(Skill)).all()}
  for name,category in all_skills():
   if (name,category) not in existing: session.add(Skill(name=name,category=category))
  existing_careers={x.title for x in session.exec(select(Career)).all()}
  for title,level,skills in CAREER_PATHS:
   if title not in existing_careers: session.add(Career(title=title,level=level,skills=skills,resources='Official documentation, projects, certifications, and peer review'))
  session.commit()
