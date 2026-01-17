from pathlib import Path
from rich import print
from .mock_data import build_mock_llm_inputs
from .llm_client import generate_parent_report_json
from .models import ParentReport

def main():
    inputs = build_mock_llm_inputs()

    out_dir = Path("out/reports")
    out_dir.mkdir(parents=True, exist_ok=True)

    for llm_input in inputs:
        payload = llm_input.model_dump()

        report_dict = generate_parent_report_json(payload)
        report = ParentReport(**report_dict)  # validate schema

        base = f"{llm_input.student.student_id}_{llm_input.student.term}"
        json_path = out_dir / f"{base}.json"
        json_path.write_text(report.model_dump_json(ensure_ascii=False, indent=2), encoding="utf-8")

        print(f"[green]Saved[/green] {json_path}")

if __name__ == "__main__":
    main()
