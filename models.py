import os
from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine

DB_URL = os.getenv('DATABASE_URL', 'sqlite:///careerx.db')
engine = create_engine(DB_URL, connect_args={'check_same_thread': False} if DB_URL.startswith('sqlite') else {})

def utcnow(): return datetime.now(timezone.utc)

class Skill(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    category: str
    description: str = ''
    proficiency: int = 0
    certificate_path: Optional[str] = None
    updated_at: datetime = Field(default_factory=utcnow)

class Career(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    level: str
    skills: str = ''
    salary_range: str = ''
    demand: str = 'Growing'
    resources: str = ''

class Roadmap(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    goal: str
    steps: str
    status: str = 'active'
    updated_at: datetime = Field(default_factory=utcnow)

class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    external_id: str = Field(index=True)
    title: str
    company: str
    location: str = ''
    url: str
    source: str = ''
    remote: bool = False
    salary: str = ''
    posted_at: Optional[str] = None
    updated_at: datetime = Field(default_factory=utcnow)

class Application(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: Optional[int] = None
    company: str
    title: str
    stage: str = 'Saved'
    applied_on: Optional[str] = None
    salary: str = ''
    notes: str = ''
    follow_up: Optional[str] = None
    updated_at: datetime = Field(default_factory=utcnow)

class Resume(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    template: str
    content: str = ''
    ats_score: int = 0
    updated_at: datetime = Field(default_factory=utcnow)

class PendingSync(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    table_name: str
    record_id: str
    operation: str
    payload: str
    created_at: datetime = Field(default_factory=utcnow)

def init_db():
    SQLModel.metadata.create_all(engine)
    from sqlmodel import Session, select
    with Session(engine) as session:
        if not session.exec(select(Skill)).first():
            for category, names in {'Software Engineering':['Python','FastAPI','SQL','Git'], 'Data Science & AI':['Python','Machine Learning','Prompt Engineering'], 'Cloud & DevOps':['AWS','Docker','Kubernetes'], 'Cybersecurity':['Networking','Threat Modeling'], 'Product Management':['Product Strategy','User Research']}.items():
                session.add_all([Skill(name=n, category=category) for n in names])
        if not session.exec(select(Career)).first():
            session.add_all([Career(title=t, level=l, skills=s, salary_range=r, demand=d, resources='Official documentation, projects, and peer review') for t,l,s,r,d in [
                ('AI Engineer','Junior → Senior','Python, ML, LLM APIs','$70k–$180k','Very high'), ('Full-Stack Developer','Junior → Lead','Python, FastAPI, SQL, UI','$60k–$160k','High'), ('Data Scientist','Junior → Principal','Python, Statistics, ML','$65k–$170k','High'), ('Cloud Architect','Mid → Principal','AWS, Docker, Kubernetes','$100k–$220k','Growing'), ('Product Manager','Associate → Director','Strategy, Research, Analytics','$70k–$190k','Steady')]])
        session.commit()
