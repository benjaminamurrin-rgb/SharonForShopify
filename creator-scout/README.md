# Creator Scout

An AI agent that finds small UK Instagram creators (1k–30k followers) who fit Ari & Co., scores them, and drafts gifting messages for you to review and send.

It runs in **Claude Code on your own computer**. It uses [Agent-Reach](https://github.com/Panniantong/Agent-Reach), which is included in `vendor/Agent-Reach`. Instagram only shows full profiles to logged-in users, and Agent-Reach reuses a login from your own browser, so this can't run in the cloud.

## One-time setup (about 10 minutes, Mac or Linux)

```bash
git clone --recurse-submodules https://github.com/benjaminamurrin-rgb/SharonForShopify.git
cd SharonForShopify

# install uv if you don't have it: https://docs.astral.sh/uv/
uv tool install ./vendor/Agent-Reach
agent-reach setup
agent-reach add instagram       # installs the browser tools it needs
agent-reach login instagram     # you sign in yourself, in the window that opens
agent-reach doctor              # instagram should show as ready
```

**Use a secondary Instagram account**, not @aricoskincare. Instagram can restrict accounts that it thinks are automated.

Don't install `agent-reach` from PyPI. That's a different project.

## Running it

Open Claude Code in this folder and say:

> /creator-scout find 15 new creators

or something like "find Sussex skincare creators for gifting". The agent will:

1. search Instagram and the web, using `search-plan.md`
2. filter and score each creator, using `scoring.md` and `brand-brief.md`
3. add them to `creators.csv` and write a ranked `shortlist.md`
4. draft a personal DM or email for each strong match in `drafts/`

You then read the drafts, make them personal, and send them yourself. After sending, set `status` in `creators.csv` to `contacted`, `accepted`, `posted` or `declined`, so later runs build on what you've learned.

## Files

| File | What it's for |
|---|---|
| `brand-brief.md` | Ari & Co.'s vibe, products, and who is and isn't a fit. Edit this to steer the agent |
| `scoring.md` | The 100-point scoring and the follower range |
| `search-plan.md` | Searches and hashtags to try |
| `outreach-templates.md` | DM and email templates, plus UK #gifted / #ad rules |
| `creators.csv` | The running list of creators |
| `rank.py` | Sorts the list and writes `shortlist.md` |
| `../.claude/skills/creator-scout/SKILL.md` | The agent's step-by-step instructions |

## Updating Agent-Reach

```bash
git submodule update --remote vendor/Agent-Reach
uv tool install --force ./vendor/Agent-Reach
agent-reach update
```
