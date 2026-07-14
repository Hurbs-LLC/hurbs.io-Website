#!/usr/bin/env python3
"""Generate public/services/*.html. Copy follows Hurbs voice rules:
we-voice, no em dashes, no MSP-speak, plain CTAs."""
import html
import os
import sys
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blog_data import POSTS, LANES, CHIP_TO_SLUG, FEATURED
from common import head, nav, cta_band, blog_cards, FOOTER

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, 'public', 'services')
POSTS_BY_SLUG = {p['slug']: p for p in POSTS}

SERVICES = [
    dict(slug='it-support', num='01', c='red', title='IT Support & Managed Services',
         blurb="Your computers, email, and network, kept running by people who answer when you call. We monitor things before they break and fix them fast when they do.",
         includes=['Help desk that reaches a real person', 'Proactive monitoring & patching', 'Email, accounts & device management', 'Vendor wrangling (ISPs, printers, licenses)', 'On-site visits when remote won’t cut it'],
         tools=['Microsoft 365', 'Google Workspace', 'Windows & Mac', 'Remote monitoring', 'Automated patching', 'Help desk tooling', 'Device management', 'Email security', 'Spam filtering', 'Backup & restore', 'Onboarding & offboarding', 'License management', 'Vendor wrangling', 'Asset tracking', 'Printer & peripheral duty', 'Server care', 'Slack & Teams', 'TeamViewer', 'Ubiquiti', 'Warranty & procurement', 'Documentation', 'On-site visits'],
         why=[('No ticket purgatory', 'Email Mason, get Mason. Issues get owned, not routed.'),
              ('Flat and fair', 'Priced for small businesses, not per-incident nickel-and-diming.'),
              ('We show up', 'If hands are needed, we fly out or send trusted local techs.')]),
    dict(slug='cloud', num='02', c='yellow', title='Cloud Setup & Migration',
         blurb="Move to Azure, AWS, or Google Cloud without the drama, and stop paying for servers you don't use. We migrate, tune, and hand you the keys.",
         includes=['Cloud readiness check & honest recommendation', 'Migration planning & execution', 'Cost tuning (right-sizing, reserved pricing)', 'Backup & disaster recovery in the cloud', 'Training so your team can run it'],
         tools=['Azure', 'AWS', 'Google Cloud', 'Cloudflare', 'Microsoft 365', 'Terraform', 'Kubernetes', 'Docker', 'Lift-and-shift migrations', 'Zero-downtime cutovers', 'Hybrid cloud', 'Cost optimization', 'Right-sizing', 'Reserved pricing', 'Cloud backups', 'Disaster recovery', 'Serverless', 'Storage & CDN', 'VPNs & private networking', 'Identity & access', 'Monitoring & alerts', 'Linux & Windows servers', 'Email migration'],
         why=[('No lock-in agenda', 'We recommend what fits you, not what pays us referral fees.'),
              ('Bills you understand', 'We tune costs so the cloud is cheaper than the closet.'),
              ('Handover included', 'Documentation and training, so you’re not stuck renting us forever.')]),
    dict(slug='cybersecurity', num='03', c='green', title='Cybersecurity',
         blurb="Locks on the doors: backups, monitoring, and training that keep you off the news. Sized for real businesses, not Fortune 500 budgets.",
         includes=['Security check-up & plain-English risk report', 'Backups & recovery you’ve actually tested', 'Endpoint protection & monitoring', 'Phishing training for your team', 'Compliance basics (HIPAA, PCI, SOC 2 prep)'],
         tools=['Endpoint protection', 'EDR/XDR', '24/7 monitoring', 'Threat hunting', 'Ransomware defense', 'Tested backups', 'Incident response', 'Phishing simulations', 'Security training', 'MFA everywhere', 'Password managers', 'Zero trust', 'Firewalls', 'Email security', 'VPNs', 'Vulnerability scanning', 'Penetration testing', 'Dark web monitoring', 'HIPAA', 'PCI DSS', 'SOC 2 prep', 'NIST CSF', 'Okta', 'Microsoft Defender'],
         why=[('Right-sized', 'Security that matches your actual risk. No fear-selling.'),
              ('Tested, not assumed', 'We restore from your backups to prove they work.'),
              ('People included', 'Most breaches start with a click. We train the clickers.')]),
    dict(slug='software', num='04', c='blue', title='Custom Software',
         blurb="Programmers on deck for the tool your business actually needs: an internal app, an integration, a customer portal. Built lean, no bloat.",
         includes=['Scoping in plain English, fixed quotes', 'Web apps & internal tools', 'Integrations between the systems you already use', 'Automation of repetitive work', 'Maintenance without hostage pricing'],
         tools=['JavaScript/TypeScript', 'Python', 'React', 'Node.js', 'PostgreSQL', 'REST APIs', 'GraphQL', 'Web apps', 'Mobile apps', 'Internal tools', 'Customer portals', 'Dashboards', 'Integrations', 'Workflow automation', 'AI features', 'Payments', 'Text & email alerts', 'CI/CD', 'Docker', 'Cloud hosting', 'Legacy rescues', 'Data migrations', 'Testing & QA', 'Ongoing maintenance'],
         why=[('On deck, not on retainer', 'Our devs spin up when you have work, so you don’t fund a bench.'),
              ('Small and shippable', 'We build the 20% you’ll use, not the 80% you won’t.'),
              ('You own it', 'Your code, your accounts, your data. Documented handoff.')]),
    dict(slug='networks', num='05', c='red', title='Networks & Infrastructure',
         blurb="Cabling, Wi-Fi, servers, and racks, built clean, labeled, and documented. The kind of closet the next tech thanks you for.",
         includes=['Network design & buildout', 'Business Wi-Fi that reaches the back office', 'Server & rack setup or cleanup', 'Office moves & new-location standups', 'Documentation & labeling (yes, really)'],
         tools=['Ubiquiti', 'Cisco', 'Meraki', 'pfSense', 'Firewalls', 'VLANs', 'Business Wi-Fi', 'Wi-Fi coverage mapping', 'Fiber & Cat6', 'Structured cabling', 'Rack builds', 'Patch panels', 'Server rooms', 'Cameras & access control', 'VoIP phones', 'VPNs', 'Failover internet', 'Switching & routing', 'Windows Server', 'Active Directory', 'Virtualization', 'NAS & storage', 'UPS & power', 'Labeling & documentation'],
         why=[('We fly out', 'Physical work anywhere in the country: Mason on a plane, or vetted local crews.'),
              ('Done right once', 'Clean runs and labels beat cheap-now, mystery-later.'),
              ('Documented', 'Maps, passwords, and diagrams handed over, not held over you.')]),
    dict(slug='data-ai', num='06', c='yellow', title='Data & AI Analytics',
         blurb="Numbers you can act on. We pull your scattered data together, build dashboards people actually open, and apply AI where it genuinely helps.",
         includes=['Data cleanup & consolidation', 'Dashboards & reporting (live, not monthly PDFs)', 'Forecasting & trend analysis', 'Practical AI: assistants, document processing, automation', 'Training so your team trusts the numbers'],
         tools=['Power BI', 'Looker Studio', 'Python', 'SQL', 'Excel (no shame)', 'Live dashboards', 'KPI reporting', 'Forecasting', 'Data cleanup', 'Data warehouses', 'ETL pipelines', 'Claude & LLM APIs', 'AI assistants', 'Document processing', 'Workflow automation', 'Spreadsheet rescues', 'Customer analytics', 'Sales & inventory data', 'Plain-English reports', 'Training & handoff'],
         why=[('Useful before impressive', 'One dashboard people check daily beats ten nobody opens.'),
              ('AI without the hype', 'We’ll tell you when a spreadsheet is the right answer.'),
              ('Your data stays yours', 'Built in your accounts, with your keys.')]),
    dict(slug='digital', num='07', c='green', title='Digital Transformation',
         blurb="Old process, new tools. We take the paper forms, the shared-drive chaos, the 'it lives in Carol's head' workflows, and make them systems.",
         includes=['Process walkthrough & honest priorities', 'Replacing paper & spreadsheet workflows', 'Modernizing legacy apps that still matter', 'Process automation & handoffs', 'Change help: training, not just tools'],
         tools=['Microsoft 365', 'Google Workspace', 'SharePoint', 'Teams', 'Slack', 'Power Automate', 'Zapier/Make', 'Airtable', 'Paper-to-digital', 'E-signatures', 'Approvals & workflows', 'Process automation', 'Document management', 'Intranets', 'Scheduling & booking', 'Legacy app rescues', 'QuickBooks integrations', 'Custom tooling', 'Training & rollout', 'Change management'],
         why=[('One bite at a time', 'We fix the workflow that hurts most first, not a 2-year roadmap.'),
              ('People-first', 'Tools only stick if the team likes them. We train until they do.'),
              ('Priced fair', 'Transformation without the consulting-firm invoice.')]),
    dict(slug='staffing', num='08', c='blue', title='Staffing & Recruiting',
         blurb="The right tech hires, vetted by people who do the work. Contract crews for a project, or permanent hires for your team, anywhere in the country.",
         includes=['Tech screening by actual technicians', 'Contract crews for projects & rollouts', 'Direct-hire recruiting for IT roles', 'Local hands in other cities, managed by us', 'Backfill & temp coverage'],
         tools=['Direct hire', 'Contract crews', 'Contract-to-hire', 'Temp-to-perm', 'W-2 or 1099', 'Help desk techs', 'Sysadmins', 'Network engineers', 'Developers', 'Field techs', 'Cabling crews', 'Project rollouts', 'Nationwide coverage', 'Tech-led screening', 'Skills testing', 'Background checks', 'Same-week placements', 'Backfill coverage', 'Managed teams', 'Payroll handled'],
         why=[('Vetted by doers', 'Candidates are screened by techs, not keyword-matching recruiters.'),
              ('We’ve got backup', 'If a placement doesn’t work out, we make it right.'),
              ('Flexible', 'One tech for a day or a crew for a quarter.')]),
]

