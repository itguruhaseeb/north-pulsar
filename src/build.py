#!/usr/bin/env python3
"""Builds site/ from the sources beside this file.

Inlines the shared stylesheet and the mark into each page.

Every page ships self contained: one file, no external CSS, no fonts, no
scripts. That way it renders identically on any static host and can be
previewed straight from disk.
"""
import base64
from pathlib import Path

here = Path(__file__).parent
root = here.parent / "site"
root.mkdir(parents=True, exist_ok=True)
css = (here / "_shared.css").read_text()
mark_tpl = (here / "_mark.svg").read_text().strip()

# The mark ships in two keyings from one source: true brand blue on light
# surfaces, and a reversed light version for the dark hero band.
BRAND = mark_tpl.format(A="#3E88D1", B="#4E95D6")
mark = mark_tpl.format(A="#FFFFFF", B="#BDD9F2")

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="color-scheme" content="light dark">
<link rel="canonical" href="https://northpulsar.com{canon}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://northpulsar.com{canon}">
<meta property="og:type" content="website">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<style>
{css}</style>
</head>
<body>
"""

FOOT = """<footer>
<div class="wrap">
<nav>
<a href="/">NorthPulsar</a>
<a href="/app">App support</a>
<a href="/app/privacy">Privacy policy</a>
<a href="mailto:info@northpulsar.com">info@northpulsar.com</a>
</nav>
<p>NorthPulsar is an independent iPhone app. Everything goes through
<a href="mailto:info@northpulsar.com">info@northpulsar.com</a>.<br>
Copyright 2026 NorthPulsar. All rights reserved.</p>
</div>
</footer>
</body>
</html>
"""

def page(path, title, desc, canon, body):
    out = root / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(HEAD.format(title=title, desc=desc, canon=canon, css=css) + body + FOOT)
    print(f"{path}  {len(out.read_text()):>6} bytes")

MARK = mark

# Screenshots live in src/shots as base64 so they can be committed as text,
# and are written out as real files at build time. They are simulator grabs
# from the UI tests, so they show the shipping build rather than a mockup.
shots = here / "shots"
images = root / "images"
have = set()
if shots.is_dir():
    images.mkdir(parents=True, exist_ok=True)
    for source in sorted(shots.glob("*.b64")):
        (images / f"{source.stem}.webp").write_bytes(
            base64.b64decode(source.read_text())
        )
        have.add(source.stem)
print(f"images/  {len(have)} screenshots" + ("" if have else ", the pages fall back to text"))


def shot(name, alt):
    """One screenshot in a phone bezel, or nothing if that shot is missing.

    Missing rather than broken on purpose. A screenshot arrives only after a
    build run has produced one, and a page with an empty image frame on it
    looks worse than a page that never promised a picture. Every layout that
    uses this reads fine with the frame absent.
    """
    if name not in have:
        return ""
    return (f'<div class="shot"><img src="/images/{name}.webp" alt="{alt}"'
            f' width="440" height="956" loading="lazy" decoding="async"></div>')


# The hero only splits into two columns when there is something to put in the
# second one.
HERO = "hero split" if "home" in have else "hero"


def step(name, alt, heading, body, flip=False):
    """One beat of the walkthrough: the screen beside what it does.

    With no screenshot to show it falls all the way back to the plain card
    the page used before there were any, rather than leaving a heading and a
    paragraph floating with nothing to separate them from the next one.
    """
    picture = shot(name, alt)
    if not picture:
        return f'<div class="card">\n<h3>{heading}</h3>\n<p>{body}</p>\n</div>'
    side = "step flip" if flip else "step"
    return (f'<div class="{side}">\n{picture}\n<div class="step-body">\n'
            f'<h3>{heading}</h3>\n<p>{body}</p>\n</div>\n</div>')

page("index.html",
     "NorthPulsar",
     "Behavioral interview preparation, built by an ex Amazon Bar Raiser. The NorthPulsar iPhone app scores your stories, drills them under pressure and tracks every loop to the offer, all on your own phone.",
     "/",
     f"""<header class="{HERO}">
<div class="wrap">
<div class="copy">
{MARK}
<h1>NorthPulsar</h1>
<p>Find your north on the interview loop. Behavioral preparation that works from your own experience, not from a script somebody else wrote.</p>
</div>
{shot("home", "The NorthPulsar home screen, showing readiness for the active job and which competencies are covered")}
</div>
</header>
<main class="wrap">

<p class="lede">Most people walk into a behavioral loop with good stories and no way to find them under pressure. NorthPulsar turns your resume into a scored story bank, shows you which competencies you cannot evidence yet, and drills retrieval until the right story arrives before you need it.</p>

<h2>The iPhone app</h2>
<p>NorthPulsar for iPhone turns your own history into a story bank you can actually reach for in the room, then walks the loop with you from the recruiter screen to the offer call.</p>

{step("stories", "The story bank, each story scored and tagged with the competency it carries", "Build the bank", "Import your resume and NorthPulsar drafts each achievement into a STAR story, scores how strong it is, and shows which competencies you have no evidence for yet. Drafting runs on the phone with Apple Intelligence, and it moves your own words into place rather than inventing an achievement you did not have. You can type or speak every field.")}

