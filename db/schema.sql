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
  status      text not null default 'graded',
  feedback    text not null default ''
);
create index if not exists submissions_email_item
  on submissions (email, topic_id, item_id, ts desc, id desc);

create table if not exists page_views (
  day     date not null,
  unit_id text not null,
  views   integer not null default 0,
  primary key (day, unit_id)
);

create table if not exists engine_sessions (
  id           text primary key,
  session_type text not null default 'adaptive',
  name         text not null default '',
  email        text not null default '',
  unit         text not null default '',
  topic_id     text not null default '',
  data         jsonb not null,
  created_at   timestamptz not null default now(),
  updated_at   timestamptz not null default now()
);

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

create table if not exists unlocks (
  id         bigserial primary key,
  email      text not null,
  via        text not null default '',
  ref        text not null default '',
  revoked    boolean not null default false,
  created_at timestamptz not null default now()
);
create index if not exists unlocks_email on unlocks (email);

create table if not exists settings (
  key   text primary key,
  value text not null
);
insert into settings (key, value) values ('free_unlock', 'on') on conflict (key) do nothing;
insert into settings (key, value) values ('min_amount', '0') on conflict (key) do nothing;

create table if not exists unlock_codes (
  code       text primary key,
  uses_left  integer not null default 1,
  note       text not null default '',
  created_at timestamptz not null default now()
);

create table if not exists payments (
  id              text primary key,
  provider        text not null default 'razorpay',
  status          text not null,
  amount          bigint not null default 0,
  amount_refunded bigint not null default 0,
  fee             bigint not null default 0,
  tax             bigint not null default 0,
  currency        text not null default 'INR',
  method          text not null default '',
  email           text not null default '',
  description     text not null default '',
  created_at      timestamptz not null,
  synced_at       timestamptz not null default now()
);
alter table payments add column if not exists notes jsonb not null default '{}'::jsonb;

create table if not exists ledger_keys (
  hash       text primary key,
  note       text not null default '',
  created_at timestamptz not null default now()
);

create extension if not exists pgcrypto;

create table if not exists accounts (
  email        text primary key,
  pass_hash    text not null,
  must_change  boolean not null default false,
  fails        integer not null default 0,
  locked_until timestamptz,
  created_at   timestamptz not null default now(),
  updated_at   timestamptz not null default now()
);

create table if not exists sessions (
  token_hash text primary key,
  email      text not null,
  created_at timestamptz not null default now()
);
create index if not exists sessions_email on sessions (email);

create table if not exists reset_codes (
  email      text primary key,
  code       text not null,
  tries      integer not null default 0,
  created_at timestamptz not null default now(),
  expires_at timestamptz not null,
  sent_at    timestamptz
);

create table if not exists teacher_keys (
  hash       text primary key,
  note       text not null default '',
  created_at timestamptz not null default now()
);

create table if not exists teacher_emails (
  email      text primary key,
  created_at timestamptz not null default now()
);

alter table accounts        enable row level security;
alter table sessions        enable row level security;
alter table reset_codes     enable row level security;
alter table teacher_keys    enable row level security;
alter table teacher_emails  enable row level security;
revoke all on accounts, sessions, reset_codes, teacher_keys, teacher_emails from public, anonymous, authenticated;

alter table submissions     enable row level security;
alter table page_views      enable row level security;
alter table engine_sessions enable row level security;
alter table activity        enable row level security;
alter table unlocks         enable row level security;
alter table unlock_codes    enable row level security;
alter table payments        enable row level security;
alter table ledger_keys     enable row level security;
alter table settings        enable row level security;

revoke all on submissions, page_views, engine_sessions, activity, unlocks, unlock_codes, payments, ledger_keys, settings
  from public, anonymous, authenticated;

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

create or replace function _sha(t text)
returns text language sql immutable as $$
  select encode(sha256(convert_to(coalesce(t, ''), 'UTF8')), 'hex')
$$;

create or replace function _header(name text)
returns text language sql stable as $$
  select coalesce(nullif(current_setting('request.headers', true), '')::json->>name, '')
$$;

create or replace function _me()
returns text language sql stable security definer set search_path = public, pg_temp as $$
  select s.email from sessions s
   where _header('x-session') <> '' and s.token_hash = _sha(_header('x-session'))
     and s.created_at > now() - interval '365 days'
$$;

create or replace function _teacher()
returns boolean language sql stable security definer set search_path = public, pg_temp as $$
  select (_header('x-teacher-key') <> ''
          and exists (select 1 from teacher_keys where hash = _sha(_header('x-teacher-key'))))
      or exists (select 1 from teacher_emails where email = _me())
