from typing import List
from .models import (
    Student, SkillTarget, SkillSummary, Engagement, LLMInput,
    PrereqEdge, SubtopicRef
)

TOPIC_NUMBER = "จำนวนนับ"
SUBS = [
    "Pre-test",
    "การอ่าน/เขียนจำนวน >100,000 แต่ไม่เกิน 10,000,000",
    "การอ่าน/เขียนจำนวน >10,000,000",
    "หลักและค่าประจำหลัก",
    "การเขียนจำนวนในรูปกระจาย"
]

def prerequisite_edges_for_number_topic() -> List[PrereqEdge]:
    # Linear chain: 1 -> 2 -> 3 -> 4 -> 5
    edges = []
    for i in range(len(SUBS) - 1):
        edges.append(
            PrereqEdge(
                prerequisite=SubtopicRef(topic=TOPIC_NUMBER, subtopic=SUBS[i]),
                dependent=SubtopicRef(topic=TOPIC_NUMBER, subtopic=SUBS[i+1]),
            )
        )
    return edges

def _targets_for_group(group_name: str) -> List[SkillTarget]:
    # Differentiated assignments: same topic, different load/difficulty
    if group_name == "Needs Practice":
        diff = "easy"
        req = [15, 20, 15, 15, 10]
    elif group_name == "On Track":
        diff = "medium"
        req = [15, 25, 20, 20, 15]
    else:  # Advanced
        diff = "hard"
        req = [10, 20, 25, 25, 20]

    return [
        SkillTarget(topic=TOPIC_NUMBER, subtopic=SUBS[i], difficulty=diff, required_questions=req[i])
        for i in range(len(SUBS))
    ]

def _eng(active_days: int, streak: int, trend: str) -> Engagement:
    return Engagement(active_days=active_days, longest_streak=streak, last_two_weeks_trend=trend)