{step("mock", "A mock question with the clock running on how long it takes to find a story", "Practice under pressure", "Mocks ask one question at a time. Type or record an answer, and the app times how long you took to find the story, then tells you which signals held up and which did not. Every mock is kept, so the next one is measured against the last.", flip=True)}

{step("jobs", "The Jobs tab, with every role being pursued and one marked active", "Run the loop", "Add every job you are going for and mark one active. Each job carries its posting, its pay band and its rounds. Log the status of each round with your notes or a call transcript, and the app reads the trend toward an offer or a rejection.")}

{step("brief", "A single job opened to its rounds, each with its status and the trend read off them", "Land it", "A rejection becomes a debrief of what held up and what did not, so the next loop starts further along. An offer becomes a plan: where the number sits in the range, what to lead with, what to negotiate and in what order, and what to say on the call.", flip=True)}

<h2>Nothing leaves your phone</h2>
<p>There is no account and no sign in. Your stories, your resume, your practice history and your offer numbers are stored in the app's own container on your device and are never sent to a server. Drafting runs on the phone using Apple Intelligence where the device supports it.</p>
<p class="meta">The one exception, and only when you ask for it: if you paste a link to a job posting, the app fetches that page once so it can read the posting. Paste the text instead and no request is made at all. The full detail is in the <a href="/app/privacy">privacy policy</a>.</p>

<h2>Who builds it</h2>
<p>NorthPulsar is built by a former <strong>Amazon Bar Raiser</strong>, the interviewer brought into hiring loops specifically to judge whether a candidate is ready, with the final say on more than 200 engineering hires in that role.</p>
<p>Outside the loop, that work has meant mentoring more than 500 people into new roles directly, and over 700 more through programs including ADP and Breakthrough Tech. The day job is running engineering for a content platform used by millions.</p>
<p>The app is that loop, run from the other side of the table, put in your pocket.</p>
<p>The builder stays unnamed on purpose. Everything here goes through <a href="mailto:info@northpulsar.com">info@northpulsar.com</a>.</p>

<h2>Status</h2>
<p>NorthPulsar for iPhone is in private beta on TestFlight. It is not yet on the App Store.</p>
<p><a class="btn" href="mailto:info@northpulsar.com?subject=NorthPulsar%20beta">Ask about the beta</a></p>

</main>
""")

page("app/index.html",
     "Support, NorthPulsar for iPhone",
     "Support for the NorthPulsar iPhone app. Contact, common questions, and how to erase your data.",
     "/app",
     f"""<header class="hero">
<div class="wrap">
{MARK}
<p class="eyebrow">NorthPulsar for iPhone</p>
<h1>Support</h1>
<p>Questions, problems and feature requests for the NorthPulsar iPhone app.</p>
</div>
</header>
<main class="wrap">

<h2>Get in touch</h2>
<p>Email <a href="mailto:info@northpulsar.com">info@northpulsar.com</a> and a person reads it. Inside the app, <strong>Settings, Support</strong> opens the same address with your build number, iOS version and device model already filled in, which makes a problem much faster to place.</p>
<p class="meta">App: NorthPulsar for iPhone, published by NorthPulsar. Support is read and answered by the person who builds the app, at info@northpulsar.com.</p>

<h2>Common questions</h2>

<div class="card">
<h3>Where is my data, and how do I erase it?</h3>
<p>Everything you write stays in the app's own container on your iPhone. There is no account and no server holding a copy. To erase all of it, open <strong>Settings</strong> in the app and tap <strong>Erase everything on this phone</strong>. Deleting the app removes it too. Either way it is gone and there is nothing for us to delete on our side, because we never had it.</p>
</div>

<div class="card">
<h3>I imported my resume. What happened to the file?</h3>
<p>It is read on your phone and never copied out of its original location. NorthPulsar keeps the achievement lines it read, in the same local store as your stories, so it can score them and draft from them. The file itself is not transmitted anywhere.</p>
</div>

<div class="card">
<h3>The app did not draft a story from my resume line.</h3>
<p>Drafting uses Apple's on device model, which needs an iPhone with Apple Intelligence turned on. Without it, the app sorts your own words into the four STAR boxes rather than writing prose. Either way nothing is sent off the phone.</p>
</div>

<div class="card">
<h3>Pasting a job link did not work.</h3>
<p>Some job boards block automated fetches or put the posting behind a sign in. Copy the text of the posting and paste that instead. The app reads pasted text exactly the same way, and it makes no network request at all.</p>
</div>

<div class="card">
<h3>Recording an answer is not transcribing.</h3>
<p>Speech to text uses Apple's Speech framework and needs microphone and speech recognition permission. Check <strong>iOS Settings, NorthPulsar</strong> and make sure both are allowed. Audio is never saved by the app.</p>
</div>

<div class="card">
<h3>Can I move my stories to a new phone?</h3>
<p>If you have iCloud Backup or an encrypted local backup turned on, iOS includes NorthPulsar's data in that backup the same as any other app, and restoring to a new phone brings it across. That is handled entirely by Apple.</p>
</div>

