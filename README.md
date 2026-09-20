# Bug Manager

An interactive, **simulated** demo of agentic bug management. Agents scan twelve fictional repositories, rank
what they find, open a pull request with a proposed fix for each finding they can fix, and log a ticket. A team
then burns the ranked list down in one sprint.

Nothing here scans code, calls a language model, or makes a network request. Every repository, finding, pull
request, and ticket is generated in the browser, and the same seed always produces the same 156 findings.

It is the public companion to the case study at <https://davidwaynebaxter.com/ai/bug-manager/>. The real system
ran Claude agents over real repositories, and its findings are confidential.

## Run it

```bash
python3 serve.py                 # http://0.0.0.0:8430/
python3 serve.py --port 9000     # another port
```

No install step and no dependencies. Only `public/` is served, directory listings are off, and the server sends a
strict Content-Security-Policy.

## Keep it running (systemd user service)

```bash
cp bug-manager.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now bug-manager.service
systemctl --user status bug-manager.service
```

Lingering is enabled for this user, so the service starts at boot. To remove it:
`systemctl --user disable --now bug-manager.service`.

## Serve it on a domain

The server listens on port 8430 and accepts any `Host` header, so a reverse proxy can map a name straight to it,
for example `https://bug-manager.projects.davidwaynebaxter.net` to `http://192.168.1.42:8430`.

All asset URLs are relative, so `public/` can also be dropped into any folder of a static host. The production copy lives at
`https://davidwaynebaxter.com/projects/bug-manager/`, deployed from the portfolio repo.

## Layout

```
public/index.html            the app shell (top bar, status bar, cards, workspace, drawer, About dialog)
public/assets/app.js         data generator, scan, ranking, filters, drawer, burn-down sprint
public/assets/app.css        all styles, light and dark themes, no external fonts
public/assets/theme-init.js  applies the saved or system theme before first paint
serve.py                     static server with a strict Content-Security-Policy
bug-manager.service          systemd user unit
```

The app is fully self-contained: it loads no fonts, scripts, or images from any other origin, and the
Content-Security-Policy (`default-src 'self'`, `connect-src 'none'`, no inline styles) enforces that.

## Using it

- The app opens with a completed scan. **Run scan** replays the scan from scratch.
- Click a repository to filter the findings, and click a finding to open its detail drawer (code, reasoning,
  pull request, ticket, and how it was ranked).
- **Play sprint** closes the highest-ranked findings over ten days. The **Burn-down** tab compares that with
  closing the same number in no particular order.
- **About** explains what is simulated and links to the case study.

## How the simulation works

- **Findings.** 156 findings are generated from a library of templates (data consistency, failure risk, security,
  code smell) across 12 fictional repositories, with a fixed random seed.
- **Ranking.** Illustrative only: risk score = severity weight × (1 + the repository's client exposure) × the
  agent's confidence.
- **Pull requests.** A finding gets a simulated pull request unless the agent's confidence is low or the fix
  needs a design decision, in which case it is flagged for an engineer.
- **Burn-down.** A ten-day sprint closes the highest-ranked findings first, and the chart compares that with
  closing the same number in no particular order.