$$;

create or replace function _need_me(p_email text)
returns void language plpgsql stable security definer set search_path = public, pg_temp as $$
begin
  if not _teacher() and _me() is distinct from lower(trim(coalesce(p_email, ''))) then
    raise exception 'sign in required';
  end if;
end $$;

create or replace function _need_teacher()
returns void language plpgsql stable security definer set search_path = public, pg_temp as $$
begin
  if not _teacher() then
    raise exception 'teacher key required';
  end if;
end $$;

create or replace function _email_ok(e text)
returns boolean language sql immutable as $$
  select e ~ '^[^\s@]+@[^\s@]+\.[^\s@]+$' and length(e) <= 200
$$;

create or replace function _password_problem(p text)
returns text language sql immutable as $$
  select case when length(coalesce(p, '')) < 8 then 'Use at least 8 characters.'
              when length(p) > 200 then 'That password is too long.'
              when lower(p) = 'lock&key' then 'Choose a password of your own.' end
$$;

create or replace function _new_session(e text)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  tok text := encode(gen_random_bytes(32), 'hex');
begin
  insert into sessions (token_hash, email) values (_sha(tok), e);
  return jsonb_build_object('ok', true, 'email', e, 'token', tok,
    'mustChange', coalesce((select must_change from accounts where email = e), false));
end $$;

create or replace function api_sign_in(p_email text, p_password text)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  e text := lower(trim(coalesce(p_email, '')));
  a accounts;
begin
  select * into a from accounts where email = e;
  if not found then
    return jsonb_build_object('ok', false, 'error', 'No account for that email yet. Create one below.',
                              'noAccount', true);
  end if;
  if a.locked_until > now() then
    return jsonb_build_object('ok', false, 'error',
      'Too many wrong passwords. Try again in 15 minutes, or reset your password.');
  end if;
  if crypt(coalesce(p_password, ''), a.pass_hash) <> a.pass_hash then
    update accounts set fails = case when fails + 1 >= 10 then 0 else fails + 1 end,
           locked_until = case when fails + 1 >= 10 then now() + interval '15 minutes' else locked_until end
     where email = e;
    return jsonb_build_object('ok', false, 'error', 'Wrong email or password.');
  end if;
  update accounts set fails = 0, locked_until = null where email = e;
  return _new_session(e);
end $$;

create or replace function api_sign_up(p_email text, p_password text)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  e text := lower(trim(coalesce(p_email, '')));
  bad text := _password_problem(p_password);
begin
  if not _email_ok(e) then
    return jsonb_build_object('ok', false, 'error', 'Please enter a valid email address.');
  end if;
  if bad is not null then
    return jsonb_build_object('ok', false, 'error', bad);
  end if;
  insert into accounts (email, pass_hash) values (e, crypt(p_password, gen_salt('bf', 10)))
  on conflict (email) do nothing;
  if not found then
    return jsonb_build_object('ok', false, 'error',
      'That email already has an account. Sign in, or use "Forgot password".');
  end if;
  return _new_session(e);
end $$;

create or replace function api_sign_out()
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
begin
  delete from sessions where _header('x-session') <> '' and token_hash = _sha(_header('x-session'));
  return jsonb_build_object('ok', true);
end $$;

create or replace function api_change_password(p_new text)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  e text := _me();
  bad text := _password_problem(p_new);
begin
  if e is null then
    return jsonb_build_object('ok', false, 'error', 'Please sign in again.');
  end if;
  if bad is not null then
    return jsonb_build_object('ok', false, 'error', bad);
  end if;
  update accounts set pass_hash = crypt(p_new, gen_salt('bf', 10)), must_change = false, updated_at = now()
   where email = e;
  delete from sessions where email = e and token_hash <> _sha(_header('x-session'));
  return jsonb_build_object('ok', true);
end $$;

create or replace function api_forgot_password(p_email text)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  e text := lower(trim(coalesce(p_email, '')));
begin
  if exists (select 1 from accounts where email = e)
     and not exists (select 1 from reset_codes where email = e and created_at > now() - interval '1 minute') then
    insert into reset_codes (email, code, expires_at)
    values (e, lpad(((('x' || encode(gen_random_bytes(4), 'hex'))::bit(32)::bigint) % 1000000)::text, 6, '0'),
            now() + interval '30 minutes')
    on conflict (email) do update
      set code = excluded.code, tries = 0, created_at = now(), expires_at = excluded.expires_at, sent_at = null;
  end if;
  return jsonb_build_object('ok', true);
