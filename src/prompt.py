import json

PARENT_REPORT_SCHEMA = {
  "type": "object",
  "additionalProperties": False,
  "properties": {
    "overall_summary": {"type": "string"},
    "strengths": {"type": "array", "items": {"type": "string"}},
    "focus_areas": {"type": "array", "items": {"type": "string"}},
    "evidence": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
          "topic": {"type": "string"},
          "subtopic": {"type": "string"},
          "assigned_completion": {"type": "string"},
          "assigned_mastery": {"type": "string"},
          "notes": {"type": "string"}
        },
        "required": ["topic","subtopic","assigned_completion","assigned_mastery","notes"]
      }
    },
    "learning_habits": {"type": "array", "items": {"type": "string"}},
    "next_steps_2_weeks": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
          "action": {"type": "string"},
          "why": {"type": "string"},
          "how": {"type": "string"}
        },
        "required": ["action","why","how"]
      }
    },
    "encouragement": {"type": "string"},
    "flags_for_teacher_followup": {"type": "array", "items": {"type": "string"}}
  },
  "required": [
    "overall_summary","strengths","focus_areas","evidence",
    "learning_habits","next_steps_2_weeks","encouragement","flags_for_teacher_followup"
  ]
}

SYSTEM_INSTRUCTIONS_TH = """คุณเป็นนักวิเคราะห์การเรียนรู้สำหรับนักเรียนประถมศึกษาปีที่ 4 วิชาคณิตศาสตร์

หลักการสำคัญ:
- ประเมิน “ผลการเรียน” โดยอ้างอิงเฉพาะงานที่ครูมอบหมาย (assigned homework) เท่านั้น
- ใช้ “การฝึกเพิ่มเติมนอกงานที่มอบหมาย” เป็นสัญญาณด้านพฤติกรรมเชิงบวกเท่านั้น (ห้ามใช้ลงโทษ/ทำให้ดูแย่)
- นักเรียนอาจอยู่คนละกลุ่ม (Needs Practice / On Track / Advanced) ทำให้งานที่ได้รับต่างกัน: สรุปผลโดยเทียบกับ “เป้าหมายงานที่ได้รับ”
- ข้อมูลต่อข้อมี: ดาว (0–3), เวลา, จำนวนครั้งที่ลองทำ (attempts)
- หากมี prerequisite_edges ให้ช่วยอธิบาย “สาเหตุราก”:
  ถ้านักเรียนอ่อนในบทย่อย A และบทย่อย B ที่ขึ้นกับ A อ่อนตาม ให้ชี้ว่า B อ่อนเพราะ A ยังไม่แน่น และแนะนำให้แก้ A ก่อน
- เขียนภาษาไทย สุภาพ อ่านง่าย ไม่ตำหนิ พร้อมแผน 2 สัปดาห์ที่ทำได้จริง 3 ข้อ
- ห้ามใส่ข้อความนอก JSON"""

def build_user_prompt(input_payload: dict) -> str:
    return (
        "สร้างรายงานสรุปปลายภาคสำหรับผู้ปกครอง ตาม JSON schema ที่กำหนดเท่านั้น\n"
        "ห้ามใส่ข้อความนอก JSON\n\n"
        "JSON schema:\n"
        f"{json.dumps(PARENT_REPORT_SCHEMA, ensure_ascii=False)}\n\n"
        "ข้อมูลนักเรียน:\n"
        f"{json.dumps(input_payload, ensure_ascii=False)}"
    )