def build_mock_llm_inputs() -> List[LLMInput]:
    edges = prerequisite_edges_for_number_topic()

    students = [
        # 1) The "subtopic 3 -> subtopic 4" root cause case (weak at subtopic 3 causes 4&5 weak)
        Student(
            student_id="S-04001",
            name_th="เด็กชาย ภูมิ",
            classroom="ป.4/1",
            term="2568-T2",
            group_name="On Track",
            group_goal_th="ทำตามแผนมาตรฐานและค่อยๆ เพิ่มความยาก"
        ),
        # 2) Needs practice but improving + extra practice helps
        Student(
            student_id="S-04002",
            name_th="เด็กหญิง มายด์",
            classroom="ป.4/1",
            term="2568-T2",
            group_name="Needs Practice",
            group_goal_th="เน้นความแม่นยำและพื้นฐานให้แน่น"
        ),
        # 3) Advanced student (high mastery, medium/hard stable)
        Student(
            student_id="S-04003",
            name_th="เด็กชาย ไท",
            classroom="ป.4/1",
            term="2568-T2",
            group_name="Advanced",
            group_goal_th="ต่อยอดโจทย์ยากและความเร็วในการคิด"
        ),
        # 4) On track but low engagement (completion issues)
        Student(
            student_id="S-04004",
            name_th="เด็กหญิง ฝน",
            classroom="ป.4/1",
            term="2568-T2",
            group_name="On Track",
            group_goal_th="ทำตามแผนมาตรฐานและค่อยๆ เพิ่มความยาก"
        ),
        # 5) Needs practice with “careless mistakes” profile (stars ok but attempts low/time ok)
        Student(
            student_id="S-04005",
            name_th="เด็กชาย นนท์",
            classroom="ป.4/1",
            term="2568-T2",
            group_name="Needs Practice",
            group_goal_th="เน้นความแม่นยำและพื้นฐานให้แน่น"
        ),
    ]

    inputs: List[LLMInput] = []

    # Helper to build summaries quickly
    def s(topic, sub, source, diff, attempted_q, stars, time_sec, attempts):
        return SkillSummary(
            topic=topic, subtopic=sub, source=source, difficulty=diff,
            attempted_questions=attempted_q, avg_stars=stars, avg_time_sec=time_sec, avg_attempts=attempts
        )

    for st in students:
        targets = _targets_for_group(st.group_name)
        diff = targets[0].difficulty

        if st.student_id == "S-04001":
            # Root cause chain: Subtopic 3 weak => Subtopic 4&5 also weak
            assigned = [
                s(TOPIC_NUMBER, SUBS[0], "assigned", diff, 15, 2.3, 38, 1.3),
                s(TOPIC_NUMBER, SUBS[1], "assigned", diff, 25, 2.1, 45, 1.4),
                s(TOPIC_NUMBER, SUBS[2], "assigned", diff, 20, 1.2, 68, 2.2),  # weak
                s(TOPIC_NUMBER, SUBS[3], "assigned", diff, 20, 1.3, 72, 2.0),  # weak dependent
                s(TOPIC_NUMBER, SUBS[4], "assigned", diff, 15, 1.1, 80, 2.3),  # weak dependent
            ]
            extra = [
                s(TOPIC_NUMBER, SUBS[2], "extra", "easy", 10, 1.6, 60, 1.8),
            ]
            eng = _eng(18, 5, "flat")

        elif st.student_id == "S-04002":
            # Improving + extra practice helps fundamentals
            assigned = [
                s(TOPIC_NUMBER, SUBS[0], "assigned", diff, 15, 1.8, 48, 1.7),
                s(TOPIC_NUMBER, SUBS[1], "assigned", diff, 20, 1.6, 55, 1.9),
                s(TOPIC_NUMBER, SUBS[2], "assigned", diff, 15, 1.5, 58, 2.0),
                s(TOPIC_NUMBER, SUBS[3], "assigned", diff, 15, 1.9, 50, 1.6),
                s(TOPIC_NUMBER, SUBS[4], "assigned", diff, 10, 1.7, 54, 1.8),
            ]
            extra = [
                s(TOPIC_NUMBER, SUBS[1], "extra", "easy", 12, 2.2, 44, 1.3),
                s(TOPIC_NUMBER, SUBS[2], "extra", "easy", 10, 2.0, 46, 1.4),
            ]
            eng = _eng(22, 6, "up")

        elif st.student_id == "S-04003":
            # Advanced: high mastery, fast, low attempts
            assigned = [
                s(TOPIC_NUMBER, SUBS[0], "assigned", diff, 10, 2.8, 28, 1.1),
                s(TOPIC_NUMBER, SUBS[1], "assigned", diff, 20, 2.7, 32, 1.1),
                s(TOPIC_NUMBER, SUBS[2], "assigned", diff, 25, 2.6, 36, 1.2),
                s(TOPIC_NUMBER, SUBS[3], "assigned", diff, 25, 2.5, 38, 1.2),
                s(TOPIC_NUMBER, SUBS[4], "assigned", diff, 20, 2.4, 40, 1.2),
            ]
            extra = [
                s(TOPIC_NUMBER, SUBS[4], "extra", "hard", 12, 2.5, 42, 1.2),
            ]
            eng = _eng(26, 9, "up")

        elif st.student_id == "S-04004":
            # On track but low completion/engagement: some subtopics under-attempted
            assigned = [
                s(TOPIC_NUMBER, SUBS[0], "assigned", diff, 10, 2.0, 44, 1.5),
                s(TOPIC_NUMBER, SUBS[1], "assigned", diff, 12, 2.1, 46, 1.4),
                s(TOPIC_NUMBER, SUBS[2], "assigned", diff, 6,  2.0, 50, 1.5),
                s(TOPIC_NUMBER, SUBS[3], "assigned", diff, 4,  2.2, 47, 1.3),
                s(TOPIC_NUMBER, SUBS[4], "assigned", diff, 3,  2.1, 49, 1.4),
            ]
            extra = []
            eng = _eng(9, 2, "down")

        else:  # S-04005
            # Careless mistakes: stars somewhat ok, attempts low, time ok; inconsistency
            assigned = [
                s(TOPIC_NUMBER, SUBS[0], "assigned", diff, 15, 2.2, 36, 1.1),
                s(TOPIC_NUMBER, SUBS[1], "assigned", diff, 18, 2.0, 40, 1.1),
                s(TOPIC_NUMBER, SUBS[2], "assigned", diff, 12, 2.1, 39, 1.1),
                s(TOPIC_NUMBER, SUBS[3], "assigned", diff, 15, 1.9, 41, 1.1),
                s(TOPIC_NUMBER, SUBS[4], "assigned", diff, 10, 2.0, 42, 1.1),
            ]
            extra = [
                s(TOPIC_NUMBER, SUBS[3], "extra", "easy", 8, 2.4, 34, 1.0),
            ]
            eng = _eng(15, 4, "flat")

        inputs.append(
            LLMInput(
                student=st,
                assigned_targets=targets,
                assigned_summary=assigned,
                extra_summary=extra,
                engagement=eng,
                prerequisite_edges=edges,
            )
        )

    return inputs
