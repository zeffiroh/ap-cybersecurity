-- Aayat-AP-Prep, Neon database (the site's only backend).
--
-- Paste this whole file into the Neon SQL Editor and run it. It is safe to
-- run again: tables are created only if missing, and functions are replaced.
-- Run it AFTER enabling Neon Auth and the Data API (they create the
-- `anonymous` and `authenticated` roles this file grants to).
--
-- Security model. Visitors never sign in: the browser asks Neon Auth for a
-- short-lived anonymous token and calls the Data API with it. That token can
-- touch NO table directly. Every table has row-level security switched on
-- with no policies, and no table privileges are granted. The only things a
-- visitor can do are the api_* functions below, which run as the database
-- owner and validate everything they write. The gradebook is deliberately
-- open (anyone can read reports by email), matching the course's choice;
-- what the functions prevent is editing or deleting history, oversized
-- writes, and out-of-range grades.

-- ---------------------------------------------------------------- tables --

-- One row per graded attempt. Append-only: a retry or an instructor grade is
-- a newer row, and the latest row per (email, topic_id, item_id) counts.
create table if not exists submissions (
  id          bigint generated always as identity primary key,
  ts          timestamptz not null default now(),
  email       text not null,
  topic_id    text not null,
  atom_id     text not null default '',
  kind        text not null,
  item_id     text not null,
  correct     boolean not null default false,
  points      numeric not null default 0,
  max_points  numeric not null default 0,
  response    text not null default '',
  explanation text not null default '',
  status      text not null default 'graded',   -- 'graded' | 'pending'
  feedback    text not null default ''
);
create index if not exists submissions_email_item
  on submissions (email, topic_id, item_id, ts desc, id desc);

-- Sponsor audience counts: a date, a unit and a tally. Nothing about a person.
create table if not exists page_views (
  day     date not null,
  unit_id text not null,
  views   integer not null default 0,
  primary key (day, unit_id)
);

-- Adaptive-test and CW/HW quiz sessions for the tutor dashboard. The engine
-- runs in the browser; it saves its whole session record here as JSON.
create table if not exists engine_sessions (
  id           text primary key,
  session_type text not null default 'adaptive',  -- 'adaptive' | 'hw'
  name         text not null default '',
  email        text not null default '',
  unit         text not null default '',
  topic_id     text not null default '',
  data         jsonb not null,
  created_at   timestamptz not null default now(),
  updated_at   timestamptz not null default now()
);

-- What each student opened: one row per student, day and thing (a topic's
-- notes, a sim). Opening it again that day adds to n.
create table if not exists activity (
  email    text not null,
  day      date not null,
  kind     text not null,
  ref      text not null,
  topic_id text not null default '',
  n        integer not null default 1,
  first_ts timestamptz not null default now(),
  last_ts  timestamptz not null default now(),
  primary key (email, day, kind, ref)
);
create index if not exists activity_email_last on activity (email, last_ts desc);

alter table submissions     enable row level security;
alter table page_views      enable row level security;
alter table engine_sessions enable row level security;
alter table activity        enable row level security;

-- The Neon Console grants new public tables to `authenticated` by default;
-- take that back so a signed-in token is no stronger than an anonymous one.
revoke all on submissions, page_views, engine_sessions, activity from public, anonymous, authenticated;

-- ---------------------------------------------------------------- helpers --

create or replace function _clean(t text, max_len integer)
returns text language sql immutable as $$
  select left(coalesce(t, ''), max_len)
$$;

create or replace function _iso(t timestamptz)
returns text language sql immutable as $$
  select to_char(t at time zone 'UTC', 'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"')
$$;

create or replace function _num(v jsonb)
returns numeric language sql immutable as $$
  select case when jsonb_typeof(v) = 'number' then v::text::numeric
              when jsonb_typeof(v) = 'string' and v #>> '{}' ~ '^-?[0-9]+(\.[0-9]+)?$'
                then (v #>> '{}')::numeric
              else 0 end
$$;

-- ------------------------------------------------------------ write calls --

-- A graded (or pending) result from any page. Mirrors the old Apps Script
-- "submit" action. Points are clamped to 0..max_points, max_points to 0..100.
create or replace function api_submit(p jsonb)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  v_email text := lower(trim(_clean(p->>'email', 254)));
  v_max   numeric := least(greatest(_num(p->'maxPoints'), 0), 100);
  v_kind  text := _clean(p->>'kind', 40);
begin
  if v_email = '' or coalesce(p->>'topic_id', '') = '' or v_kind = ''
     or coalesce(p->>'item_id', '') = '' then
    return jsonb_build_object('ok', false, 'error', 'missing required field(s)');
  end if;
  insert into submissions (email, topic_id, atom_id, kind, item_id, correct,
                           points, max_points, response, explanation, status, feedback)
  values (v_email,
          _clean(p->>'topic_id', 40),
          _clean(p->>'atom_id', 60),
          v_kind,
          _clean(p->>'item_id', 120),
          coalesce((p->>'correct')::boolean, false),
          least(greatest(_num(p->'points'), 0), v_max),
          v_max,
          _clean(p->>'response', 10000),
          _clean(p->>'explanation', 4000),
          case when p->>'status' in ('graded', 'pending') then p->>'status'
               when v_kind = 'exit_ticket' then 'pending' else 'graded' end,
          '');
  return jsonb_build_object('ok', true);
end $$;

-- Instructor grade on top of a pending item (exit tickets). Appends a graded
-- row that carries the student's original response forward.
create or replace function api_grade_submission(p jsonb)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  v_email text := lower(trim(_clean(p->>'email', 254)));
  prior   submissions;
  v_max   numeric;
  v_pts   numeric;
begin
  if v_email = '' or coalesce(p->>'topic_id', '') = '' or coalesce(p->>'item_id', '') = '' then
    return jsonb_build_object('ok', false, 'error', 'missing required field(s)');
  end if;
  select * into prior from submissions
   where email = v_email and topic_id = p->>'topic_id' and item_id = p->>'item_id'
   order by ts desc, id desc limit 1;
  if not found then
    return jsonb_build_object('ok', false, 'error', 'no submission to grade');
  end if;
  v_max := least(greatest(coalesce(nullif(_num(p->'maxPoints'), 0), prior.max_points), 0), 100);
  v_pts := least(greatest(_num(p->'points'), 0), v_max);
  insert into submissions (email, topic_id, atom_id, kind, item_id, correct,
                           points, max_points, response, explanation, status, feedback)
  values (v_email, prior.topic_id, prior.atom_id, prior.kind, prior.item_id,
          v_max > 0 and v_pts >= v_max, v_pts, v_max, prior.response,
          _clean(p->>'explanation', 4000), 'graded', _clean(p->>'feedback', 4000));
  return jsonb_build_object('ok', true);
end $$;

-- One view of a unit page, tallied by day. Accepts nothing identifying.
create or replace function api_page_view(p_unit text)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
begin
  if coalesce(p_unit, '') !~ '^[a-z0-9\-]{1,40}$' then
    return jsonb_build_object('ok', false, 'error', 'bad unit_id');
  end if;
  insert into page_views (day, unit_id, views)
  values ((now() at time zone 'UTC')::date, p_unit, 1)
  on conflict (day, unit_id) do update set views = page_views.views + 1;
  return jsonb_build_object('ok', true);
end $$;

-- Create or update one engine session (adaptive test or CW/HW quiz).
create or replace function api_save_engine_session(p jsonb)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  v_id text := p->>'id';
begin
  if coalesce(v_id, '') !~ '^[A-Z0-9\-]{4,24}$' then
    return jsonb_build_object('ok', false, 'error', 'bad session id');
  end if;
  if pg_column_size(p) > 262144 then
    return jsonb_build_object('ok', false, 'error', 'session too large');
  end if;
  insert into engine_sessions (id, session_type, name, email, unit, topic_id, data)
  values (v_id,
          case when p->>'session_type' = 'hw' then 'hw' else 'adaptive' end,
          _clean(coalesce(p->>'student_name', p->>'name'), 120),
          lower(trim(_clean(coalesce(p->>'student_email', p->>'email'), 254))),
          _clean(p->>'unit', 10),
          _clean(p->>'topic_id', 20),
          p)
  on conflict (id) do update
    set data = excluded.data, name = excluded.name, email = excluded.email,
        updated_at = now();
  return jsonb_build_object('ok', true);
end $$;

-- Something a student opened. p: {email, kind, ref, topic_id, at?}. `at` lets a
-- page upload views made before the student signed in (clamped to the last 60 days).
create or replace function api_track(p jsonb)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  v_email text := lower(trim(_clean(p->>'email', 254)));
  v_kind  text := coalesce(p->>'kind', '');
  v_ref   text := coalesce(p->>'ref', '');
  v_at    timestamptz := now();
begin
  if v_email !~ '^[^\s@]+@[^\s@]+\.[^\s@]+$' then
    return jsonb_build_object('ok', false, 'error', 'bad email');
  end if;
  if v_kind not in ('topic', 'notes', 'slides', 'practice', 'simlab', 'sim', 'flashcards', 'quiz',
                    'assignments', 'activities', 'unit', 'lecture', 'book', 'capstone', 'test') then
    return jsonb_build_object('ok', false, 'error', 'bad kind');
  end if;
  if v_ref !~ '^[A-Za-z0-9._-]{1,40}$' then
    return jsonb_build_object('ok', false, 'error', 'bad ref');
  end if;
  begin
    if p ? 'at' then
      v_at := least(greatest((p->>'at')::timestamptz, now() - interval '60 days'), now());
    end if;
  exception when others then
    v_at := now();
  end;
  insert into activity (email, day, kind, ref, topic_id, n, first_ts, last_ts)
  values (v_email, (v_at at time zone 'UTC')::date, v_kind, v_ref, _clean(p->>'topic_id', 20), 1, v_at, v_at)
  on conflict (email, day, kind, ref) do update
    set n = activity.n + 1, last_ts = greatest(activity.last_ts, excluded.last_ts);
  return jsonb_build_object('ok', true);
end $$;

-- ------------------------------------------------------------- read calls --

-- Progress for one student (p_email) or everyone (null), in the compact shape
-- assets/theme/progress.js turns into mastery:
--   {email: {work: [[topic, atom, kind, points, max, n, last]],
--            tests: {U1: theta}, hw: {topic: best %}, seen: [[kind, ref, topic, n, last]], last}}
-- work uses the latest graded attempt per item, summed per topic, atom and kind.
create or replace function _progress(p_email text)
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  with latest as (
    select distinct on (email, topic_id, item_id) * from submissions
     where status <> 'pending' and (p_email is null or email = p_email)
     order by email, topic_id, item_id, ts desc, id desc
  ), work as (
    select email, jsonb_agg(jsonb_build_array(topic_id, atom_id, kind, pts, mx, n, _iso(last))) w, max(last) last
      from (select email, topic_id, atom_id, kind, sum(points) pts, sum(max_points) mx, count(*) n, max(ts) last
              from latest group by 1, 2, 3, 4) x
     group by email
  ), tests as (
    select email, jsonb_object_agg(unit, theta) t, max(updated_at) last
      from (select distinct on (email, unit) email, unit, round(_num(data->'overall'->'theta'), 3) theta, updated_at
              from engine_sessions
             where session_type = 'adaptive' and email <> '' and data->>'done' = 'true'
               and (p_email is null or email = p_email)
             order by email, unit, _num(data->'overall'->'theta') desc) x
     group by email
  ), hw as (
    select email, jsonb_object_agg(topic_id, best) h, max(last) last
      from (select email, topic_id, max(_num(data->'accuracy_pct')) best, max(created_at) last
              from engine_sessions
             where session_type = 'hw' and email <> '' and (p_email is null or email = p_email)
             group by 1, 2) x
     group by email
  ), seen as (
    select email, jsonb_agg(jsonb_build_array(kind, ref, topic_id, n, _iso(last))) s, max(last) last
      from (select email, kind, ref, topic_id, sum(n) n, max(last_ts) last
              from activity where p_email is null or email = p_email group by 1, 2, 3, 4) x
     group by email
  ), people as (
    select email from work union select email from tests union select email from hw union select email from seen
  )
  select coalesce(jsonb_object_agg(p.email, jsonb_build_object(
           'work',  coalesce(w.w, '[]'::jsonb),
           'tests', coalesce(t.t, '{}'::jsonb),
           'hw',    coalesce(h.h, '{}'::jsonb),
           'seen',  coalesce(s.s, '[]'::jsonb),
           'last',  _iso(greatest(w.last, t.last, h.last, s.last)))), '{}'::jsonb)
    from people p
    left join work w using (email) left join tests t using (email)
    left join hw h using (email) left join seen s using (email)
$$;

-- One student's progress plus their 40 most recent things opened.
create or replace function api_student_progress(p_email text)
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select coalesce(_progress(lower(trim(coalesce(p_email, '')))) -> lower(trim(coalesce(p_email, ''))),
                  '{"work": [], "tests": {}, "hw": {}, "seen": []}'::jsonb)
         || jsonb_build_object('recent', coalesce((
              select jsonb_agg(jsonb_build_array(kind, ref, topic_id, _iso(last_ts)) order by last_ts desc)
                from (select * from activity where email = lower(trim(coalesce(p_email, '')))
                       order by last_ts desc limit 40) r), '[]'::jsonb))
$$;

-- Every student's progress, for the tutor's class grid.
create or replace function api_class_progress()
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select jsonb_build_object('students', _progress(null), 'generatedAt', _iso(now()))
$$;


-- Report card for one student (same JSON shape the Apps Script returned).
create or replace function api_student_report(p_email text)
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  with mine as (
    select * from submissions where email = lower(trim(coalesce(p_email, '')))
  ), latest as (
    select distinct on (topic_id, item_id) * from mine
     order by topic_id, item_id, ts desc, id desc
  ), scored as (
    select * from latest where status <> 'pending'
  )
  select jsonb_build_object(
    'email', lower(trim(coalesce(p_email, ''))),
    'overall', jsonb_build_object(
      'points',          coalesce((select sum(points) from scored), 0),
      'maxPoints',       coalesce((select sum(max_points) from scored), 0),
      'percent',         coalesce((select round(sum(points) / nullif(sum(max_points), 0) * 100, 1) from scored), 0),
      'submissionCount', (select count(*) from mine)),
    'byTopic', coalesce((
      select jsonb_object_agg(topic_id, t) from (
        select topic_id, jsonb_build_object(
          'points', sum(points), 'maxPoints', sum(max_points),
          'items', jsonb_object_agg(item_id, jsonb_build_object(
            'correct', correct, 'points', points, 'maxPoints', max_points, 'kind', kind))) t
        from scored group by topic_id) x), '{}'::jsonb),
    'wrongAnswers', coalesce((
      select jsonb_agg(jsonb_build_object(
        'topic_id', topic_id, 'atom_id', atom_id, 'item_id', item_id, 'kind', kind,
        'response', response, 'explanation', explanation, 'timestamp', _iso(ts)) order by ts, id)
      from latest where not correct and kind <> 'exit_ticket'), '[]'::jsonb),  -- tickets have their own list
    'history', coalesce((
      select jsonb_agg(jsonb_build_object(
        'timestamp', _iso(ts), 'topic_id', topic_id, 'atom_id', atom_id, 'kind', kind,
        'item_id', item_id, 'correct', correct, 'points', points, 'maxPoints', max_points) order by ts, id)
      from mine), '[]'::jsonb),
    'exitTickets', coalesce((
      select jsonb_agg(jsonb_build_object(
        'topic_id', topic_id, 'atom_id', atom_id, 'item_id', item_id, 'status', status,
        'points', points, 'maxPoints', max_points, 'response', response,
        'feedback', feedback, 'timestamp', _iso(ts)) order by ts, id)
      from latest where kind = 'exit_ticket'), '[]'::jsonb))
$$;

-- Whole-class roster plus every exit ticket still waiting for a grade.
-- Scores use the latest attempt per item, like the report card.
create or replace function api_class_report()
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  with latest as (
    select distinct on (email, topic_id, item_id) * from submissions
     order by email, topic_id, item_id, ts desc, id desc
  ), counts as (
    select email, count(*) n from submissions group by email
  )
  select jsonb_build_object(
    'roster', coalesce((
      select jsonb_agg(r order by r->>'email') from (
        select jsonb_build_object(
          'email', l.email,
          'submissionCount', c.n,
          'points', coalesce(sum(l.points) filter (where l.status <> 'pending'), 0),
          'maxPoints', coalesce(sum(l.max_points) filter (where l.status <> 'pending'), 0),
          'percent', coalesce(round(sum(l.points) filter (where l.status <> 'pending')
                     / nullif(sum(l.max_points) filter (where l.status <> 'pending'), 0) * 100, 1), 0),
          'topicsTouched', count(distinct l.topic_id)) r
        from latest l join counts c using (email)
        group by l.email, c.n) x), '[]'::jsonb),
    'pendingExitTickets', coalesce((
      select jsonb_agg(jsonb_build_object(
        'email', email, 'topic_id', topic_id, 'atom_id', atom_id, 'item_id', item_id,
        'response', response, 'timestamp', _iso(ts)) order by ts, id)
      from latest where kind = 'exit_ticket' and status = 'pending'), '[]'::jsonb),
    'generatedAt', _iso(now()))
$$;

-- Sponsor numbers: views per unit, all time and trailing 30 days.
create or replace function api_ad_metrics()
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  with cutoff as (select (now() at time zone 'UTC')::date - 30 as d)
  select jsonb_build_object(
    'ok', true,
    'units', coalesce((
      select jsonb_object_agg(unit_id, jsonb_build_object('total', total, 'last30', last30)) from (
        select unit_id, sum(views) total,
               sum(views) filter (where day >= (select d from cutoff)) last30
        from page_views group by unit_id) u), '{}'::jsonb),
    'total',   coalesce((select sum(views) from page_views), 0),
    'total30', coalesce((select sum(views) from page_views where day >= (select d from cutoff)), 0),
    'since',   (select to_char(min(day), 'YYYY-MM-DD') from page_views),
    'days',    (select count(distinct day) from page_views),
    'generatedAt', _iso(now()))
$$;

-- Every engine session, newest first, for the tutor dashboard.
create or replace function api_engine_sessions()
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select coalesce(jsonb_agg(data order by created_at desc), '[]'::jsonb) from engine_sessions
$$;

-- ---------------------------------------------------------------- access --

revoke execute on all functions in schema public from public;
grant usage on schema public to anonymous, authenticated;
grant execute on function
  api_submit(jsonb), api_grade_submission(jsonb), api_page_view(text),
  api_save_engine_session(jsonb), api_student_report(text), api_class_report(),
  api_ad_metrics(), api_engine_sessions(), api_track(jsonb),
  api_student_progress(text), api_class_progress()
  to anonymous, authenticated;