end $$;

create or replace function api_reset_password(p_email text, p_code text, p_new text)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  e text := lower(trim(coalesce(p_email, '')));
  r reset_codes;
  bad text := _password_problem(p_new);
begin
  select * into r from reset_codes where email = e and expires_at > now();
  if not found or r.tries >= 5 then
    delete from reset_codes where email = e and (expires_at <= now() or tries >= 5);
    return jsonb_build_object('ok', false, 'error', 'That code has expired. Ask for a new one.');
  end if;
  if r.code <> trim(coalesce(p_code, '')) then
    update reset_codes set tries = tries + 1 where email = e;
    return jsonb_build_object('ok', false, 'error', 'That code isn''t right. Check the email and try again.');
  end if;
  if bad is not null then
    return jsonb_build_object('ok', false, 'error', bad);
  end if;
  update accounts set pass_hash = crypt(p_new, gen_salt('bf', 10)), must_change = false,
         fails = 0, locked_until = null, updated_at = now()
   where email = e;
  delete from sessions where email = e;
  delete from reset_codes where email = e;
  return _new_session(e);
end $$;

create or replace function api_submit(p jsonb)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  v_email text := lower(trim(_clean(p->>'email', 254)));
  v_max   numeric := least(greatest(_num(p->'maxPoints'), 0), 100);
  v_kind  text := _clean(p->>'kind', 40);
begin
  if _me() is distinct from v_email then
    return jsonb_build_object('ok', false, 'error', 'sign in required');
  end if;
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

create or replace function api_grade_submission(p jsonb)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  v_email text := lower(trim(_clean(p->>'email', 254)));
  prior   submissions;
  v_max   numeric;
  v_pts   numeric;
begin
  perform _need_teacher();
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

create or replace function api_unlock(p jsonb)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  e text := lower(trim(coalesce(p->>'email', '')));
begin
  if e !~ '^[^\s@]+@[^\s@]+\.[^\s@]+$' or length(e) > 200 then
    return jsonb_build_object('ok', false, 'error', 'bad email');
  end if;
  if exists (select 1 from unlocks where email = e and not revoked) then
    return jsonb_build_object('ok', true);
  end if;
  if coalesce((select value from settings where key = 'free_unlock'), 'on') <> 'on'
     or coalesce((select value from settings where key = 'min_amount'), '0') <> '0' then
    return jsonb_build_object('ok', false, 'error', 'The course is no longer free. Please pay to unlock it.');
  end if;
  insert into unlocks (email, via) values (e, 'free');
  return jsonb_build_object('ok', true);
end $$;

create or replace function api_redeem_code(p_email text, p_code text)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  e text := lower(trim(coalesce(p_email, '')));
  c text := upper(trim(coalesce(p_code, '')));
begin
  if e !~ '^[^\s@]+@[^\s@]+\.[^\s@]+$' or length(e) > 200 then
    return jsonb_build_object('ok', false, 'error', 'Sign in first.');
  end if;
  if exists (select 1 from unlocks where email = e and not revoked) then
    return jsonb_build_object('ok', true);
  end if;
  update unlock_codes set uses_left = uses_left - 1
   where code = left(c, 64) and uses_left > 0;
  if not found then
    return jsonb_build_object('ok', false, 'error', 'That code isn''t valid or has been used up.');
  end if;
  insert into unlocks (email, via, ref) values (e, 'code', left(c, 64));
  return jsonb_build_object('ok', true);
end $$;

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
  if lower(trim(coalesce(p->>'student_email', p->>'email', ''))) not in ('', coalesce(_me(), '')) then
    return jsonb_build_object('ok', false, 'error', 'sign in required');
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
        updated_at = now()
    where engine_sessions.email in ('', excluded.email);
  return jsonb_build_object('ok', true);
end $$;

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
  if _me() is distinct from v_email then
    return jsonb_build_object('ok', false, 'error', 'sign in required');
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

create or replace function api_student_progress(p_email text)
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select _need_me(p_email);
  select coalesce(_progress(lower(trim(coalesce(p_email, '')))) -> lower(trim(coalesce(p_email, ''))),
                  '{"work": [], "tests": {}, "hw": {}, "seen": []}'::jsonb)
         || jsonb_build_object('recent', coalesce((
              select jsonb_agg(jsonb_build_array(kind, ref, topic_id, _iso(last_ts)) order by last_ts desc)
                from (select * from activity where email = lower(trim(coalesce(p_email, '')))
                       order by last_ts desc limit 40) r), '[]'::jsonb))
