"""CareerX / Maccy Hub README.

This repository is an offline-first Python app built with NiceGUI and SQLite. It also
includes a Supabase-ready schema and public job source metadata for later integration.
"""

# CareerX / Maccy Hub

A native Python career acceleration app by SAKET YADAV / MACCY CREATIONS.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python main.py
```

## Features included

- Dashboard, skills tracker, career path catalog, roadmap builder, resume builder,
  jobs page, applications tracker, AI hub, and settings page.
- SQLite-first local storage with seed data for skills and careers.
- Optional Supabase queue synchronization when credentials are configured.
- Public no-key job connectors for RemoteOK and Arbeitnow.
- Company directory and source metadata for major enterprise career portals.

## Environment variables

```bash
export SUPABASE_URL="https://<project>.supabase.co"
export SUPABASE_KEY="<anon-or-service-key>"
export OPENAI_API_KEY="..."
export GEMINI_API_KEY="..."
export ANTHROPIC_API_KEY="..."
export XAI_API_KEY="..."
export CANVA_CLIENT_ID="..."
export CANVA_CLIENT_SECRET="..."
export ADOBE_CLIENT_ID="..."
export ADOBE_CLIENT_SECRET="..."
export JOBSUITE_API_KEY="..."
```

## Notes

- No secrets should be committed to source control.
- The application stores local data in `careerx.db` by default.
- Real upstream job integrations and AI provider adapters should be wired in only after
  confirming provider terms and API access requirements.
