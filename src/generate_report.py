import json
from pathlib import Path
from rich import print
from .mock_data import build_mock_llm_input
from .llm_client import generate_parent_report_json
from .models import ParentReport

def main():
    llm_input = build_mock_llm_input()
    payload = llm_input.model_dump()

    report_dict = generate_parent_report_json(payload)

    # validate output matches contract
    report = ParentReport(**report_dict)

    out_dir = Path("out/reports")
    out_dir.mkdir(parents=True, exist_ok=True)

    base = f"{llm_input.student.student_id}_{llm_input.student.term}"
    json_path = out_dir / f"{base}.json"
    json_path.write_text(report.model_dump_json(ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[green]Saved[/green] {json_path}")

if __name__ == "__main__":
    main()