$$;

create or replace function api_class_progress()
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select _need_teacher();
  select jsonb_build_object('students', _progress(null), 'generatedAt', _iso(now()))
$$;

create or replace function api_student_report(p_email text)
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select _need_me(p_email);
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
      from latest where not correct and kind <> 'exit_ticket'), '[]'::jsonb),
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

create or replace function api_class_report()
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select _need_teacher();
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

create or replace function api_unlock_status(p_email text)
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select jsonb_build_object('ok', true, 'unlocked', exists (
    select 1 from unlocks where email = lower(trim(coalesce(p_email, ''))) and not revoked
    union all
    select 1 from teacher_emails where email = lower(trim(coalesce(p_email, '')))))
$$;

create or replace function api_pay_info()
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select jsonb_build_object('ok', true,
    'minAmount', coalesce((select value::bigint from settings where key = 'min_amount' and value ~ '^[0-9]+$'), 0),
    'free', coalesce((select value from settings where key = 'free_unlock'), 'on') = 'on'
            and coalesce((select value from settings where key = 'min_amount'), '0') = '0')
$$;

create or replace function api_ledger(p_key text)
returns jsonb language plpgsql stable security definer set search_path = public, pg_temp as $$
begin
  if not exists (select 1 from ledger_keys
                  where hash = encode(sha256(convert_to(coalesce(p_key, ''), 'UTF8')), 'hex')) then
    return jsonb_build_object('ok', false);
  end if;
  return (
    with paid as (
      select *, to_char(created_at at time zone 'Asia/Kolkata', 'YYYY-MM') as month
        from payments where status in ('captured', 'refunded'))
    select jsonb_build_object(
      'ok', true,
      'totals', coalesce((select jsonb_agg(jsonb_build_object(
          'currency', currency, 'payments', n, 'gross', gross, 'refunded', refunded, 'fees', fees, 'net', net)
          order by currency <> 'INR', currency)
        from (select currency, count(*) n, sum(amount) gross, sum(amount_refunded) refunded, sum(fee) fees,
                     sum(amount - amount_refunded - fee) net
                from paid group by currency) c), '[]'::jsonb),
      'months', coalesce((select jsonb_agg(jsonb_build_object(
          'month', month, 'currency', currency, 'payments', n, 'gross', gross, 'net', net)
          order by month desc, currency <> 'INR', currency)
        from (select month, currency, count(*) n, sum(amount) gross, sum(amount - amount_refunded - fee) net
                from paid group by month, currency) m), '[]'::jsonb),
      'methods', coalesce((select jsonb_agg(jsonb_build_object(
          'method', method, 'currency', currency, 'payments', n, 'net', net) order by currency <> 'INR', net desc)
        from (select method, currency, count(*) n, sum(amount - amount_refunded - fee) net
                from paid group by method, currency) m), '[]'::jsonb),
      'recent', coalesce((select jsonb_agg(jsonb_build_object(
          'id', id, 'at', _iso(created_at), 'status', status, 'amount', amount, 'currency', currency,
          'refunded', amount_refunded, 'method', method, 'email', email,
          'message', (select value from jsonb_each_text(notes) where key ilike '%message%' limit 1))
          order by created_at desc)
        from (select * from payments where id <> '_sync' order by created_at desc limit 50) r), '[]'::jsonb),
      'unlocks', coalesce((select jsonb_object_agg(via, n)
        from (select via, count(*) n from unlocks where not revoked group by via) u), '{}'::jsonb),
      'syncedAt', (select _iso(max(synced_at)) from payments),
      'generatedAt', _iso(now())));
end $$;

create or replace function api_engine_sessions()
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select _need_teacher();
  select coalesce(jsonb_agg(data order by created_at desc), '[]'::jsonb) from engine_sessions
$$;

revoke execute on all functions in schema public from public;
grant usage on schema public to anonymous, authenticated;
grant execute on function
  api_submit(jsonb), api_grade_submission(jsonb), api_page_view(text),
  api_save_engine_session(jsonb), api_student_report(text), api_class_report(),
  api_ad_metrics(), api_engine_sessions(), api_track(jsonb),
  api_student_progress(text), api_class_progress(),
  api_unlock(jsonb), api_unlock_status(text), api_redeem_code(text, text),
  api_ledger(text), api_pay_info(),
  api_sign_in(text, text), api_sign_up(text, text), api_sign_out(), api_change_password(text),
  api_forgot_password(text), api_reset_password(text, text, text)
  to anonymous, authenticated;
