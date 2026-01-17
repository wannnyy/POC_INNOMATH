import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from .mock_data import build_mock_llm_input
from .llm_client import generate_parent_report_json
from .models import ParentReport

def main():
    llm_input = build_mock_llm_input()
    payload = llm_input.model_dump()

    report_dict = generate_parent_report_json(payload)
    report = ParentReport(**report_dict)

    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape(["html", "xml"])
    )
    tmpl = env.get_template("parent_report.html.j2")
    html = tmpl.render(student=llm_input.student.model_dump(), report=report.model_dump())

    out_dir = Path("out/reports")
    out_dir.mkdir(parents=True, exist_ok=True)

    base = f"{llm_input.student.student_id}_{llm_input.student.term}"
    html_path = out_dir / f"{base}.html"
    html_path.write_text(html, encoding="utf-8")

    json_path = out_dir / f"{base}.json"
    json_path.write_text(report.model_dump_json(ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Saved:\n- {json_path}\n- {html_path}")

if __name__ == "__main__":
    main()
