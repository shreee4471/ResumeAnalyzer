from pydantic import BaseModel


class ResumeJobRequest(BaseModel):
    resume_text: str
    job_text: str


class ResumeJobResponse(BaseModel):
    score: float