e = html.escape

def page(svc):
    mailto = 'mailto:mason@hurbs.io?subject=' + quote('Question about ' + svc['title'])
    c = svc['c']
    includes = '\n'.join(
        f'''      <div class="include-row">
        <div class="include-sq sq-{c}"></div>
        <span>{e(i)}</span>
      </div>''' for i in svc['includes'])
    def chip(t):
        slug = CHIP_TO_SLUG.get(t)
        if slug:
            return f'        <a class="chip" href="/blog/{slug}">{e(t)}</a>'
        return f'        <span class="chip">{e(t)}</span>'
    chips = '\n'.join(chip(t) for t in svc['tools'])
    whys = '\n'.join(
        f'''      <div>
        <div class="why-sq sq-{c}"></div>
        <h3>{e(w[0])}</h3>
        <p>{e(w[1])}</p>
      </div>''' for w in svc['why'])
    others = '\n'.join(
        f'''    <a href="/services/{o['slug']}" class="other-row">
      <span class="other-num num-{o['c']}">{o['num']}</span>
      <span class="other-title">{e(o['title'])}</span>
      <span class="other-arrow">→</span>
    </a>''' for o in SERVICES if o['slug'] != svc['slug'])

    cards = blog_cards(FEATURED[svc['slug']], POSTS_BY_SLUG, LANES)

    return head(f"{svc['title']} | Hurbs LLC", svc['blurb'],
                canonical=f"/services/{svc['slug']}") + f'''
<div class="page">
{nav('services')}

  <header class="svc-hero">
    <a href="/#services" class="svc-breadcrumb">← ALL SERVICES</a>
    <div class="svc-mark">
      <span class="svc-num num-{c}">{svc['num']}</span>
      <div class="svc-sq sq-{c}"></div>
    </div>
    <h1>{e(svc['title'])}</h1>
    <p class="svc-blurb">{e(svc['blurb'])}</p>
    <a href="{mailto}" class="btn btn--sm">Ask us about this →</a>
  </header>

  <section class="svc-cols">
    <div class="svc-includes">
      <h2>What's included</h2>
      <p class="svc-col-sub">Scoped to what you actually need, never the whole list by default.</p>
{includes}
    </div>
    <div class="svc-tools">
      <h2>Tools we reach for</h2>
      <p class="svc-col-sub">Whatever fits. These come up a lot.</p>
      <div class="tool-chips">
{chips}
      </div>
    </div>
  </section>

  <section class="svc-why">
    <h2>Why do it with Hurbs</h2>
    <div class="why-grid">
{whys}
    </div>
  </section>

  <section class="others">
    <div class="others-head"><span>EVERYTHING ELSE WE DO</span></div>
{others}
  </section>

{cards}

{cta_band()}

{FOOTER}
'''

os.makedirs(OUT, exist_ok=True)
for svc in SERVICES:
    path = os.path.join(OUT, svc['slug'] + '.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(page(svc))
    print('wrote', path)
