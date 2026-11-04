set check_function_bodies = off;

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

create table if not exists class_groups (
  id         bigserial primary key,
  name       text not null,
  schedule   jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists group_members (
  group_id bigint not null references class_groups (id) on delete cascade,
  email    text not null,
  primary key (group_id, email)
);
create index if not exists group_members_email on group_members (email);

create table if not exists assignments (
  id         bigserial primary key,
  group_id   bigint references class_groups (id) on delete cascade,
  kind       text not null,
  ref        text not null default '',
  title      text not null,
  href       text not null default '',
  due_at     timestamptz,
  note       text not null default '',
  created_at timestamptz not null default now()
);

create table if not exists videos (
  id             bigserial primary key,
  title          text not null,
  youtube        text not null,
  topic_id       text not null default '',
  note           text not null default '',
  free           boolean not null default false,
  group_id       bigint references class_groups (id) on delete set null,
  email_students boolean not null default false,
  emailed_at     timestamptz,
  created_at     timestamptz not null default now()
);

create table if not exists video_access (
  id         bigserial primary key,
  email      text not null,
  via        text not null default '',
  ref        text not null default '',
  revoked    boolean not null default false,
  created_at timestamptz not null default now()
);
create index if not exists video_access_email on video_access (email);

alter table videos add column if not exists atom_id text not null default '';

create table if not exists live_classes (
  id         bigserial primary key,
  title      text not null,
  topic_id   text not null default '',
  note       text not null default '',
  starts_at  timestamptz,
  minutes    integer not null default 60,
  meet_url   text not null default '',
  mode       text not null default 'open',
  price_inr  integer not null default 0,
  price_usd  integer not null default 0,
  capacity   integer not null default 0,
  recording  text not null default '',
  status     text not null default 'scheduled',
  created_at timestamptz not null default now()
);

create table if not exists class_seats (
  class_id   bigint not null references live_classes (id) on delete cascade,
  email      text not null,
  paid       boolean not null default false,
  via        text not null default '',
  ref        text not null default '',
  created_at timestamptz not null default now(),
  primary key (class_id, email)
);
create index if not exists class_seats_email on class_seats (email);

create table if not exists class_requests (
  id         bigserial primary key,
  email      text not null,
  topic_id   text not null default '',
  note       text not null default '',
  times      text not null default '',
  status     text not null default 'open',
  class_id   bigint references live_classes (id) on delete set null,
  created_at timestamptz not null default now()
);

alter table live_classes add column if not exists checkin_code text not null default '';
alter table live_classes add column if not exists checkin_until timestamptz;

create table if not exists class_attendance (
  class_id      bigint not null references live_classes (id) on delete cascade,
  email         text not null,
  joined_at     timestamptz,
  last_at       timestamptz,
  checked_in_at timestamptz,
  status        text not null default '',
  primary key (class_id, email)
);

create table if not exists breakout_teams (
  class_id bigint not null references live_classes (id) on delete cascade,
  email    text not null,
  team     integer not null,
  primary key (class_id, email)
);

alter table class_attendance enable row level security;
alter table breakout_teams   enable row level security;
revoke all on class_attendance, breakout_teams from public, anonymous, authenticated;

alter table class_groups add column if not exists kind text not null default 'class';
alter table class_groups add column if not exists open_join boolean not null default false;
alter table class_groups add column if not exists about text not null default '';
alter table class_requests add column if not exists slot_at timestamptz;

create table if not exists forum_threads (
  id         bigserial primary key,
  space      text not null,
  email      text not null,
  title      text not null,
  body       text not null default '',
  pinned     boolean not null default false,
  locked     boolean not null default false,
  deleted    boolean not null default false,
  created_at timestamptz not null default now(),
  last_at    timestamptz not null default now()
);
create index if not exists forum_threads_space on forum_threads (space, last_at desc);

create table if not exists forum_posts (
  id         bigserial primary key,
  thread_id  bigint not null references forum_threads (id) on delete cascade,
  email      text not null,
  body       text not null,
  deleted    boolean not null default false,
  created_at timestamptz not null default now()
);
create index if not exists forum_posts_thread on forum_posts (thread_id, created_at);

create table if not exists shared_notebooks (
  space      text primary key,
  data       jsonb not null default '{}'::jsonb,
  version    integer not null default 0,
  updated_by text not null default '',
  updated_at timestamptz not null default now()
);

alter table shared_notebooks add column if not exists ystate text not null default '';
alter table shared_notebooks add column if not exists ystate_upto bigint not null default 0;

create table if not exists shared_updates (
  id         bigserial primary key,
  space      text not null,
  data       text not null,
  email      text not null default '',
  created_at timestamptz not null default now()
);
create index if not exists shared_updates_space on shared_updates (space, id);

create table if not exists shared_presence (
  space   text not null,
  email   text not null,
  seen_at timestamptz not null default now(),
  primary key (space, email)
);

alter table shared_updates   enable row level security;
alter table shared_presence  enable row level security;
revoke all on shared_updates, shared_presence from public, anonymous, authenticated;

alter table forum_threads    enable row level security;
alter table forum_posts      enable row level security;
alter table shared_notebooks enable row level security;
revoke all on forum_threads, forum_posts, shared_notebooks from public, anonymous, authenticated;

create table if not exists notebooks (
  email      text not null,
  ref        text not null,
  data       jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now(),
  primary key (email, ref)
);

alter table live_classes    enable row level security;
alter table class_seats     enable row level security;
alter table class_requests  enable row level security;
alter table notebooks       enable row level security;
revoke all on live_classes, class_seats, class_requests, notebooks from public, anonymous, authenticated;

alter table class_groups    enable row level security;
alter table group_members   enable row level security;
alter table assignments     enable row level security;
alter table videos          enable row level security;
alter table video_access    enable row level security;
revoke all on class_groups, group_members, assignments, videos, video_access from public, anonymous, authenticated;

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
  r unlock_codes;
begin
  if e !~ '^[^\s@]+@[^\s@]+\.[^\s@]+$' or length(e) > 200 then
    return jsonb_build_object('ok', false, 'error', 'Sign in first.');
  end if;
  select * into r from unlock_codes where code = left(c, 64) for update;
  if not found or r.uses_left <= 0 then
    return jsonb_build_object('ok', false, 'error', 'That code isn''t valid or has been used up.');
  end if;
  if r.product = 'course' and exists (select 1 from unlocks where email = e and not revoked) then
    return jsonb_build_object('ok', true, 'product', 'course');
  end if;
  if r.product = 'labs' and _has_labs(e) then
    return jsonb_build_object('ok', true, 'product', 'labs');
  end if;
  if exists (select 1 from ticket_ledger where email = e and ref = 'code:' || r.code)
     or exists (select 1 from seminar_subs where email = e and ref = 'code:' || r.code) then
    return jsonb_build_object('ok', false, 'error', 'You have already used this code.');
  end if;
  update unlock_codes set uses_left = uses_left - 1 where code = r.code;
  if r.product = 'labs' then
    insert into labs_access (email, via, ref) values (e, 'code', r.code);
  elsif r.product = 'tickets' then
    insert into ticket_ledger (email, delta, reason, ref) values (e, greatest(r.amount, 1), 'code', 'code:' || r.code);
  elsif r.product = 'seminars' then
    insert into seminar_subs (email, via, ref, until)
    values (e, 'code', 'code:' || r.code, greatest(now(), coalesce(_sub_until(e), now())) + make_interval(days => greatest(r.amount, 1)));
  else
    insert into unlocks (email, via, ref) values (e, 'code', r.code);
  end if;
  return jsonb_build_object('ok', true, 'product', r.product, 'amount', r.amount);
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
                    'assignments', 'activities', 'unit', 'lecture', 'book', 'capstone', 'test', 'video') then
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
    select 1 from teacher_emails where email = lower(trim(coalesce(p_email, '')))),
    'labs', _has_labs(lower(trim(coalesce(p_email, '')))))
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

create or replace function api_whoami()
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select jsonb_build_object('ok', true, 'email', _me(), 'teacher', _teacher())
$$;

create or replace function api_teacher_students()
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select _need_teacher();
  with people as (
    select email from accounts union select email from unlocks union select email from labs_access
    union select email from ticket_ledger union select email from seminar_subs
  )
  select jsonb_build_object('students', coalesce(jsonb_agg(jsonb_build_object(
      'email',      p.email,
      'account',    a.email is not null,
      'starter',    coalesce(a.must_change, false),
      'locked',     coalesce(a.locked_until > now(), false),
      'teacher',    exists (select 1 from teacher_emails t where t.email = p.email),
      'joined',     _iso(coalesce(a.created_at, (select min(created_at) from unlocks u where u.email = p.email))),
      'last',       _iso((select max(last_ts) from activity x where x.email = p.email)),
      'unlocked',   exists (select 1 from unlocks u where u.email = p.email and not u.revoked)
                    or exists (select 1 from teacher_emails t where t.email = p.email),
      'via',        coalesce((select string_agg(distinct u.via, ', ') from unlocks u
                               where u.email = p.email and not u.revoked), ''),
      'paid',       exists (select 1 from unlocks u where u.email = p.email and u.via in ('razorpay', 'gumroad')),
      'videos',     _has_labs(p.email),
      'labs',       _has_labs(p.email),
      'tickets',    _tickets(p.email),
      'seminarsUntil', _iso(_sub_until(p.email)),
      'groups',     coalesce((select jsonb_agg(m.group_id order by m.group_id) from group_members m
                               where m.email = p.email), '[]'::jsonb),
      'active7',    exists (select 1 from activity x where x.email = p.email and x.day > current_date - 7),
      'held',       (select count(*) from class_seats s join live_classes c on c.id = s.class_id
                      where s.email = p.email and c.status <> 'cancelled' and c.starts_at + make_interval(mins => c.minutes) < now()),
      'attended',   (select count(*) from class_seats s join live_classes c on c.id = s.class_id
                      where s.email = p.email and c.status <> 'cancelled' and c.starts_at + make_interval(mins => c.minutes) < now()
                        and _attendance(c, s.email) in ('present', 'late', 'joined', 'excused')))
    order by p.email), '[]'::jsonb),
    'codes', coalesce((select jsonb_agg(jsonb_build_object('code', code, 'usesLeft', uses_left, 'note', note,
                                                           'product', product, 'amount', amount,
                                                           'created', _iso(created_at)) order by created_at desc)
                         from unlock_codes), '[]'::jsonb),
    'generatedAt', _iso(now()))
    from people p left join accounts a using (email)
$$;

create or replace function api_teacher_add_student(p_email text, p_unlock boolean)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  e text := lower(trim(coalesce(p_email, '')));
begin
  perform _need_teacher();
  if not _email_ok(e) then
    return jsonb_build_object('ok', false, 'error', 'Please enter a valid email address.');
  end if;
  insert into accounts (email, pass_hash, must_change) values (e, crypt('lock&key', gen_salt('bf', 10)), true)
  on conflict (email) do nothing;
  if coalesce(p_unlock, false) and not exists (select 1 from unlocks where email = e and not revoked) then
    insert into unlocks (email, via) values (e, 'teacher');
  end if;
  return jsonb_build_object('ok', true);
