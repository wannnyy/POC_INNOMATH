# POC_INNOMATH

# Innomath LLM Parent Report PoC (Grade 4 Math)

## What this PoC does

- Generates an end-of-term parent report in Thai
- Performance is based on assigned homework only
- Extra practice is used only as positive behavioral signals
- Supports differentiated groups (Needs Practice / On Track / Advanced)

## Setup

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Edit .env and set OPENAI_API_KEY
```