<h2>Privacy</h2>
<p>NorthPulsar collects nothing about you. The full policy is at <a href="/app/privacy">northpulsar.com/app/privacy</a>, and the same text is readable inside the app under Settings, Privacy policy.</p>

<h2>Reporting a problem</h2>
<p>The most useful report names what you tapped, what you expected and what happened instead. If you can, send it from <strong>Settings, Support</strong> in the app so the build number travels with it. Please do not paste your resume or anything confidential into a support email. It is never needed to diagnose a problem.</p>

</main>
""")

page("app/privacy/index.html",
     "Privacy Policy, NorthPulsar",
     "NorthPulsar collects no data about you. No account, no analytics, no advertising, no crash reporting, no server holding your stories.",
     "/app/privacy",
     f"""<header class="hero">
<div class="wrap">
{MARK}
<p class="eyebrow">NorthPulsar for iPhone</p>
<h1>Privacy policy</h1>
<p>Last updated 18 September 2026</p>
</div>
</header>
<main class="wrap">
<a class="back" href="/app">Back to support</a>

<p class="lede">NorthPulsar does not collect any data about you. There is no account, no sign in, no analytics, no advertising and no crash reporting library. We run no server that your stories, your resume or your practice history is ever sent to.</p>

<h2>What stays on your phone</h2>
<ul>
<li><strong>Your stories and drafts.</strong> Everything you write is stored in the app's own container on your device.</li>
<li><strong>Your resume.</strong> If you import it, it is read on your phone. The file is never copied out of its original location and its contents are never transmitted. NorthPulsar keeps the achievement lines it read, in the same local store as your stories, so it can score them and draft from them.</li>
<li><strong>Job postings and your loop.</strong> If you paste one, or several, their text is kept on the phone so your fit against each can be scored and the Jobs tab can quote them. The status you set on each round, the notes or call transcripts you type under it, and the offer numbers you enter are kept in the same local store and go with the job when you remove it. The Jobs tab also offers links to public salary sites; tapping one opens a search in Safari, and the app itself sends nothing.</li>
<li><strong>Your practice history.</strong> The questions you answered in mocks, how long you took, how fast you found the story, the score you gave yourself, and the transcript of what you said when you chose to record an answer. Audio is never saved.</li>
</ul>
<p>All of it is removed when you delete the app, or from Settings, "Erase everything on this phone".</p>

<h2>What leaves your phone</h2>
<p>In this version, exactly one thing, and only when you ask for it:</p>
<ul>
<li><strong>A job posting link.</strong> If you paste a link to a posting, the app fetches that page once so it can read the posting. The request carries the link and nothing else. Your resume, your stories and your role never go with it. Paste the posting text instead and no request is made at all.</li>
</ul>
<p>Two features use Apple's own on-device services:</p>
<ul>
<li><strong>Drafting.</strong> On an iPhone with Apple Intelligence, drafts are written on the phone by Apple's on-device model from your own words. Nothing is sent anywhere. Without Apple Intelligence, the app sorts your words into the boxes itself.</li>
<li><strong>Recording an answer in a mock, or dictating a story.</strong> Speech is turned into text by the Speech framework, on the phone when your iPhone supports on-device recognition. On older iPhones, or for some languages, Apple's speech recognition service processes the audio under Apple's privacy terms. The app itself never stores or transmits the audio.</li>
</ul>
<p>A future version may offer to draft from a resume line using a NorthPulsar service. If it does, it will ask first, send only that one line and your target role, and this policy will be updated before that version ships.</p>

<h2>Backups</h2>
<p>If you have iCloud Backup or an encrypted local backup turned on, iOS may include NorthPulsar's data in that backup, the same as it does for other apps. That is handled by Apple under Apple's terms, and NorthPulsar has no access to it.</p>

<h2>Children</h2>
<p>NorthPulsar is rated 4+ and collects nothing from anyone, of any age.</p>

<h2>Changes</h2>
<p>If a future version adds anything that leaves your phone, this policy is updated before that version ships, and the change is called out in the release notes rather than buried here.</p>

<h2>Contact</h2>
<p>Questions about this policy: <a href="mailto:info@northpulsar.com">info@northpulsar.com</a>, or Support in the app's Settings, which opens an email from the phone. The same policy is readable inside the app under Settings, Privacy policy.</p>

</main>
""")

page("404.html", "Page not found, NorthPulsar", "That page does not exist.", "/404",
     f"""<header class="hero"><div class="wrap">{MARK}<h1>Not here</h1>
<p>That page does not exist.</p></div></header>
<main class="wrap"><p><a href="/">Go to northpulsar.com</a></p></main>
""")

(root / "favicon.svg").write_text(BRAND.replace(' class="mark"', '').replace('<svg ', '<svg width="64" height="64" '))
(root / "robots.txt").write_text("User-agent: *\nAllow: /\n\nSitemap: https://northpulsar.com/sitemap.xml\n")
(root / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>https://northpulsar.com{u}</loc><lastmod>2026-09-18</lastmod></url>\n"
              for u in ["/", "/app", "/app/privacy"])
    + "</urlset>\n")
print("favicon.svg, robots.txt, sitemap.xml")
