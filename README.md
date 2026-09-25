# CareerX / Maccy Hub

A native Python career acceleration workspace by **SAKET YADAV / MACCY CREATIONS**. The current implementation is an offline-first NiceGUI application with SQLite, public job-board ingestion, career/skills/roadmap/resume/tracker/AI settings screens, and a Supabase schema prepared for authenticated sync.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Open the local URL printed by NiceGUI. A `careerx.db` SQLite file is created automatically. No password or service-role credential belongs in source control.

## Supabase setup

1. Create/link the Supabase project with the Supabase CLI.
2. Run `db_schema.sql` in the Supabase SQL Editor.
3. Configure `SUPABASE_URL` and `SUPABASE_KEY` in the deployment environment. Use the publishable/anon key only in a controlled client context; never expose a service-role key.
4. Add authentication flows and a server-side sync adapter before enabling production multi-user sync. The local queue deliberately remains safe when credentials are absent.

## Integrations

Set provider credentials as environment variables: `OPENAI_API_KEY`, `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`, `XAI_API_KEY`, `CANVA_CLIENT_ID`, `CANVA_CLIENT_SECRET`, `ADOBE_CLIENT_ID`, `ADOBE_CLIENT_SECRET`, and `JOBSUITE_API_KEY`. The UI reports configuration status without displaying secret values. Provider SDKs are optional and should be added only for the provider actually used.

## Offline verification

1. Run the app without Supabase variables.
2. Add skills, a roadmap, resume, and applications; stop/restart the app.
3. Confirm they remain in `careerx.db`.
4. Configure Supabase and add the authenticated sync adapter, then use **Sync now**. Apply last-write-wins only after validating user ownership and conflict handling.

## Data and job sources

Live jobs use genuine public RemoteOK and Arbeitnow endpoints, with source links preserved. Listings should be independently verified on the employer's official career site. No fabricated employers, salary claims, or job records are seeded.