end $$;

create or replace function api_teacher_reset_password(p_email text)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  e text := lower(trim(coalesce(p_email, '')));
begin
  perform _need_teacher();
  if exists (select 1 from teacher_emails where email = e) then
    return jsonb_build_object('ok', false, 'error', 'Teacher accounts reset their own password with "Forgot password?".');
  end if;
  update accounts set pass_hash = crypt('lock&key', gen_salt('bf', 10)), must_change = true,
         fails = 0, locked_until = null, updated_at = now()
   where email = e;
  if not found then
    return jsonb_build_object('ok', false, 'error', 'That student has no account yet.');
  end if;
  delete from sessions where email = e;
  delete from reset_codes where email = e;
  return jsonb_build_object('ok', true);
end $$;

create or replace function api_teacher_set_unlock(p_email text, p_on boolean)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  e text := lower(trim(coalesce(p_email, '')));
begin
  perform _need_teacher();
  if not _email_ok(e) then
    return jsonb_build_object('ok', false, 'error', 'Please enter a valid email address.');
  end if;
  if coalesce(p_on, false) then
    if not exists (select 1 from unlocks where email = e and not revoked) then
      insert into unlocks (email, via) values (e, 'teacher');
    end if;
  else
    update unlocks set revoked = true where email = e and not revoked;
  end if;
  return jsonb_build_object('ok', true);
end $$;

create or replace function api_teacher_remove_student(p_email text)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  e text := lower(trim(coalesce(p_email, '')));
begin
  perform _need_teacher();
  if exists (select 1 from teacher_emails where email = e) then
    return jsonb_build_object('ok', false, 'error', 'Teacher accounts can''t be removed here.');
  end if;
  delete from activity where email = e;
  delete from engine_sessions where email = e;
  delete from submissions where email = e;
  delete from sessions where email = e;
  delete from reset_codes where email = e;
  delete from unlocks where email = e and via not in ('razorpay', 'gumroad');
  delete from accounts where email = e;
  return jsonb_build_object('ok', true);
end $$;

create or replace function api_teacher_make_code(p_note text, p_uses integer)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  abc text := 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  c text := 'CLASS-';
  i integer;
begin
  perform _need_teacher();
  for i in 1..8 loop
    if i = 5 then c := c || '-'; end if;
    c := c || substr(abc, 1 + (get_byte(gen_random_bytes(1), 0) % 32), 1);
  end loop;
  insert into unlock_codes (code, uses_left, note)
  values (c, least(greatest(coalesce(p_uses, 1), 1), 500), _clean(trim(coalesce(p_note, '')), 100));
  return jsonb_build_object('ok', true, 'code', c);
end $$;

create or replace function api_teacher_end_code(p_code text)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
begin
  perform _need_teacher();
  update unlock_codes set uses_left = 0 where code = upper(trim(coalesce(p_code, '')));
  return jsonb_build_object('ok', true);
end $$;

create or replace function api_teacher_dashboard()
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select _need_teacher();
  with days as (
    select generate_series(current_date - 29, current_date, interval '1 day')::date as day
  ), act as (
    select day, count(distinct email) as active, sum(n) as opens from activity
     where day > current_date - 30 and email not in (select email from teacher_emails) group by day
  ), sub as (
    select ts::date as day, count(*) as n,
           round(sum(points) / nullif(sum(max_points), 0) * 100) as pct
      from submissions where ts > current_date - 30 and status <> 'pending' group by 1
  ), per as (
    select email, jsonb_agg(coalesce(x.n, 0) order by d.day) as spark
      from (select distinct email from activity where email not in (select email from teacher_emails)) e
      cross join (select day from days where day > current_date - 14) d
      left join (select email, day, sum(n) as n from activity group by 1, 2) x using (email, day)
     group by email
  )
  select jsonb_build_object(
    'days', (select jsonb_agg(jsonb_build_object('day', d.day, 'active', coalesce(a.active, 0),
                                                 'opens', coalesce(a.opens, 0), 'submissions', coalesce(s.n, 0),
                                                 'pct', s.pct) order by d.day)
               from days d left join act a using (day) left join sub s using (day)),
    'sparks', coalesce((select jsonb_object_agg(email, spark) from per), '{}'::jsonb),
    'online', coalesce((select jsonb_agg(jsonb_build_object('email', email, 'kind', kind, 'ref', ref,
                                                            'topic', topic_id, 'at', _iso(last_ts)) order by last_ts desc)
                          from (select distinct on (email) * from activity
                                 where last_ts > now() - interval '15 minutes'
                                   and email not in (select email from teacher_emails)
                                 order by email, last_ts desc) o), '[]'::jsonb),
    'pendingTickets', (select count(*) from (select distinct on (email, topic_id, item_id) status from submissions
                                              order by email, topic_id, item_id, ts desc, id desc) l
                        where status = 'pending'),
    'students', (select count(*) from accounts where email not in (select email from teacher_emails)),
    'activeWeek', (select count(distinct email) from activity where day > current_date - 7
                     and email not in (select email from teacher_emails)),
    'generatedAt', _iso(now()))
$$;

create or replace function api_teacher_live(p_topic text)
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select _need_teacher();
  select jsonb_build_object(
    'online', coalesce((select jsonb_agg(jsonb_build_object('email', email, 'kind', kind, 'ref', ref,
                                                            'topic', topic_id, 'at', _iso(last_ts)) order by email)
                          from (select distinct on (email) * from activity
                                 where last_ts > now() - interval '15 minutes'
                                   and email not in (select email from teacher_emails)
                                 order by email, last_ts desc) o), '[]'::jsonb),
    'results', coalesce((select jsonb_agg(jsonb_build_object('email', email, 'points', pts, 'max', mx, 'n', n,
                                                             'last', _iso(last)) order by email)
                           from (select email, sum(points) as pts, sum(max_points) as mx, count(*) as n, max(ts) as last
                                   from (select distinct on (email, item_id) * from submissions
                                          where topic_id = coalesce(p_topic, '') and ts > now() - interval '12 hours'
                                            and status <> 'pending'
                                          order by email, item_id, ts desc, id desc) l
                                  group by email) r), '[]'::jsonb),
    'generatedAt', _iso(now()))
$$;

create or replace function api_teacher_get_schedule()
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select _need_teacher();
  select coalesce((select value::jsonb from settings where key = 'schedule'), '{}'::jsonb)
$$;

create or replace function api_teacher_set_schedule(p jsonb)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
begin
  perform _need_teacher();
  if jsonb_typeof(p) <> 'object' or length(p::text) > 20000 then
    return jsonb_build_object('ok', false, 'error', 'bad schedule');
  end if;
  insert into settings (key, value) values ('schedule', p::text)
  on conflict (key) do update set value = excluded.value;
  return jsonb_build_object('ok', true);
end $$;

create or replace function _my_groups()
returns setof bigint language sql stable security definer set search_path = public, pg_temp as $$
  select group_id from group_members where email = _me()
$$;

create or replace function _has_videos(e text)
returns boolean language sql stable security definer set search_path = public, pg_temp as $$
  select _has_labs(e)
$$;

create or replace function _assignment_json(a assignments)
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select jsonb_build_object('id', a.id, 'group', a.group_id, 'kind', a.kind, 'ref', a.ref, 'title', a.title,
                            'href', a.href, 'due', _iso(a.due_at), 'note', a.note, 'created', _iso(a.created_at))
$$;

create or replace function _done(a assignments, e text)
returns boolean language sql stable security definer set search_path = public, pg_temp as $$
  select case a.kind
    when 'adaptive' then exists (select 1 from engine_sessions s where s.email = e and s.unit = a.ref
                                    and s.updated_at >= a.created_at)
    when 'quiz' then exists (select 1 from activity x where x.email = e and x.kind = 'quiz' and x.ref = a.ref
                                and x.last_ts >= a.created_at)
                  or exists (select 1 from submissions s where s.email = e and s.topic_id = a.ref and s.ts >= a.created_at)
    when 'link' then false
    else exists (select 1 from activity x where x.email = e and x.ref = a.ref and x.last_ts >= a.created_at)
  end
$$;

create or replace function api_teacher_groups()
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select _need_teacher();
  select jsonb_build_object(
    'groups', coalesce((select jsonb_agg(jsonb_build_object('id', g.id, 'name', g.name, 'schedule', g.schedule,
               'kind', g.kind, 'open', g.open_join, 'about', g.about,
               'members', coalesce((select jsonb_agg(m.email order by m.email) from group_members m where m.group_id = g.id), '[]'::jsonb))
               order by g.name) from class_groups g), '[]'::jsonb),
    'default', coalesce((select value::jsonb from settings where key = 'schedule'), '{}'::jsonb))
$$;

create or replace function api_teacher_save_group(p jsonb)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  v_id   bigint := nullif(p->>'id', '')::bigint;
  v_name text := _clean(trim(coalesce(p->>'name', '')), 80);
  v_sch  jsonb := coalesce(p->'schedule', '{}'::jsonb);
  v_kind text := case when p->>'kind' = 'cohort' then 'cohort' else 'class' end;
begin
  perform _need_teacher();
  if jsonb_typeof(v_sch) <> 'object' or length(v_sch::text) > 20000 then
    return jsonb_build_object('ok', false, 'error', 'bad schedule');
  end if;
  if v_id is null then
    if v_name = '' then
      return jsonb_build_object('ok', false, 'error', 'Give it a name.');
    end if;
    insert into class_groups (name, schedule, kind, open_join, about)
    values (v_name, v_sch, v_kind, coalesce((p->>'open')::boolean, false), _clean(trim(coalesce(p->>'about', '')), 500))
    returning id into v_id;
  else
    update class_groups set name = coalesce(nullif(v_name, ''), name),
           schedule = case when p ? 'schedule' then v_sch else schedule end,
           kind = case when p ? 'kind' then v_kind else kind end,
           open_join = case when p ? 'open' then coalesce((p->>'open')::boolean, false) else open_join end,
           about = case when p ? 'about' then _clean(trim(coalesce(p->>'about', '')), 500) else about end
     where id = v_id;
  end if;
  return jsonb_build_object('ok', true, 'id', v_id);
end $$;

create or replace function api_teacher_delete_group(p_id bigint)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
begin
  perform _need_teacher();
  delete from class_groups where id = p_id;
  return jsonb_build_object('ok', true);
end $$;

create or replace function api_teacher_set_members(p_id bigint, p_emails text[], p_add boolean)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
begin
  perform _need_teacher();
  if not exists (select 1 from class_groups where id = p_id) then
    return jsonb_build_object('ok', false, 'error', 'That group no longer exists.');
  end if;
  if coalesce(p_add, true) then
    insert into group_members (group_id, email)
    select p_id, lower(trim(e)) from unnest(p_emails) e where _email_ok(lower(trim(e)))
    on conflict do nothing;
  else
    delete from group_members where group_id = p_id and email = any (select lower(trim(e)) from unnest(p_emails) e);
  end if;
  return jsonb_build_object('ok', true);
