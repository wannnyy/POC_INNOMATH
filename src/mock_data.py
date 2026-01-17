import random
from typing import List
from .models import Student, SkillTarget, SkillSummary, Engagement, LLMInput

def _pct(correct: int, attempted: int) -> float:
    return 0.0 if attempted == 0 else correct / attempted

def build_mock_llm_input() -> LLMInput:
    # Example: Grade 4 Math, one student, Needs Practice group
    student = Student(
        student_id="S-04012",
        name_th="เด็กชาย ก้อง",
        classroom="ป.4/1",
        term="2568-T2",
        group_name="Needs Practice",
        group_goal_th="เน้นความแม่นยำและพื้นฐาน"
    )

    assigned_targets = [
        SkillTarget(skill="Fractions: compare (ตัวส่วนต่างกัน)", difficulty="easy", required_questions=30),
        SkillTarget(skill="Addition/Subtraction: regrouping (ทด/ยืม)", difficulty="easy", required_questions=25),
    ]

    assigned_summary = [
        SkillSummary(skill=assigned_targets[0].skill, source="assigned", difficulty="easy",
                     attempted=28, correct=18, avg_time_sec=41, retry_rate=0.32),
        SkillSummary(skill=assigned_targets[1].skill, source="assigned", difficulty="easy",
                     attempted=25, correct=21, avg_time_sec=33, retry_rate=0.12),
    ]

    extra_summary = [
        SkillSummary(skill="Fractions: compare (ตัวส่วนต่างกัน)", source="extra", difficulty="easy",
                     attempted=20, correct=16, avg_time_sec=38),
        SkillSummary(skill="Word problems (โจทย์ปัญหา 1–2 ขั้น)", source="extra", difficulty="easy",
                     attempted=8, correct=3, avg_time_sec=70),
    ]

    engagement = Engagement(active_days=14, longest_streak=4, last_two_weeks_trend="up")

    return LLMInput(
        student=student,
        assigned_targets=assigned_targets,
        assigned_summary=assigned_summary,
        extra_summary=extra_summary,
        engagement=engagement,
    )
