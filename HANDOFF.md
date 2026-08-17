# Handoff — ansonchu.com

**Goal:** Personal site for Anson Chu (software engineer, job-hunting). Extended
resume + blog of 5–10 opinion pieces (AI alignment, RL, hardware/silicon,
markets). Minimal "engineering notebook" aesthetic, mobile + dark mode,
hand-written HTML/CSS, no build step.

## Local files: `~/ansonchu.com/`
- `index.html` — homepage: bio + links + writing index (changelog-style, grouped by theme)
- `style.css` — full design system, one file (system serif + mono, ink-blue accent)
- `writing/why-reward-models-drift.html` — example post (edit or delete)
- `CNAME` — contains `ansonchu.com`

## Hosting: GitHub Pages
- Repo: `github.com/kumikoda/ansonchu.com` (GitHub user is **kumikoda**), pushed to `main`
- Pages enabled, custom domain `ansonchu.com` set, HTTPS auto-enables after DNS
- Deploy workflow: edit → `git commit` → `git push` → live in ~1 min

## Domain
Registered at **Squarespace Domains** (was Google Domains). DNS managed at Squarespace.

### DNS records to add (user's task, may be partly done)
- 4× `A` @ → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
- 1× `CNAME` www → `kumikoda.github.io`

## Open items
1. Confirm DNS added + verify https://ansonchu.com resolves
2. Fill `[ bracket ]` placeholders in `index.html` (role, bio, previous company)
3. Verify/fix LinkedIn + X links (currently guessed placeholders); GitHub link already set to kumikoda
4. Write real posts (copy the example file, rename = new URL, add `<li>` to homepage index)

## Note
A local preview server runs at `http://localhost:8787/` (python http.server, background).