end $$;

create or replace function api_teacher_assignments()
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select _need_teacher();
  select coalesce(jsonb_agg(_assignment_json(a) || jsonb_build_object(
           'students', (select count(*) from (select email from group_members where group_id = a.group_id
                                              union select email from accounts where a.group_id is null
                                                and email not in (select email from teacher_emails)) w),
           'done', (select coalesce(jsonb_agg(w.email order by w.email), '[]'::jsonb)
                      from (select email from group_members where group_id = a.group_id
                            union select email from accounts where a.group_id is null
                              and email not in (select email from teacher_emails)) w
                     where _done(a, w.email)))
         order by coalesce(a.due_at, a.created_at) desc), '[]'::jsonb)
    from assignments a
$$;

create or replace function api_teacher_assign(p jsonb)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  v_id bigint;
  v_due timestamptz;
begin
  perform _need_teacher();
  if coalesce(p->>'kind', '') not in ('skill', 'topic', 'quiz', 'adaptive', 'video', 'lecture', 'link')
     or trim(coalesce(p->>'title', '')) = '' then
    return jsonb_build_object('ok', false, 'error', 'Pick what to assign.');
  end if;
  begin
    v_due := nullif(p->>'due', '')::timestamptz;
  exception when others then
    return jsonb_build_object('ok', false, 'error', 'That due date isn''t valid.');
  end;
  insert into assignments (group_id, kind, ref, title, href, due_at, note)
  values (nullif(p->>'group', '')::bigint, p->>'kind', _clean(p->>'ref', 60), _clean(trim(p->>'title'), 200),
          _clean(p->>'href', 500), v_due, _clean(trim(coalesce(p->>'note', '')), 1000))
  returning id into v_id;
  return jsonb_build_object('ok', true, 'id', v_id);
end $$;

create or replace function api_teacher_unassign(p_id bigint)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
begin
  perform _need_teacher();
  delete from assignments where id = p_id;
  return jsonb_build_object('ok', true);
end $$;

create or replace function api_teacher_videos()
returns jsonb language plpgsql stable security definer set search_path = public, pg_temp as $$
begin
  perform _need_teacher();
  return jsonb_build_object(
    'videos', coalesce((select jsonb_agg(jsonb_build_object('id', v.id, 'title', v.title, 'youtube', v.youtube,
                'topic', v.topic_id, 'atom', v.atom_id, 'note', v.note, 'free', v.free, 'group', v.group_id, 'email', v.email_students,
                'emailed', _iso(v.emailed_at), 'created', _iso(v.created_at),
                'views', (select count(distinct email) from activity x where x.kind = 'video' and x.ref = 'v' || v.id))
              order by v.created_at desc) from videos v), '[]'::jsonb),
    'buyers', (select count(distinct email) from labs_access where not revoked));
end $$;

create or replace function api_teacher_save_video(p jsonb)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  v_id bigint := nullif(p->>'id', '')::bigint;
  v_yt text := coalesce(p->>'youtube', '');
begin
  perform _need_teacher();
  v_yt := coalesce(substring(v_yt from '(?:youtu\.be/|v=|embed/|shorts/|live/)([A-Za-z0-9_-]{11})'),
                   substring(v_yt from '^([A-Za-z0-9_-]{11})$'));
  if v_yt is null then
    return jsonb_build_object('ok', false, 'error', 'Paste a YouTube link (youtube.com/watch?v=… or youtu.be/…).');
  end if;
  if trim(coalesce(p->>'title', '')) = '' then
    return jsonb_build_object('ok', false, 'error', 'Give the video a title.');
  end if;
  if v_id is null then
    insert into videos (title, youtube, topic_id, atom_id, note, free, group_id, email_students)
    values (_clean(trim(p->>'title'), 200), v_yt, _clean(p->>'topic', 20), _clean(p->>'atom', 20),
            _clean(trim(coalesce(p->>'note', '')), 2000),
            coalesce((p->>'free')::boolean, false), nullif(p->>'group', '')::bigint,
            coalesce((p->>'email')::boolean, false))
    returning id into v_id;
  else
    update videos set title = _clean(trim(p->>'title'), 200), youtube = v_yt, topic_id = _clean(p->>'topic', 20),
           atom_id = _clean(p->>'atom', 20),
           note = _clean(trim(coalesce(p->>'note', '')), 2000), free = coalesce((p->>'free')::boolean, false),
           group_id = nullif(p->>'group', '')::bigint
     where id = v_id;
  end if;
  return jsonb_build_object('ok', true, 'id', v_id);
end $$;

create or replace function api_teacher_delete_video(p_id bigint)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
begin
  perform _need_teacher();
  delete from assignments where kind = 'video' and ref = 'v' || p_id;
  delete from videos where id = p_id;
  return jsonb_build_object('ok', true);
end $$;

create or replace function api_teacher_set_video_access(p_email text, p_on boolean)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
begin
  return api_teacher_give(p_email, 'labs', case when coalesce(p_on, false) then 1 else 0 end);
end $$;

create or replace function _seat_ok(c live_classes, e text)
returns boolean language sql stable security definer set search_path = public, pg_temp as $$
  select exists (select 1 from teacher_emails where email = e)
      or exists (select 1 from class_seats s where s.class_id = c.id and s.email = e
                   and (_class_cost(c) = 0 or s.paid))
$$;

create or replace function _class_json(c live_classes, e text)
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select jsonb_build_object('id', c.id, 'code', 'C' || c.id, 'title', c.title, 'topic', c.topic_id, 'note', c.note,
    'starts', _iso(c.starts_at), 'minutes', c.minutes, 'mode', c.mode, 'tickets', _class_cost(c), 'cost', c.tickets,
    'capacity', c.capacity, 'status', c.status,
    'taken', (select count(*) from class_seats s where s.class_id = c.id),
    'seat', case when _seat_ok(c, e) then 'confirmed'
                 when exists (select 1 from class_seats s where s.class_id = c.id and s.email = e) then 'pending'
                 else 'none' end,
    'meet', case when _seat_ok(c, e) then nullif(c.meet_url, '') end,
    'team', (select b.team from breakout_teams b where b.class_id = c.id and b.email = e),
    'teamMeet', case when _seat_ok(c, e) then (select _team_url(c.meet_url, b.team) from breakout_teams b
                                                 where b.class_id = c.id and b.email = e) end,
    'checkinOpen', c.checkin_until > now(),
    'checkedIn', exists (select 1 from class_attendance a where a.class_id = c.id and a.email = e and a.checked_in_at is not null),
    'hasRecording', c.recording <> '',
    'recording', case when _seat_ok(c, e) then nullif(c.recording, '') end)
$$;

create or replace function _team_url(u text, t integer)
returns text language sql immutable as $$
  select case when u ~ '^https://meet\.jit\.si/' then regexp_replace(u, '([?#].*)?$', '') || '-team' || t
              else u end
$$;

create or replace function _attendance(c live_classes, e text)
returns text language sql stable security definer set search_path = public, pg_temp as $$
  select coalesce(nullif(a.status, ''),
                  case when a.checked_in_at is not null then 'present'
                       when a.joined_at is not null then 'joined'
                       when c.starts_at + make_interval(mins => c.minutes) < now() then 'absent'
                       else '' end)
    from (select 1) x left join class_attendance a on a.class_id = c.id and a.email = e
$$;

create or replace function api_class_join(p_id bigint, p_team boolean)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  e text := _me();
  c live_classes;
  t integer;
begin
  select * into c from live_classes where id = p_id;
  if e is null or not found or not _seat_ok(c, e) then
    return jsonb_build_object('ok', false, 'error', 'You need a seat in this class first.');
  end if;
  if c.meet_url = '' then
    return jsonb_build_object('ok', false, 'error', 'The meeting link isn''t ready yet.');
  end if;
  if c.starts_at is null or now() between c.starts_at - interval '30 minutes' and c.starts_at + make_interval(mins => c.minutes + 30) then
    insert into class_attendance (class_id, email, joined_at, last_at) values (c.id, e, now(), now())
    on conflict (class_id, email) do update set joined_at = coalesce(class_attendance.joined_at, now()), last_at = now();
  end if;
  select team into t from breakout_teams where class_id = c.id and email = e;
  return jsonb_build_object('ok', true, 'url', case when coalesce(p_team, false) and t is not null then _team_url(c.meet_url, t) else c.meet_url end);
end $$;

create or replace function api_class_checkin(p_id bigint, p_code text)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  e text := _me();
  c live_classes;
begin
  select * into c from live_classes where id = p_id;
  if e is null or not found or not _seat_ok(c, e) then
    return jsonb_build_object('ok', false, 'error', 'You need a seat in this class first.');
  end if;
  if c.checkin_until is null or c.checkin_until < now() then
    return jsonb_build_object('ok', false, 'error', 'Check-in isn''t open right now.');
  end if;
  if c.checkin_code <> trim(coalesce(p_code, '')) then
    return jsonb_build_object('ok', false, 'error', 'That code isn''t right.');
  end if;
  insert into class_attendance (class_id, email, joined_at, last_at, checked_in_at) values (c.id, e, now(), now(), now())
  on conflict (class_id, email) do update set checked_in_at = coalesce(class_attendance.checked_in_at, now()), last_at = now();
  return jsonb_build_object('ok', true);
end $$;

create or replace function api_teacher_open_checkin(p_id bigint, p_minutes integer)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  v text := lpad(((get_byte(gen_random_bytes(2), 0) * 256 + get_byte(gen_random_bytes(2), 1)) % 10000)::text, 4, '0');
begin
  perform _need_teacher();
  if coalesce(p_minutes, 0) <= 0 then
    update live_classes set checkin_until = now() where id = p_id;
    return jsonb_build_object('ok', true);
  end if;
  update live_classes set checkin_code = v, checkin_until = now() + make_interval(mins => least(p_minutes, 120)) where id = p_id;
  return jsonb_build_object('ok', true, 'code', v, 'until', _iso(now() + make_interval(mins => least(p_minutes, 120))));
end $$;

create or replace function api_teacher_set_attendance(p_id bigint, p_email text, p_status text)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
begin
  perform _need_teacher();
  if coalesce(p_status, '') not in ('', 'present', 'late', 'absent', 'excused') then
    return jsonb_build_object('ok', false, 'error', 'bad status');
  end if;
  insert into class_attendance (class_id, email, status) values (p_id, lower(trim(p_email)), p_status)
  on conflict (class_id, email) do update set status = excluded.status;
  return jsonb_build_object('ok', true);
end $$;

