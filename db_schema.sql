-- CareerX / Maccy Hub Supabase schema. Apply in Supabase SQL Editor.
create extension if not exists pgcrypto;
create table if not exists public.profiles (id uuid primary key references auth.users(id) on delete cascade, display_name text default '', avatar_url text, created_at timestamptz default now());
create table if not exists public.skills (id uuid primary key default gen_random_uuid(), user_id uuid not null references auth.users(id) on delete cascade, name text not null, category text not null, proficiency int default 0 check (proficiency between 0 and 100), certificate_url text, updated_at timestamptz default now());
create table if not exists public.careers (id uuid primary key default gen_random_uuid(), title text not null, level text not null, skills text default '', salary_range text default '', demand text default 'Growing');
create table if not exists public.roadmaps (id uuid primary key default gen_random_uuid(), user_id uuid not null references auth.users(id) on delete cascade, goal text not null, steps jsonb not null default '[]', status text default 'active', updated_at timestamptz default now());
create table if not exists public.resumes (id uuid primary key default gen_random_uuid(), user_id uuid not null references auth.users(id) on delete cascade, name text not null, template text not null, content text default '', ats_score int default 0, updated_at timestamptz default now());
create table if not exists public.jobs (id uuid primary key default gen_random_uuid(), external_id text unique not null, title text not null, company text not null, location text default '', url text not null, source text default '', remote boolean default false, salary text default '', posted_at timestamptz);
create table if not exists public.applications (id uuid primary key default gen_random_uuid(), user_id uuid not null references auth.users(id) on delete cascade, job_id uuid references public.jobs(id), company text not null, title text not null, stage text default 'Saved', applied_on date, salary text default '', notes text default '', follow_up date, updated_at timestamptz default now());
create table if not exists public.ai_keys (id uuid primary key default gen_random_uuid(), user_id uuid not null references auth.users(id) on delete cascade, provider text not null, encrypted_key text not null, unique(user_id, provider));
create table if not exists public.api_integrations (id uuid primary key default gen_random_uuid(), user_id uuid not null references auth.users(id) on delete cascade, provider text not null, enabled boolean default false, config jsonb default '{}', unique(user_id, provider));
create table if not exists public.pending_sync (id uuid primary key default gen_random_uuid(), user_id uuid not null references auth.users(id) on delete cascade, table_name text not null, record_id text not null, operation text not null, payload jsonb not null, created_at timestamptz default now());

alter table public.profiles enable row level security;
create policy profiles_owner on public.profiles for all using (id = auth.uid()) with check (id = auth.uid());

-- All user-owned tables use the same explicit ownership rule.
do $$ declare t text; begin foreach t in array array['skills','roadmaps','resumes','applications','ai_keys','api_integrations','pending_sync'] loop execute format('alter table public.%I enable row level security',t); execute format('create policy %I_owner on public.%I for all using (user_id = auth.uid()) with check (user_id = auth.uid())',t,t); end loop; end $$;
-- careers and jobs are public read-only catalogs.
alter table public.careers enable row level security; create policy careers_read on public.careers for select using (true);
alter table public.jobs enable row level security; create policy jobs_read on public.jobs for select using (true);
