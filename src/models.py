from pydantic import BaseModel, Field
from typing import List, Literal, Optional

Difficulty = Literal["easy", "medium", "hard"]
Source = Literal["assigned", "extra"]
GroupName = Literal["Needs Practice", "On Track", "Advanced"]

class Student(BaseModel):
    student_id: str
    name_th: str
    grade: int = 4
    classroom: str
    term: str
    group_name: GroupName
    group_goal_th: str

class SubtopicRef(BaseModel):
    topic: str
    subtopic: str

class PrereqEdge(BaseModel):
    prerequisite: SubtopicRef
    dependent: SubtopicRef

class SkillTarget(BaseModel):
    topic: str
    subtopic: str
    difficulty: Difficulty
    required_questions: int

class SkillSummary(BaseModel):
    topic: str
    subtopic: str
    source: Source
    difficulty: Difficulty
    attempted_questions: int
    avg_stars: float  # 0..3
    avg_time_sec: float
    avg_attempts: float  # attempts per question (>=1)
    # Optional: if you want
    last_activity: Optional[str] = None

class Engagement(BaseModel):
    active_days: int
    longest_streak: int
    last_two_weeks_trend: Literal["up", "flat", "down"]

class LLMInput(BaseModel):
    student: Student
    assigned_targets: List[SkillTarget]
    assigned_summary: List[SkillSummary]
    extra_summary: List[SkillSummary]
    engagement: Engagement
    prerequisite_edges: List[PrereqEdge] = Field(default_factory=list)

# LLM output contract
class EvidenceItem(BaseModel):
    topic: str
    subtopic: str
    assigned_completion: str
    assigned_mastery: str
    notes: str

class NextStep(BaseModel):
    action: str
    why: str
    how: str

class ParentReport(BaseModel):
    overall_summary: str
    strengths: List[str]
    focus_areas: List[str]
    evidence: List[EvidenceItem]
    learning_habits: List[str]
    next_steps_2_weeks: List[NextStep]
    encouragement: str
    flags_for_teacher_followup: List[str] = Field(default_factory=list)
