"""Models for this app."""

from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class _Education(BaseModel):
    institution: Optional[str] = Field(
        description="Name of the educational institution."
    )
    degree: Optional[str] = Field(description="Degree or certification obtained.")
    field_of_study: Optional[str] = Field(description="Field of study.")
    start_date: Optional[date] = Field(description="Start date of education.")
    end_date: Optional[date] = Field(
        description="End date or expected graduation date."
    )
    gpa: Optional[str | float] = Field(description="Grade Point Average.")


class _Experience(BaseModel):
    job_title: Optional[str] = Field(description="Job title.")
    company: Optional[str] = Field(description="Company name.")
    location: Optional[str] = Field(description="Job location.")
    start_date: Optional[date] = Field(description="Start date of employment.")
    end_date: Optional[date] = Field(description="End date of employment.")
    description: Optional[str] = Field(
        description="Very short description of job responsibilities."
    )


class _Project(BaseModel):
    title: Optional[str] = Field(description="Project title.")
    description: Optional[str] = Field(
        description="Very short description of the project."
    )
    technologies_used: Optional[List[str]] = Field(
        description="Technologies used in the project."
    )


class _ExtracurricularActivity(BaseModel):
    name: Optional[str] = Field(description="Name of the activity.")
    description: Optional[str] = Field(
        description="Very short description of the activity."
    )
    start_date: Optional[date] = Field(description="Start date of the activity.")
    end_date: Optional[date] = Field(description="End date of the activity.")


class ResumeMetadata(BaseModel):
    name: Optional[str] = Field(description="Full name.")
    email: Optional[str] = Field(description="Email address.")
    phone: Optional[str] = Field(description="Phone number.")
    summary: Optional[str] = Field(
        description="Very short summary or objective statement."
    )
    languages: Optional[List[str]] = Field(description="List of spoken languages.")
    skills: Optional[List[str]] = Field(description="List of skills.")
    education: Optional[List[_Education]] = Field(description="List of _Education")
    experience: Optional[List[_Experience]] = Field(description="List of _Experience.")
    projects: Optional[List[_Project]] = Field(description="List of _Project.")


class JobMetadata(BaseModel):
    job_title: Optional[str] = Field(description="Job title.")
    company: Optional[str] = Field(description="Company name.")
    location: Optional[str] = Field(description="Job location.")
    skills_required: Optional[List[str]] = Field(
        description="Skills required for the job."
    )
    education_required: Optional[List[str]] = Field(
        description="Education required for the job."
    )
    experience_required: Optional[List[str]] = Field(
        description="Experience required for the job."
    )
    job_description: Optional[str] = Field(description="Job responsibilities.")
    salary_range: Optional[str] = Field(description="Salary range.")
    job_type: Optional[str] = Field(
        description="Type of job (e.g., full-time, part-time)."
    )
    application_url: Optional[str] = Field(description="URL to apply for the job.")
    posted_date: Optional[date] = Field(description="Date when the job was posted.")
    deadline: Optional[date] = Field(description="Application deadline.")
    benefits: Optional[List[str]] = Field(description="List of benefits.")
    remote: Optional[bool] = Field(description="Whether the job is remote.")
