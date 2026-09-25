"""CareerX / Maccy Hub database models and seed data."""
import os
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select

from data.catalog import CAREER_PATHS, all_skills

DB_URL = os.getenv("DATABASE_URL", "sqlite:///careerx.db")
engine = create_engine(
    DB_URL,
    connect_args={"check_same_thread": False} if DB_URL.startswith("sqlite") else {},
)


def utcnow():
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    name: str = ""
    password_hash: str
    created_at: datetime = Field(default_factory=utcnow)


class Skill(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, index=True)
    name: str = Field(index=True)
    category: str
    description: str = ""
    proficiency: int = 0
    certificate_path: Optional[str] = None
    updated_at: datetime = Field(default_factory=utcnow)


class Career(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    level: str
    skills: str = ""
    salary_range: str = ""
    demand: str = "Growing"
    resources: str = ""


class Roadmap(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, index=True)
    goal: str
    steps: str
    status: str = "active"
    updated_at: datetime = Field(default_factory=utcnow)


class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    external_id: str = Field(index=True)
    title: str
    company: str
    location: str = ""
    url: str
    source: str = ""
    remote: bool = False
    salary: str = ""
    posted_at: Optional[str] = None
    updated_at: datetime = Field(default_factory=utcnow)


class Application(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, index=True)
    job_id: Optional[int] = None
    company: str
    title: str
    stage: str = "Saved"
    applied_on: Optional[str] = None
    salary: str = ""
    notes: str = ""
    follow_up: Optional[str] = None
    updated_at: datetime = Field(default_factory=utcnow)


class Resume(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, index=True)
    name: str
    template: str
    content: str = ""
    ats_score: int = 0
    updated_at: datetime = Field(default_factory=utcnow)


class PendingSync(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, index=True)
    table_name: str
    record_id: str
    operation: str
    payload: str
    created_at: datetime = Field(default_factory=utcnow)


def init_db():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        if not session.exec(select(User)).first():
            from services.auth import create_user
            create_user("demo@maccy.com", "Demo User", "careerx123")

        seeded_skills = {(row.name, row.category) for row in session.exec(select(Skill)).all()}
        for name, category in all_skills():
            if (name, category) not in seeded_skills:
                session.add(Skill(name=name, category=category, proficiency=0, user_id=None))

        seeded_careers = {row.title for row in session.exec(select(Career)).all()}
        for title, level, skills in CAREER_PATHS:
            if title not in seeded_careers:
                session.add(
                    Career(
                        title=title,
                        level=level,
                        skills=skills,
                        salary_range="$60k–$200k",
                        demand="Growing",
                        resources="Official documentation, projects, portfolios, and certifications",
                    )
                )

        session.commit()


__all__ = [
    "engine",
    "User",
    "Skill",
    "Career",
    "Roadmap",
    "Job",
    "Application",
    "Resume",
    "PendingSync",
    "init_db",
]
