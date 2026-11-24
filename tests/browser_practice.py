import functools
import socketserver
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import browser_soc as B

check = B.check


def page_for(browser, base, query):
    page = browser.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.route("**/*", lambda route: route.continue_() if route.request.url.startswith(base) else route.abort())
    page.add_init_script("""try {
      localStorage.setItem('apcyber_session', 'test-session');
      localStorage.setItem('apcyber_student_email', 'practice-test@example.org');
      localStorage.setItem('apcyber_unlocks', JSON.stringify({ 'practice-test@example.org': { via: 'test' } }));
    } catch (e) {}""")
    page.goto(f"{base}/tests/index.html{query}")
    page.wait_for_function("() => document.querySelectorAll('#inp-topic option').length > 1 && document.querySelectorAll('#inp-unit option').length > 1")
    page.evaluate("() => { Identity.ensureEmail = cb => cb('practice-test@example.org'); }")
    return page, errors


def answer_until_report(page, limit):
    asked = 0
    for _ in range(limit + 1):
        page.wait_for_selector("#screen-quiz:not(.hidden) .choice-btn, #screen-report:not(.hidden)")
        if page.is_visible("#screen-report"):
            break
        asked += 1
        page.locator(".choice-btn").first.click()
        page.click("#btn-submit")
        page.wait_for_selector("#screen-review:not(.hidden) #btn-next-review")
        page.click("#btn-next-review")
    page.wait_for_selector("#screen-report:not(.hidden)")
    return asked


def practice(browser, base):
    page, errors = page_for(browser, base, "?topic=2.2")
    check(page.input_value("#inp-mode") == "practice" and page.input_value("#inp-topic") == "2.2", "a ?topic= link opens topic practice on that topic")
    check(page.inner_text("#app-title") == "Topic practice" and page.is_hidden("#row-unit") and page.is_visible("#row-topic"), "practice mode shows the topic list, not the unit list")
    page.fill("#inp-name", "Practice Test")
    page.click("text=Begin Assessment")
    page.wait_for_selector("#screen-quiz:not(.hidden) .choice-btn")
    check(page.inner_text("#q-max") == "10", f"a practice round is out of 10 ({page.inner_text('#q-max')})")
    badge = page.inner_text("#skill-badge")
    check("Evaluate risk impacts" in badge or "Document risks" in badge, f"the skill badge uses the topic's own skill names ({badge})")
    asked = answer_until_report(page, 10)
    check(6 <= asked <= 10, f"the round stops between 6 and 10 questions ({asked})")
    sub, body = page.inner_text("#rpt-subtitle"), page.inner_text("#report-body")
    check("Topic 2.2" in sub and "round 1" in sub, f"the report names the topic and the round ({sub})")
    check("unit gate" not in body and "doesn't count towards your grade" in body, "practice reports never mention the unit gate")
    again = page.locator("#report-body button", has_text="Practise again")
    check(again.count() == 1, "the report offers a Practise again button")
    again.click()
    page.wait_for_selector("#screen-quiz:not(.hidden) .choice-btn")
    rnd = page.evaluate("() => SESSION.attempt")
    check(rnd == 2, f"Practise again starts round 2 ({rnd})")
    stored = page.evaluate("() => Object.values(JSON.parse(localStorage.getItem('apcyber_engine_sessions_v1') || '{}')).filter(s => s.session_type === 'practice' && s.topic === '2.2').length")
    check(stored == 2, f"both rounds are saved as practice sessions ({stored})")
    check(not errors, f"no page errors in practice ({errors[:3]})")
    page.close()


def unit_test(browser, base):
    page, errors = page_for(browser, base, "?unit=U1")
    check(page.input_value("#inp-mode") == "test" and page.is_visible("#row-unit"), "a ?unit= link still opens the unit test")
    page.fill("#inp-name", "Unit Test")
    page.click("text=Begin Assessment")
    page.wait_for_selector("#screen-quiz:not(.hidden) .choice-btn")
    check(page.inner_text("#q-max") == "24", f"the unit test is still out of 24 ({page.inner_text('#q-max')})")
    answer_until_report(page, 24)
    check("unit gate" in page.inner_text("#report-body"), "the unit test report still shows the unit gate")
    check(not errors, f"no page errors in the unit test ({errors[:3]})")
    page.close()


def main():
    from playwright.sync_api import sync_playwright
    sys.stdout.reconfigure(encoding="utf-8")
    handler = functools.partial(B.Quiet, directory=str(B.SITE))
    with socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler) as server:
        base = f"http://127.0.0.1:{server.server_address[1]}"
        threading.Thread(target=server.serve_forever, daemon=True).start()
        with sync_playwright() as p:
            browser = p.chromium.launch()
            for name, fn in (("Topic practice", practice), ("Unit test", unit_test)):
                print(name)
                try:
                    fn(browser, base)
                except Exception as e:
                    check(False, f"{name} ran without an exception ({e.__class__.__name__}: {str(e)[:240]})")
            browser.close()
        server.shutdown()
    print(f"\n{len(B.FAILS)} failed" if B.FAILS else "\nall passed")
    return 1 if B.FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