create or replace function api_teacher_breakouts(p_id bigint, p_teams jsonb)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
begin
  perform _need_teacher();
  if jsonb_typeof(coalesce(p_teams, '[]'::jsonb)) <> 'array' then
    return jsonb_build_object('ok', false, 'error', 'bad teams');
  end if;
  delete from breakout_teams where class_id = p_id;
  insert into breakout_teams (class_id, email, team)
  select p_id, lower(trim(m.value #>> '{}')), t.ord::int
    from jsonb_array_elements(coalesce(p_teams, '[]'::jsonb)) with ordinality t(value, ord),
         jsonb_array_elements(t.value) m(value)
  on conflict (class_id, email) do update set team = excluded.team;
  return jsonb_build_object('ok', true);
end $$;

create or replace function api_classes()
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select jsonb_build_object(
    'me', _me(),
    'tickets', coalesce(_tickets(_me()), 0),
    'classes', coalesce((select jsonb_agg(_class_json(c, _me()) order by c.starts_at nulls last)
                           from live_classes c
                          where c.status <> 'cancelled'
                            and (c.mode <> 'request' or exists (select 1 from class_seats s where s.class_id = c.id and s.email = _me()))),
                        '[]'::jsonb),
    'requests', coalesce((select jsonb_agg(jsonb_build_object('id', r.id, 'topic', r.topic_id, 'note', r.note, 'times', r.times,
                            'slot', _iso(r.slot_at), 'status', r.status, 'class', r.class_id, 'created', _iso(r.created_at)) order by r.created_at desc)
                            from class_requests r where r.email = _me()), '[]'::jsonb))
$$;

create or replace function api_join_class(p_id bigint)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  e text := _me();
  c live_classes;
  s class_seats;
  cost integer;
begin
  if e is null then
    return jsonb_build_object('ok', false, 'error', 'Sign in first.');
  end if;
  select * into c from live_classes where id = p_id and status = 'scheduled';
  if not found then
    return jsonb_build_object('ok', false, 'error', 'That class isn''t open to join.');
  end if;
  cost := _class_cost(c);
  select * into s from class_seats where class_id = c.id and email = e;
  if c.mode = 'request' and s.email is null then
    return jsonb_build_object('ok', false, 'error', 'That class isn''t open to join.');
  end if;
  if s.email is not null and (s.paid or cost = 0) then
    return jsonb_build_object('ok', true, 'class', _class_json(c, e), 'tickets', _tickets(e));
  end if;
  if s.email is null and c.capacity > 0 and (select count(*) from class_seats where class_id = c.id) >= c.capacity then
    return jsonb_build_object('ok', false, 'error', 'That class is full.');
  end if;
  if not _spend(e, cost, 'class', 'class:' || c.id) then
    return jsonb_build_object('ok', false, 'error', 'This class needs ' || cost || ' ticket' || case when cost = 1 then '' else 's' end ||
                              '. You have ' || _tickets(e) || '.', 'need', cost);
  end if;
  insert into class_seats (class_id, email, paid, via) values (c.id, e, cost > 0, case when cost > 0 then 'tickets' else 'join' end)
  on conflict (class_id, email) do update set paid = class_seats.paid or excluded.paid,
    via = case when excluded.paid then 'tickets' else class_seats.via end;
  return jsonb_build_object('ok', true, 'class', _class_json(c, e), 'tickets', _tickets(e));
end $$;

create or replace function api_leave_class(p_id bigint)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  e text := _me();
  c live_classes;
  s class_seats;
begin
  select * into c from live_classes where id = p_id;
  select * into s from class_seats where class_id = p_id and email = e;
  if c.id is null or s.email is null then
    return jsonb_build_object('ok', true);
  end if;
  if s.paid and s.via = 'tickets' then
    if c.starts_at is not null and c.starts_at <= now() + interval '2 hours' then
      return jsonb_build_object('ok', false, 'error', 'It''s too late to cancel: the class starts within 2 hours.');
    end if;
    perform _refund_class(c.id, e);
  elsif s.paid then
    return jsonb_build_object('ok', false, 'error', 'Ask your teacher to cancel a paid seat.');
  end if;
  delete from class_seats where class_id = p_id and email = e;
  return jsonb_build_object('ok', true, 'tickets', _tickets(e));
end $$;

create or replace function api_request_class(p jsonb)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  v_slot timestamptz;
begin
  if _me() is null then
    return jsonb_build_object('ok', false, 'error', 'Sign in first.');
  end if;
  if (select count(*) from class_requests where email = _me() and status = 'open') >= 5 then
    return jsonb_build_object('ok', false, 'error', 'You already have 5 open requests.');
  end if;
  begin
    v_slot := nullif(p->>'slot', '')::timestamptz;
  exception when others then
    return jsonb_build_object('ok', false, 'error', 'Pick a time from the grid.');
  end;
  if v_slot is not null and not exists (select 1 from jsonb_array_elements_text((api_availability())->'free') f where f::timestamptz = v_slot) then
    return jsonb_build_object('ok', false, 'error', 'That time was just taken. Pick another.');
  end if;
  insert into class_requests (email, topic_id, note, times, slot_at)
  values (_me(), _clean(p->>'topic', 20), _clean(trim(coalesce(p->>'note', '')), 1000), _clean(trim(coalesce(p->>'times', '')), 300), v_slot);
  return jsonb_build_object('ok', true);
end $$;

create or replace function api_availability()
returns jsonb language plpgsql stable security definer set search_path = public, pg_temp as $$
declare
  a jsonb := coalesce((select value::jsonb from settings where key = 'availability'), '{}'::jsonb);
  tz text := coalesce(nullif(a->>'tz', ''), 'Asia/Kolkata');
  mins integer := least(greatest(coalesce((a->>'minutes')::int, 60), 15), 240);
  weeks integer := least(greatest(coalesce((a->>'weeks')::int, 2), 1), 8);
  out jsonb := '[]'::jsonb;
  d date;
  h text;
  t timestamptz;
begin
  for d in select generate_series((now() at time zone tz)::date, (now() at time zone tz)::date + weeks * 7 - 1, interval '1 day')::date loop
    for h in select jsonb_array_elements_text(coalesce(a->'slots'->(extract(dow from d)::int::text), '[]'::jsonb)) loop
      t := (d::text || ' ' || h)::timestamp at time zone tz;
      if t > now() + interval '12 hours'
         and not exists (select 1 from class_requests r where r.slot_at = t and r.status in ('open', 'scheduled'))
         and not exists (select 1 from live_classes c where c.status <> 'cancelled' and c.starts_at is not null
                           and tstzrange(c.starts_at, c.starts_at + make_interval(mins => c.minutes)) && tstzrange(t, t + make_interval(mins => mins))) then
        out := out || to_jsonb(_iso(t));
      end if;
    end loop;
  end loop;
  return jsonb_build_object('tz', tz, 'minutes', mins, 'weeks', weeks, 'slots', coalesce(a->'slots', '{}'::jsonb), 'free', out);
end $$;

create or replace function api_teacher_set_availability(p jsonb)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
begin
  perform _need_teacher();
  if jsonb_typeof(p) <> 'object' or length(p::text) > 8000 then
    return jsonb_build_object('ok', false, 'error', 'bad availability');
  end if;
  insert into settings (key, value) values ('availability', p::text)
  on conflict (key) do update set value = excluded.value;
  return jsonb_build_object('ok', true);
end $$;

create or replace function _space_ok(p_space text, e text)
returns boolean language sql stable security definer set search_path = public, pg_temp as $$
  select e is not null and (
    exists (select 1 from teacher_emails where email = e)
    or (p_space = 'all' and exists (select 1 from accounts where email = e))
    or (p_space ~ '^g[0-9]+$' and exists (select 1 from group_members where group_id = substr(p_space, 2)::bigint and email = e)))
$$;

create or replace function _who(e text)
returns text language sql stable security definer set search_path = public, pg_temp as $$
  select case when _teacher() then e
              when exists (select 1 from teacher_emails where email = e) then 'Teacher'
              else split_part(e, '@', 1) end
$$;

create or replace function api_spaces()
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select jsonb_build_object('me', _me(), 'teacher', _teacher(),
    'spaces', case when _me() is null and not _teacher() then '[]'::jsonb else
      jsonb_build_array(jsonb_build_object('space', 'all', 'name', 'Everyone', 'kind', 'all', 'about', 'The whole course.',
        'threads', (select count(*) from forum_threads where space = 'all' and not deleted),
        'last', (select _iso(max(last_at)) from forum_threads where space = 'all' and not deleted)))
      || coalesce((select jsonb_agg(jsonb_build_object('space', 'g' || g.id, 'id', g.id, 'name', g.name, 'kind', g.kind, 'about', g.about,
           'open', g.open_join, 'member', exists (select 1 from group_members m where m.group_id = g.id and m.email = _me()),
           'members', (select count(*) from group_members m where m.group_id = g.id),
           'threads', (select count(*) from forum_threads t where t.space = 'g' || g.id and not t.deleted),
           'last', (select _iso(max(last_at)) from forum_threads t where t.space = 'g' || g.id and not t.deleted))
           order by g.kind, g.name)
         from class_groups g
        where _teacher() or g.open_join or exists (select 1 from group_members m where m.group_id = g.id and m.email = _me())), '[]'::jsonb) end)
$$;

create or replace function api_group_join(p_id bigint, p_join boolean)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
begin
  if _me() is null then
    return jsonb_build_object('ok', false, 'error', 'Sign in first.');
  end if;
  if not exists (select 1 from class_groups where id = p_id and open_join) then
    return jsonb_build_object('ok', false, 'error', 'Ask your teacher to add you to that one.');
  end if;
  if coalesce(p_join, true) then
    insert into group_members (group_id, email) values (p_id, _me()) on conflict do nothing;
  else
    delete from group_members where group_id = p_id and email = _me();
  end if;
  return jsonb_build_object('ok', true);
end $$;

create or replace function api_forum_threads(p_space text)
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select case when not (_teacher() or _space_ok(p_space, _me()))
    then jsonb_build_object('ok', false, 'error', 'Join this space to read it.')
    else jsonb_build_object('ok', true, 'threads', coalesce((select jsonb_agg(jsonb_build_object('id', t.id, 'title', t.title,
      'by', _who(t.email), 'mine', t.email = _me(), 'pinned', t.pinned, 'locked', t.locked, 'created', _iso(t.created_at),
      'last', _iso(t.last_at), 'replies', (select count(*) from forum_posts p where p.thread_id = t.id and not p.deleted))
      order by t.pinned desc, t.last_at desc) from forum_threads t where t.space = p_space and not t.deleted), '[]'::jsonb)) end
$$;

create or replace function api_forum_thread(p_id bigint)
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select case when t.id is null or not (_teacher() or _space_ok(t.space, _me()))
    then jsonb_build_object('ok', false, 'error', 'Not found.')
    else jsonb_build_object('ok', true, 'thread', jsonb_build_object('id', t.id, 'space', t.space, 'title', t.title, 'body', t.body,
      'by', _who(t.email), 'mine', t.email = _me(), 'pinned', t.pinned, 'locked', t.locked, 'created', _iso(t.created_at)),
      'posts', coalesce((select jsonb_agg(jsonb_build_object('id', p.id, 'body', p.body, 'by', _who(p.email), 'mine', p.email = _me(),
        'created', _iso(p.created_at)) order by p.created_at) from forum_posts p where p.thread_id = t.id and not p.deleted), '[]'::jsonb)) end
    from (select 1) x left join forum_threads t on t.id = p_id and not t.deleted
$$;

create or replace function api_forum_post(p jsonb)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  e text := coalesce(_me(), '');
  t forum_threads;
  v_body text := _clean(trim(coalesce(p->>'body', '')), 8000);
  v_id bigint;
begin
  if e = '' then
    return jsonb_build_object('ok', false, 'error', 'Sign in to post.');
  end if;
  if (select count(*) from forum_posts where email = e and created_at > now() - interval '1 minute')
     + (select count(*) from forum_threads where email = e and created_at > now() - interval '1 minute') >= 6 then
    return jsonb_build_object('ok', false, 'error', 'Slow down a little, then try again.');
  end if;
  if nullif(p->>'thread', '') is not null then
    select * into t from forum_threads where id = (p->>'thread')::bigint and not deleted;
    if not found or not _space_ok(t.space, e) then
      return jsonb_build_object('ok', false, 'error', 'Not found.');
    end if;
    if t.locked and not _teacher() then
      return jsonb_build_object('ok', false, 'error', 'This thread is closed.');
    end if;
    if v_body = '' then
      return jsonb_build_object('ok', false, 'error', 'Write something first.');
    end if;
    insert into forum_posts (thread_id, email, body) values (t.id, e, v_body) returning id into v_id;
    update forum_threads set last_at = now() where id = t.id;
    return jsonb_build_object('ok', true, 'id', v_id);
  end if;
  if not _space_ok(coalesce(p->>'space', ''), e) then
    return jsonb_build_object('ok', false, 'error', 'Join this space to post.');
  end if;
  if trim(coalesce(p->>'title', '')) = '' then
    return jsonb_build_object('ok', false, 'error', 'Give your post a title.');
  end if;
  insert into forum_threads (space, email, title, body) values (p->>'space', e, _clean(trim(p->>'title'), 200), v_body) returning id into v_id;
  return jsonb_build_object('ok', true, 'id', v_id);
end $$;

create or replace function api_forum_moderate(p_kind text, p_id bigint, p_action text)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
begin
  if p_kind = 'post' then
    update forum_posts set deleted = true where id = p_id and p_action = 'delete' and (email = _me() or _teacher());
  elsif p_action = 'delete' then
    update forum_threads set deleted = true where id = p_id and (email = _me() or _teacher());
  else
    perform _need_teacher();
    update forum_threads set pinned = case p_action when 'pin' then true when 'unpin' then false else pinned end,
           locked = case p_action when 'lock' then true when 'unlock' then false else locked end
     where id = p_id;
  end if;
  return jsonb_build_object('ok', true);
end $$;

create or replace function api_shared_get(p_space text)
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select case when not (_teacher() or _space_ok(p_space, _me())) then jsonb_build_object('ok', false, 'error', 'Join this space to open its notebook.')
    else jsonb_build_object('ok', true, 'data', coalesce(n.data, '{}'::jsonb), 'version', coalesce(n.version, 0),
      'by', case when n.updated_by <> '' then _who(n.updated_by) end, 'updated', _iso(n.updated_at),
      'ystate', coalesce(n.ystate, ''), 'upto', coalesce(n.ystate_upto, 0)) end
    from (select 1) x left join shared_notebooks n on n.space = p_space
$$;

create or replace function api_shared_push(p_space text, p_update text)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  v bigint;
  e text := coalesce(_me(), '');
begin
  if not (_teacher() or _space_ok(p_space, e)) then
    return jsonb_build_object('ok', false, 'error', 'Join this space to edit its notebook.');
  end if;
  if length(coalesce(p_update, '')) = 0 or length(p_update) > 200000 then
    return jsonb_build_object('ok', false, 'error', 'That change is too big.');
  end if;
  insert into shared_updates (space, data, email) values (p_space, p_update, e) returning id into v;
  return jsonb_build_object('ok', true, 'id', v);
end $$;

create or replace function api_shared_pull(p_space text, p_after bigint)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  e text := coalesce(_me(), '');
begin
  if not (_teacher() or _space_ok(p_space, e)) then
    return jsonb_build_object('ok', false, 'error', 'Join this space to open its notebook.');
  end if;
  if e <> '' then
    insert into shared_presence (space, email) values (p_space, e)
    on conflict (space, email) do update set seen_at = now();
  end if;
  return jsonb_build_object('ok', true,
    'updates', coalesce((select jsonb_agg(jsonb_build_array(u.id, u.data) order by u.id)
                           from (select id, data from shared_updates where space = p_space and id > coalesce(p_after, 0)
                                  order by id limit 400) u), '[]'::jsonb),
    'count', (select count(*) from shared_updates where space = p_space),
    'upto', coalesce((select ystate_upto from shared_notebooks where space = p_space), 0),
    'here', coalesce((select jsonb_agg(_who(email) order by email) from shared_presence
                       where space = p_space and seen_at > now() - interval '30 seconds'), '[]'::jsonb));
end $$;

create or replace function api_shared_compact(p_space text, p_state text, p_upto bigint, p_data jsonb)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  e text := coalesce(_me(), '');
begin
  if not (_teacher() or _space_ok(p_space, e)) then
    return jsonb_build_object('ok', false, 'error', 'Join this space to edit its notebook.');
  end if;
  if length(coalesce(p_state, '')) > 600000 or jsonb_typeof(coalesce(p_data, '{}'::jsonb)) <> 'object' then
    return jsonb_build_object('ok', false, 'error', 'That notebook is too big to save.');
  end if;
  insert into shared_notebooks (space) values (p_space) on conflict do nothing;
  update shared_notebooks set ystate = p_state, ystate_upto = p_upto, data = coalesce(p_data, data),
         version = version + 1, updated_by = e, updated_at = now()
   where space = p_space and ystate_upto <= p_upto;
  delete from shared_updates where space = p_space and id <= p_upto;
  return jsonb_build_object('ok', true);
end $$;

create or replace function api_shared_save(p_space text, p_data jsonb, p_version integer)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  v integer;
  e text := coalesce(_me(), '');
begin
  if not (_teacher() or _space_ok(p_space, e)) then
    return jsonb_build_object('ok', false, 'error', 'Join this space to edit its notebook.');
  end if;
  if jsonb_typeof(p_data) <> 'object' or length(p_data::text) > 300000 then
    return jsonb_build_object('ok', false, 'error', 'That notebook is too big to save.');
  end if;
  insert into shared_notebooks (space) values (p_space) on conflict do nothing;
  update shared_notebooks set data = p_data, version = version + 1, updated_by = e, updated_at = now()
   where space = p_space and version = coalesce(p_version, 0)
  returning version into v;
  if v is null then
    return jsonb_build_object('ok', false, 'conflict', true, 'error', 'Someone else just edited this notebook.');
  end if;
  return jsonb_build_object('ok', true, 'version', v);
end $$;

create or replace function api_lesson_video(p_atom text)
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select jsonb_build_object('pass', coalesce(_has_videos(_me()), false), 'videos',
    coalesce((select jsonb_agg(jsonb_build_object('id', v.id, 'title', v.title, 'note', v.note, 'free', v.free,
               'youtube', case when v.free or _has_videos(_me()) then v.youtube end) order by v.created_at)
               from videos v where v.atom_id = coalesce(p_atom, '') and v.group_id is null), '[]'::jsonb))
$$;

create or replace function api_notebook_get(p_ref text)
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select coalesce((select data || jsonb_build_object('updated', _iso(updated_at)) from notebooks
                    where email = _me() and ref = left(coalesce(p_ref, ''), 60)), '{}'::jsonb)
$$;

create or replace function api_notebook_save(p_ref text, p_data jsonb)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
begin
  if _me() is null then
    return jsonb_build_object('ok', false, 'error', 'Sign in to save your notebook.');
  end if;
  if jsonb_typeof(p_data) <> 'object' or length(p_data::text) > 300000 then
    return jsonb_build_object('ok', false, 'error', 'That notebook is too big to save.');
  end if;
  insert into notebooks (email, ref, data) values (_me(), left(p_ref, 60), p_data)
  on conflict (email, ref) do update set data = excluded.data, updated_at = now();
  return jsonb_build_object('ok', true);
end $$;

create or replace function api_notebook_list()
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select coalesce(jsonb_agg(jsonb_build_object('ref', ref, 'title', data->>'title', 'updated', _iso(updated_at))
                            order by updated_at desc), '[]'::jsonb)
    from notebooks where email = _me()
$$;

create or replace function api_teacher_classes()
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select _need_teacher();
  select jsonb_build_object(
    'classes', coalesce((select jsonb_agg(_class_json(c, null) || jsonb_build_object('meet', c.meet_url, 'recording', c.recording,
                 'checkinCode', case when c.checkin_until > now() then c.checkin_code end, 'checkinUntil', _iso(c.checkin_until),
                 'teams', (select count(distinct team) from breakout_teams b where b.class_id = c.id),
                 'seats', coalesce((select jsonb_agg(jsonb_build_object('email', s.email, 'paid', s.paid, 'via', s.via,
                            'ok', _seat_ok(c, s.email), 'attendance', _attendance(c, s.email),
                            'joined', _iso(a.joined_at), 'checkedIn', _iso(a.checked_in_at), 'mark', coalesce(a.status, ''),
                            'team', b.team) order by s.created_at)
                            from class_seats s
                            left join class_attendance a on a.class_id = c.id and a.email = s.email
                            left join breakout_teams b on b.class_id = c.id and b.email = s.email
                           where s.class_id = c.id), '[]'::jsonb))
                 order by c.starts_at desc nulls first) from live_classes c), '[]'::jsonb),
    'requests', coalesce((select jsonb_agg(jsonb_build_object('id', r.id, 'email', r.email, 'topic', r.topic_id, 'note', r.note,
                 'times', r.times, 'slot', _iso(r.slot_at), 'status', r.status, 'class', r.class_id, 'created', _iso(r.created_at)) order by r.created_at desc)
                 from class_requests r), '[]'::jsonb),
    'availability', coalesce((select value::jsonb from settings where key = 'availability'), '{}'::jsonb))
$$;

create or replace function api_teacher_save_class(p jsonb)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  v_id bigint := nullif(p->>'id', '')::bigint;
  v_start timestamptz;
  v_mode text := coalesce(nullif(p->>'mode', ''), 'open');
begin
  perform _need_teacher();
  if v_mode not in ('open', 'paid', 'request') or trim(coalesce(p->>'title', '')) = '' then
    return jsonb_build_object('ok', false, 'error', 'Give the class a title.');
  end if;
  begin
    v_start := nullif(p->>'starts', '')::timestamptz;
  exception when others then
    return jsonb_build_object('ok', false, 'error', 'That start time isn''t valid.');
  end;
  if v_id is null then
    insert into live_classes (title) values ('x') returning id into v_id;
  end if;
  update live_classes set title = _clean(trim(p->>'title'), 200), topic_id = _clean(p->>'topic', 20),
         note = _clean(trim(coalesce(p->>'note', '')), 2000), starts_at = v_start,
         minutes = least(greatest(coalesce(nullif(p->>'minutes', '')::int, 60), 15), 480),
         meet_url = coalesce(nullif(_clean(trim(coalesce(p->>'meet', '')), 500), ''),
                             nullif(meet_url, ''),
                             'https://meet.jit.si/AayatAPPrep-C' || v_id || '-' || encode(gen_random_bytes(5), 'hex')),
         mode = v_mode,
         price_inr = greatest(coalesce(nullif(p->>'inr', '')::int, 0), 0),
         price_usd = greatest(coalesce(nullif(p->>'usd', '')::int, 0), 0),
         tickets = least(greatest(coalesce(nullif(p->>'tickets', '')::int, tickets), 0), 50),
         capacity = greatest(coalesce(nullif(p->>'capacity', '')::int, 0), 0),
         status = coalesce(nullif(p->>'status', ''), status)
   where id = v_id;
  if p->>'status' = 'cancelled' then
    perform _refund_class(v_id, null);
  end if;
  if p ? 'recording' then
    update live_classes set recording = coalesce(substring(p->>'recording' from '(?:youtu\.be/|v=|embed/|live/)([A-Za-z0-9_-]{11})'),
                                                 substring(p->>'recording' from '^([A-Za-z0-9_-]{11})$'), '')
     where id = v_id;
  end if;
  if nullif(p->>'request', '') is not null then
    update class_requests set status = 'scheduled', class_id = v_id where id = (p->>'request')::bigint;
    insert into class_seats (class_id, email, paid, via)
    select v_id, email, false, 'request' from class_requests where id = (p->>'request')::bigint
    on conflict do nothing;
  end if;
  return jsonb_build_object('ok', true, 'id', v_id);
end $$;

create or replace function api_teacher_delete_class(p_id bigint)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
begin
  perform _need_teacher();
  perform _refund_class(p_id, null);
  update class_requests set status = 'open', class_id = null where class_id = p_id;
  delete from live_classes where id = p_id;
  return jsonb_build_object('ok', true);
end $$;

create or replace function api_teacher_set_seat(p_id bigint, p_email text, p_state text)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  e text := lower(trim(coalesce(p_email, '')));
begin
  perform _need_teacher();
  if p_state = 'remove' then
    perform _refund_class(p_id, e);
    delete from class_seats where class_id = p_id and email = e;
  elsif p_state in ('add', 'paid') then
    if not _email_ok(e) then
      return jsonb_build_object('ok', false, 'error', 'Please enter a valid email address.');
    end if;
    insert into class_seats (class_id, email, paid, via) values (p_id, e, p_state = 'paid', 'teacher')
    on conflict (class_id, email) do update set paid = class_seats.paid or excluded.paid;
  end if;
  return jsonb_build_object('ok', true);
end $$;

create or replace function api_teacher_answer_request(p_id bigint, p_status text)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
begin
  perform _need_teacher();
  update class_requests set status = case when p_status in ('declined', 'open') then p_status else status end where id = p_id;
  return jsonb_build_object('ok', true);
end $$;

create or replace function api_my_feed()
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select jsonb_build_object(
    'me', _me(),
    'groups', coalesce((select jsonb_agg(jsonb_build_object('id', g.id, 'name', g.name, 'schedule', g.schedule) order by g.name)
                          from class_groups g where g.id in (select _my_groups())), '[]'::jsonb),
    'default', coalesce((select value::jsonb from settings where key = 'schedule'), '{}'::jsonb),
    'assignments', coalesce((select jsonb_agg(_assignment_json(a) || jsonb_build_object('done',
                      _me() is not null and _done(a, _me())) order by coalesce(a.due_at, a.created_at))
                      from assignments a
                     where (a.group_id is null and _me() is not null) or a.group_id in (select _my_groups())), '[]'::jsonb),
    'classes', coalesce((select jsonb_agg(_class_json(c, _me()) order by c.starts_at)
                           from live_classes c where c.status <> 'cancelled' and c.starts_at is not null
                            and exists (select 1 from class_seats s where s.class_id = c.id and s.email = _me())), '[]'::jsonb),
    'videos', coalesce((select jsonb_agg(jsonb_build_object('id', v.id, 'title', v.title, 'topic', v.topic_id, 'atom', v.atom_id,
                      'note', v.note, 'free', v.free, 'created', _iso(v.created_at),
                      'youtube', case when v.free or _has_videos(_me()) then v.youtube end)
                      order by v.created_at desc)
                      from videos v where v.group_id is null or v.group_id in (select _my_groups())), '[]'::jsonb),
    'videoAccess', coalesce(_has_videos(_me()), false),
    'generatedAt', _iso(now()))
$$;

create table if not exists ctf_challenges (
  id         text primary key,
  unit       integer not null default 0,
  points     integer not null default 100,
  title      text not null,
  body       text not null default '',
  hint       text not null default '',
  link       text not null default '',
  flag_hash  text not null,
  flag       text not null default '',
  solve      text not null default '',
  sort       integer not null default 1000,
  builtin    boolean not null default false,
  active     boolean not null default true,
  created_at timestamptz not null default now()
);

create table if not exists ctf_solves (
  challenge_id text not null references ctf_challenges (id) on delete cascade,
  email        text not null,
  solved_at    timestamptz not null default now(),
  primary key (challenge_id, email)
);
create index if not exists ctf_solves_email on ctf_solves (email);

create table if not exists ctf_attempts (
  id           bigserial primary key,
  email        text not null,
  challenge_id text not null,
  created_at   timestamptz not null default now()
);
create index if not exists ctf_attempts_email on ctf_attempts (email, created_at);

alter table ctf_challenges enable row level security;
alter table ctf_solves     enable row level security;
alter table ctf_attempts   enable row level security;
revoke all on ctf_challenges, ctf_solves, ctf_attempts from public, anonymous, authenticated;

create or replace function _flag_hash(f text)
returns text language sql immutable as $$
  select _sha(lower(trim(coalesce(f, ''))))
$$;

create or replace function _ctf_space(p_space text)
returns text language sql stable security definer set search_path = public, pg_temp as $$
  select case when coalesce(p_space, 'all') = 'all' then 'all'
              when _teacher() or _space_ok(p_space, _me()) then p_space
              else 'all' end
$$;

create or replace function _ctf_scores(p_space text)
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select coalesce(jsonb_agg(jsonb_build_object('name', _who(x.email), 'me', x.email = _me(), 'score', x.score,
                                               'solved', x.solved, 'last', _iso(x.last)) order by x.score desc, x.last), '[]'::jsonb)
    from (select s.email, sum(c.points) as score, count(*) as solved, max(s.solved_at) as last
            from ctf_solves s join ctf_challenges c on c.id = s.challenge_id and c.active
           where p_space = 'all'
              or (p_space ~ '^g[0-9]+$' and s.email in (select email from group_members where group_id = substr(p_space, 2)::bigint))
           group by s.email
           order by score desc, last
           limit 100) x
$$;

create or replace function api_ctf_board(p_space text)
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select jsonb_build_object('ok', true, 'me', _me(), 'teacher', _teacher(), 'space', _ctf_space(p_space),
    'spaces', jsonb_build_array(jsonb_build_object('space', 'all', 'name', 'Everyone'))
      || coalesce((select jsonb_agg(jsonb_build_object('space', 'g' || g.id, 'name', g.name, 'kind', g.kind) order by g.kind, g.name)
                     from class_groups g
                    where _teacher() or exists (select 1 from group_members m where m.group_id = g.id and m.email = _me())), '[]'::jsonb),
    'challenges', coalesce((select jsonb_agg(jsonb_build_object('id', c.id, 'unit', c.unit, 'points', c.points, 'title', c.title,
                     'body', c.body, 'hint', c.hint, 'link', c.link, 'sort', c.sort,
                     'solves', (select count(*) from ctf_solves s where s.challenge_id = c.id),
                     'solved', exists (select 1 from ctf_solves s where s.challenge_id = c.id and s.email = _me()))
                     order by c.unit, c.sort, c.id)
                   from ctf_challenges c where c.active), '[]'::jsonb),
    'scores', _ctf_scores(_ctf_space(p_space)))
$$;

create or replace function api_ctf_submit(p_id text, p_flag text)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  e text := _me();
  c ctf_challenges;
begin
  if e is null then
    return jsonb_build_object('ok', false, 'error', 'Sign in to score points.');
  end if;
  select * into c from ctf_challenges where id = p_id and active;
  if not found then
    return jsonb_build_object('ok', false, 'error', 'No such challenge.');
  end if;
  if exists (select 1 from ctf_solves where challenge_id = c.id and email = e) then
    return jsonb_build_object('ok', true, 'correct', true, 'already', true, 'points', c.points);
  end if;
  if (select count(*) from ctf_attempts where email = e and created_at > now() - interval '1 minute') >= 10 then
    return jsonb_build_object('ok', false, 'error', 'Too many tries. Wait a minute.');
  end if;
  insert into ctf_attempts (email, challenge_id) values (e, c.id);
  if _flag_hash(p_flag) <> c.flag_hash then
    return jsonb_build_object('ok', true, 'correct', false);
  end if;
  insert into ctf_solves (challenge_id, email) values (c.id, e) on conflict do nothing;
  return jsonb_build_object('ok', true, 'correct', true, 'points', c.points);
end $$;

create or replace function api_teacher_ctf()
returns jsonb language plpgsql stable security definer set search_path = public, pg_temp as $$
begin
  perform _need_teacher();
  return jsonb_build_object('ok', true,
    'challenges', coalesce((select jsonb_agg(jsonb_build_object('id', c.id, 'unit', c.unit, 'points', c.points, 'title', c.title,
                     'body', c.body, 'hint', c.hint, 'link', c.link, 'flag', c.flag, 'solve', c.solve, 'sort', c.sort,
                     'builtin', c.builtin, 'active', c.active,
                     'solves', (select count(*) from ctf_solves s where s.challenge_id = c.id),
                     'tries', (select count(*) from ctf_attempts a where a.challenge_id = c.id))
                     order by c.unit, c.sort, c.id) from ctf_challenges c), '[]'::jsonb),
    'solves', coalesce((select jsonb_agg(jsonb_build_object('email', s.email, 'id', s.challenge_id, 'at', _iso(s.solved_at))
                     order by s.solved_at desc) from (select * from ctf_solves order by solved_at desc limit 300) s), '[]'::jsonb));
end $$;

create or replace function api_teacher_ctf_save(p jsonb)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  v_id text := nullif(trim(coalesce(p->>'id', '')), '');
  v_flag text := trim(coalesce(p->>'flag', ''));
begin
  perform _need_teacher();
  if trim(coalesce(p->>'title', '')) = '' then
    return jsonb_build_object('ok', false, 'error', 'Give the challenge a title.');
  end if;
  if v_id is null then
    if v_flag = '' then
      return jsonb_build_object('ok', false, 'error', 'Set the flag students must find.');
    end if;
    v_id := 't' || to_char(clock_timestamp(), 'YYMMDDHH24MISSMS');
    insert into ctf_challenges (id, title, flag_hash, flag) values (v_id, '', _flag_hash(v_flag), v_flag);
  end if;
  update ctf_challenges set
    unit = least(greatest(case when p ? 'unit' then _num(p->'unit')::integer else unit end, 0), 5),
    points = least(greatest(case when p ? 'points' then _num(p->'points')::integer else points end, 10), 1000),
    title = _clean(trim(p->>'title'), 200),
    body = _clean(coalesce(p->>'body', body), 8000),
    hint = _clean(coalesce(p->>'hint', hint), 1000),
    link = _clean(coalesce(p->>'link', link), 500),
    solve = _clean(coalesce(p->>'solve', solve), 2000),
    active = case when p ? 'active' then (p->>'active')::boolean else active end,
    flag = case when v_flag <> '' then v_flag else flag end,
    flag_hash = case when v_flag <> '' then _flag_hash(v_flag) else flag_hash end
  where id = v_id;
  if not found then
    return jsonb_build_object('ok', false, 'error', 'No such challenge.');
  end if;
  return jsonb_build_object('ok', true, 'id', v_id);
end $$;

create or replace function api_teacher_ctf_delete(p_id text)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
begin
  perform _need_teacher();
  delete from ctf_challenges where id = p_id and not builtin;
  update ctf_challenges set active = false where id = p_id and builtin;
  return jsonb_build_object('ok', true);
end $$;

create table if not exists labs_access (
  id         bigserial primary key,
  email      text not null,
  via        text not null default '',
  ref        text not null default '',
  revoked    boolean not null default false,
  created_at timestamptz not null default now()
);
create index if not exists labs_access_email on labs_access (email);

insert into labs_access (email, via, ref)
select distinct v.email, 'video-pass', '' from video_access v
 where not v.revoked and not exists (select 1 from labs_access l where l.email = v.email);

create table if not exists ticket_ledger (
  id         bigserial primary key,
  email      text not null,
  delta      integer not null,
  reason     text not null default '',
  ref        text not null default '',
  created_at timestamptz not null default now()
);
create index if not exists ticket_ledger_email on ticket_ledger (email, created_at);
create index if not exists ticket_ledger_ref on ticket_ledger (ref);

create table if not exists seminars (
  id          bigserial primary key,
  title       text not null,
  summary     text not null default '',
  description text not null default '',
  level       text not null default '',
  minutes     integer not null default 0,
  cover       text not null default '',
  youtube     text not null default '',
  topics      text not null default '',
  chapters    jsonb not null default '[]'::jsonb,
  resources   jsonb not null default '[]'::jsonb,
  tickets     integer not null default 1,
  published   boolean not null default false,
  sort        integer not null default 0,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);

create table if not exists seminar_access (
  seminar_id bigint not null references seminars (id) on delete cascade,
  email      text not null,
  via        text not null default '',
  created_at timestamptz not null default now(),
  primary key (seminar_id, email)
);

create table if not exists seminar_subs (
  id         bigserial primary key,
  email      text not null,
  via        text not null default '',
  ref        text not null default '',
  until      timestamptz not null,
  revoked    boolean not null default false,
  created_at timestamptz not null default now()
);
create index if not exists seminar_subs_email on seminar_subs (email);

create table if not exists premium_items (
  id         bigserial primary key,
  kind       text not null default 'lab',
  title      text not null,
  summary    text not null default '',
  unit       integer not null default 0,
  topic      text not null default '',
  tool       text not null default '',
  body       text not null default '',
  data       jsonb not null default '{}'::jsonb,
  published  boolean not null default false,
  sort       integer not null default 0,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

alter table unlock_codes add column if not exists product text not null default 'course';
alter table unlock_codes add column if not exists amount integer not null default 0;
alter table live_classes add column if not exists tickets integer not null default 1;

alter table labs_access    enable row level security;
alter table ticket_ledger  enable row level security;
alter table seminars       enable row level security;
alter table seminar_access enable row level security;
alter table seminar_subs   enable row level security;
alter table premium_items  enable row level security;
revoke all on labs_access, ticket_ledger, seminars, seminar_access, seminar_subs, premium_items from public, anonymous, authenticated;

insert into settings (key, value) values ('seminar_sub_days', '365') on conflict (key) do nothing;

create or replace function _has_labs(e text)
returns boolean language sql stable security definer set search_path = public, pg_temp as $$
  select e is not null and (exists (select 1 from labs_access where email = e and not revoked)
      or exists (select 1 from teacher_emails where email = e))
$$;

create or replace function _tickets(e text)
returns integer language sql stable security definer set search_path = public, pg_temp as $$
  select coalesce(sum(delta), 0)::integer from ticket_ledger where email = e
$$;

create or replace function _sub_until(e text)
returns timestamptz language sql stable security definer set search_path = public, pg_temp as $$
  select max(until) from seminar_subs where email = e and not revoked and until > now()
$$;

create or replace function _spend(e text, n integer, why text, r text)
returns boolean language plpgsql security definer set search_path = public, pg_temp as $$
begin
  if coalesce(n, 0) <= 0 then
    return true;
  end if;
  perform pg_advisory_xact_lock(hashtext('tickets:' || e));
  if _tickets(e) < n then
    return false;
  end if;
  insert into ticket_ledger (email, delta, reason, ref) values (e, -n, why, r);
  return true;
end $$;

create or replace function _refund_class(p_id bigint, p_email text)
returns void language sql security definer set search_path = public, pg_temp as $$
  insert into ticket_ledger (email, delta, reason, ref)
  select email, -sum(delta), 'refund', ref from ticket_ledger
   where ref = 'class:' || p_id and (p_email is null or email = p_email)
   group by email, ref having sum(delta) < 0
$$;

create or replace function _class_cost(c live_classes)
returns integer language sql immutable as $$
  select case when c.mode = 'open' then 0 else greatest(c.tickets, 0) end
$$;

create or replace function api_my_access()
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select jsonb_build_object('ok', true, 'me', _me(), 'teacher', _teacher(),
    'course', _teacher() or exists (select 1 from unlocks where email = _me() and not revoked),
    'labs', _teacher() or coalesce(_has_labs(_me()), false),
    'tickets', coalesce(_tickets(_me()), 0),
    'seminarsUntil', _iso(_sub_until(_me())),
    'history', coalesce((select jsonb_agg(jsonb_build_object('delta', delta, 'reason', reason, 'at', _iso(created_at)) order by created_at desc)
                 from (select * from ticket_ledger where email = _me() order by created_at desc limit 20) t), '[]'::jsonb))
$$;

create or replace function api_teacher_make_product_code(p_note text, p_uses integer, p_product text, p_amount integer)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  abc text := 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  v_product text := coalesce(nullif(p_product, ''), 'course');
  c text;
  i integer;
begin
  perform _need_teacher();
  if v_product not in ('course', 'labs', 'tickets', 'seminars') then
    return jsonb_build_object('ok', false, 'error', 'Unknown product.');
  end if;
  if v_product in ('tickets', 'seminars') and coalesce(p_amount, 0) <= 0 then
    return jsonb_build_object('ok', false, 'error', case when v_product = 'tickets' then 'How many tickets?' else 'How many days?' end);
  end if;
  c := case v_product when 'course' then 'CLASS-' when 'labs' then 'LABS-' when 'tickets' then 'TIX-' else 'SEM-' end;
  for i in 1..8 loop
    if i = 5 then c := c || '-'; end if;
    c := c || substr(abc, 1 + (get_byte(gen_random_bytes(1), 0) % 32), 1);
  end loop;
  insert into unlock_codes (code, uses_left, note, product, amount)
  values (c, least(greatest(coalesce(p_uses, 1), 1), 500), _clean(trim(coalesce(p_note, '')), 100), v_product,
          least(greatest(coalesce(p_amount, 0), 0), 3650));
  return jsonb_build_object('ok', true, 'code', c);
end $$;

create or replace function api_teacher_give(p_email text, p_what text, p_amount integer)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  e text := lower(trim(coalesce(p_email, '')));
  n integer := coalesce(p_amount, 0);
begin
  perform _need_teacher();
  if not _email_ok(e) then
    return jsonb_build_object('ok', false, 'error', 'Please enter a valid email address.');
  end if;
  if p_what = 'labs' then
    if n > 0 then
      if not exists (select 1 from labs_access where email = e and not revoked) then
        insert into labs_access (email, via) values (e, 'teacher');
      end if;
    else
      update labs_access set revoked = true where email = e and not revoked;
    end if;
  elsif p_what = 'tickets' then
    if n = 0 or n < -_tickets(e) or abs(n) > 500 then
      return jsonb_build_object('ok', false, 'error', 'Enter a number of tickets (and don''t take away more than they have).');
    end if;
    insert into ticket_ledger (email, delta, reason) values (e, n, case when n > 0 then 'gift' else 'teacher' end);
  elsif p_what = 'seminars' then
    if n > 0 then
      insert into seminar_subs (email, via, until) values (e, 'teacher', greatest(now(), coalesce(_sub_until(e), now())) + make_interval(days => least(n, 3650)));
    else
      update seminar_subs set revoked = true where email = e and not revoked;
    end if;
  else
    return jsonb_build_object('ok', false, 'error', 'Unknown product.');
  end if;
  return jsonb_build_object('ok', true, 'tickets', _tickets(e), 'labs', _has_labs(e), 'seminarsUntil', _iso(_sub_until(e)));
end $$;

create or replace function _seminar_ok(s seminars, e text)
returns boolean language sql stable security definer set search_path = public, pg_temp as $$
  select _teacher() or s.tickets = 0 or (e is not null and (
         exists (select 1 from seminar_access a where a.seminar_id = s.id and a.email = e)
      or exists (select 1 from seminar_subs u where u.email = e and not u.revoked and u.until > now())))
$$;

create or replace function _seminar_json(s seminars, e text, full_detail boolean)
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select jsonb_build_object('id', s.id, 'title', s.title, 'summary', s.summary, 'level', s.level, 'minutes', s.minutes,
    'cover', s.cover, 'topics', s.topics, 'tickets', s.tickets, 'published', s.published, 'updated', _iso(s.updated_at),
    'chapters', case when full_detail then (select coalesce(jsonb_agg(jsonb_build_object('t', c->>'t', 'title', c->>'title')), '[]'::jsonb)
                                            from jsonb_array_elements(s.chapters) c)
                     else to_jsonb(jsonb_array_length(s.chapters)) end,
    'owned', _seminar_ok(s, e),
    'description', case when full_detail then s.description end,
    'youtube', case when full_detail and _seminar_ok(s, e) then s.youtube end,
    'resources', case when full_detail and _seminar_ok(s, e) then s.resources else '[]'::jsonb end)
$$;

create or replace function api_seminars()
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select jsonb_build_object('ok', true, 'me', _me(), 'tickets', coalesce(_tickets(_me()), 0), 'until', _iso(_sub_until(_me())),
    'seminars', coalesce((select jsonb_agg(_seminar_json(s, _me(), false) order by s.sort, s.created_at desc)
                            from seminars s where s.published or _teacher()), '[]'::jsonb))
$$;

create or replace function api_seminar(p_id bigint)
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select coalesce((select jsonb_build_object('ok', true, 'me', _me(), 'tickets', coalesce(_tickets(_me()), 0),
                     'until', _iso(_sub_until(_me())), 'seminar', _seminar_json(s, _me(), true))
                     from seminars s where s.id = p_id and (s.published or _teacher())),
                  jsonb_build_object('ok', false, 'error', 'No such seminar.'))
$$;

create or replace function api_seminar_unlock(p_id bigint)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  e text := _me();
  s seminars;
begin
  if e is null then
    return jsonb_build_object('ok', false, 'error', 'Sign in first.');
  end if;
  select * into s from seminars where id = p_id and published;
  if not found then
    return jsonb_build_object('ok', false, 'error', 'No such seminar.');
  end if;
  if _seminar_ok(s, e) then
    return jsonb_build_object('ok', true, 'tickets', _tickets(e));
  end if;
  if not _spend(e, s.tickets, 'seminar', 'seminar:' || s.id) then
    return jsonb_build_object('ok', false, 'error', 'This seminar needs ' || s.tickets || ' ticket' || case when s.tickets = 1 then '' else 's' end ||
                              '. You have ' || _tickets(e) || '.', 'need', s.tickets);
  end if;
  insert into seminar_access (seminar_id, email, via) values (s.id, e, 'tickets') on conflict do nothing;
  return jsonb_build_object('ok', true, 'tickets', _tickets(e));
end $$;

create or replace function api_teacher_seminars()
returns jsonb language plpgsql stable security definer set search_path = public, pg_temp as $$
begin
  perform _need_teacher();
  return jsonb_build_object('ok', true,
    'seminars', coalesce((select jsonb_agg(jsonb_build_object('id', s.id, 'title', s.title, 'summary', s.summary, 'description', s.description,
                  'level', s.level, 'minutes', s.minutes, 'cover', s.cover, 'youtube', s.youtube, 'topics', s.topics,
                  'chapters', s.chapters, 'resources', s.resources, 'tickets', s.tickets, 'published', s.published, 'sort', s.sort,
                  'owners', (select count(*) from seminar_access a where a.seminar_id = s.id), 'updated', _iso(s.updated_at))
                  order by s.sort, s.created_at desc) from seminars s), '[]'::jsonb),
    'subscribers', (select count(distinct email) from seminar_subs where not revoked and until > now()));
end $$;

create or replace function api_teacher_save_seminar(p jsonb)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  v_id bigint := nullif(p->>'id', '')::bigint;
begin
  perform _need_teacher();
  if trim(coalesce(p->>'title', '')) = '' then
    return jsonb_build_object('ok', false, 'error', 'Give the seminar a title.');
  end if;
  if coalesce(p->>'youtube', '') !~* '^(https://(www\.|m\.)?(youtube\.com|youtu\.be)/\S+)?$' then
    return jsonb_build_object('ok', false, 'error', 'Paste a YouTube video or playlist link.');
  end if;
  if v_id is null then
    insert into seminars (title) values ('x') returning id into v_id;
  end if;
  update seminars set
    title = _clean(trim(p->>'title'), 200),
    summary = _clean(trim(coalesce(p->>'summary', '')), 500),
    description = _clean(coalesce(p->>'description', ''), 20000),
    level = _clean(trim(coalesce(p->>'level', '')), 40),
    minutes = least(greatest(coalesce(_num(p->'minutes'), 0)::integer, 0), 6000),
    cover = _clean(trim(coalesce(p->>'cover', '')), 500),
    youtube = _clean(trim(coalesce(p->>'youtube', '')), 500),
    topics = _clean(trim(coalesce(p->>'topics', '')), 300),
    chapters = case when jsonb_typeof(p->'chapters') = 'array' then p->'chapters' else '[]'::jsonb end,
    resources = case when jsonb_typeof(p->'resources') = 'array' then p->'resources' else '[]'::jsonb end,
    tickets = least(greatest(coalesce(_num(p->'tickets'), 1)::integer, 0), 100),
    published = coalesce((p->>'published')::boolean, false),
    sort = coalesce(_num(p->'sort'), 0)::integer,
    updated_at = now()
  where id = v_id;
  return jsonb_build_object('ok', true, 'id', v_id);
end $$;

create or replace function api_teacher_delete_seminar(p_id bigint)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
begin
  perform _need_teacher();
  if exists (select 1 from seminar_access where seminar_id = p_id) then
    update seminars set published = false where id = p_id;
    return jsonb_build_object('ok', true, 'hidden', true);
  end if;
  delete from seminars where id = p_id;
  return jsonb_build_object('ok', true);
end $$;

create or replace function api_premium_list()
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select jsonb_build_object('ok', true, 'me', _me(), 'labs', _teacher() or coalesce(_has_labs(_me()), false),
    'items', coalesce((select jsonb_agg(jsonb_build_object('id', i.id, 'kind', i.kind, 'title', i.title, 'summary', i.summary,
               'unit', i.unit, 'topic', i.topic, 'tool', i.tool, 'published', i.published, 'updated', _iso(i.updated_at))
               order by i.unit, i.sort, i.id) from premium_items i where i.published or _teacher()), '[]'::jsonb))
$$;

create or replace function api_premium_get(p_id bigint)
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select case
    when i.id is null then jsonb_build_object('ok', false, 'error', 'Not found.')
    when not (_teacher() or coalesce(_has_labs(_me()), false)) then
      jsonb_build_object('ok', false, 'locked', true, 'error', 'This is part of Labs.', 'title', i.title, 'summary', i.summary, 'kind', i.kind)
    else jsonb_build_object('ok', true, 'item', jsonb_build_object('id', i.id, 'kind', i.kind, 'title', i.title, 'summary', i.summary,
           'unit', i.unit, 'topic', i.topic, 'tool', i.tool, 'body', i.body, 'data', i.data, 'published', i.published,
           'updated', _iso(i.updated_at)))
  end
  from (select 1) x left join premium_items i on i.id = p_id and (i.published or _teacher())
$$;

create or replace function api_teacher_premium_save(p jsonb)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  v_id bigint := nullif(p->>'id', '')::bigint;
  v_kind text := coalesce(nullif(p->>'kind', ''), 'lab');
begin
  perform _need_teacher();
  if v_kind not in ('lab', 'notebook') or trim(coalesce(p->>'title', '')) = '' then
    return jsonb_build_object('ok', false, 'error', 'Give it a title.');
  end if;
  if length(coalesce(p->>'body', '')) > 200000 or length(coalesce((p->'data')::text, '')) > 2000000 then
    return jsonb_build_object('ok', false, 'error', 'That is too big to store (2 MB limit).');
  end if;
  if v_id is null then
    insert into premium_items (kind, title) values (v_kind, 'x') returning id into v_id;
  end if;
  update premium_items set
    kind = v_kind,
    title = _clean(trim(p->>'title'), 200),
    summary = _clean(trim(coalesce(p->>'summary', summary)), 1000),
    unit = least(greatest(case when p ? 'unit' then _num(p->'unit')::integer else unit end, 0), 5),
    topic = _clean(trim(coalesce(p->>'topic', topic)), 20),
    tool = _clean(trim(coalesce(p->>'tool', tool)), 40),
    body = case when p ? 'body' then coalesce(p->>'body', '') else body end,
    data = case when jsonb_typeof(p->'data') = 'object' then p->'data' else data end,
    published = case when p ? 'published' then (p->>'published')::boolean else published end,
    sort = case when p ? 'sort' then _num(p->'sort')::integer else sort end,
    updated_at = now()
  where id = v_id;
  return jsonb_build_object('ok', true, 'id', v_id);
end $$;

create or replace function api_teacher_premium_delete(p_id bigint)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
begin
  perform _need_teacher();
  delete from premium_items where id = p_id;
  return jsonb_build_object('ok', true);
end $$;

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
  api_forgot_password(text), api_reset_password(text, text, text),
  api_whoami(), api_teacher_students(), api_teacher_add_student(text, boolean),
  api_teacher_reset_password(text), api_teacher_set_unlock(text, boolean),
  api_teacher_remove_student(text), api_teacher_make_code(text, integer), api_teacher_end_code(text),
  api_teacher_dashboard(), api_teacher_live(text), api_teacher_get_schedule(), api_teacher_set_schedule(jsonb),
  api_teacher_groups(), api_teacher_save_group(jsonb), api_teacher_delete_group(bigint),
  api_teacher_set_members(bigint, text[], boolean), api_teacher_assignments(), api_teacher_assign(jsonb),
  api_teacher_unassign(bigint), api_teacher_videos(), api_teacher_save_video(jsonb), api_teacher_delete_video(bigint),
  api_teacher_set_video_access(text, boolean), api_my_feed(),
  api_classes(), api_join_class(bigint), api_leave_class(bigint), api_request_class(jsonb), api_lesson_video(text),
  api_notebook_get(text), api_notebook_save(text, jsonb), api_notebook_list(),
  api_teacher_classes(), api_teacher_save_class(jsonb), api_teacher_delete_class(bigint),
  api_teacher_set_seat(bigint, text, text), api_teacher_answer_request(bigint, text),
  api_class_join(bigint, boolean), api_class_checkin(bigint, text), api_teacher_open_checkin(bigint, integer),
  api_teacher_set_attendance(bigint, text, text), api_teacher_breakouts(bigint, jsonb),
  api_availability(), api_teacher_set_availability(jsonb), api_spaces(), api_group_join(bigint, boolean),
  api_forum_threads(text), api_forum_thread(bigint), api_forum_post(jsonb), api_forum_moderate(text, bigint, text),
  api_shared_get(text), api_shared_save(text, jsonb, integer),
  api_shared_push(text, text), api_shared_pull(text, bigint), api_shared_compact(text, text, bigint, jsonb),
  api_ctf_board(text), api_ctf_submit(text, text), api_teacher_ctf(), api_teacher_ctf_save(jsonb), api_teacher_ctf_delete(text),
  api_my_access(), api_teacher_make_product_code(text, integer, text, integer), api_teacher_give(text, text, integer),
  api_seminars(), api_seminar(bigint), api_seminar_unlock(bigint), api_teacher_seminars(), api_teacher_save_seminar(jsonb),
  api_teacher_delete_seminar(bigint), api_premium_list(), api_premium_get(bigint), api_teacher_premium_save(jsonb),
  api_teacher_premium_delete(bigint)
  to anonymous, authenticated;

notify pgrst, 'reload schema';
