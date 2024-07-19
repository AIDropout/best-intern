"""Models for this app."""

from datetime import date
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class _Education(BaseModel):
    institution: str
    degree: str
    field_of_study: str
    start_date: date
    end_date: Optional[date] = None
    gpa: Optional[float] = None
    relevant_courses: Optional[List[str]] = None


class _Experience(BaseModel):
    job_title: str
    company: str
    location: str
    start_date: date
    end_date: Optional[date] = None
    description: Optional[str] = None


class _Project(BaseModel):
    title: str
    description: Optional[str] = None
    technologies_used: Optional[List[str]] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class _Certification(BaseModel):
    name: str
    issuing_organization: str
    issue_date: date
    expiration_date: Optional[date] = None
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None


class _ExtracurricularActivity(BaseModel):
    name: str
    position: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class ResumeMetadata(BaseModel):
    name: str
    email: EmailStr
    phone: str
    summary: Optional[str] = None
    skills: List[str]
    education: List[_Education]
    experience: List[_Experience]
    internships: Optional[List[_Experience]] = None
    certifications: Optional[List[_Certification]] = None
    projects: Optional[List[_Project]] = None
    languages: Optional[List[str]] = None
    extracurricular_activities: Optional[List[_ExtracurricularActivity]] = None
    awards: Optional[List[str]] = None


class JobMetadata(BaseModel):
    job_title: str
    company: str
    location: str
    skills_required: List[str]
    education_required: Optional[List[str]] = None
    experience_required: Optional[List[str]] = None
    job_description: str
    salary_range: Optional[str] = None
    job_type: str
    application_url: str
    posted_date: Optional[date] = None
    deadline: Optional[date] = None
    company_size: Optional[str] = None
    industry: Optional[str] = None
    benefits: Optional[List[str]] = None
    remote: Optional[bool] = None
