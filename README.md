# CareerX / Maccy Hub

The Skills tab now seeds a curated taxonomy covering communication, business, software, data, cloud, DevOps, cybersecurity, and **Identity and Access Management (IAM)**. The Career tab includes aligned paths such as IAM Engineer, Cloud Security Engineer, Cybersecurity Analyst, Full-Stack Engineer, Data Analyst, ML Engineer, DevOps Engineer, ITSM Specialist, Technical Project Manager, Business Analyst, Technical Writer, and Solutions Architect.

## Job data and source integrity

The job directory includes the requested boards (Naukri, Indeed, LinkedIn, Shine, Internshala, Foundit, FlexJobs, US.jobs, We Work Remotely, Remotive, Glassdoor, Himalayas, Apna, and Job Hai) plus an MNC/company career-site directory. **Only RemoteOK and Arbeitnow are active no-key API imports in this build.** Other sites commonly restrict automated collection or require an approved partner API, so they are presented as links rather than pretending that scraped data is available. Company names are directory metadata; the app does not fabricate vacancies.

To add a compliant connector, implement an approved API/feed in `services/jobs.py`, preserve the source URL, and import only fields allowed by that provider's terms. Verify every listing on the employer's official site before applying.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python main.py
```

The first run adds the complete skill and career catalogs to `careerx.db` idempotently; existing user-created records are retained. Set `DATABASE_URL` to use another SQLModel-supported database.
