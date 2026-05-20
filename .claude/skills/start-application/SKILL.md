---
name: start-application
description: >
  Start application skill for iShine. Use this skill when the user has chosen a recommended role
  and wants to begin the real application workflow. It promotes the selected recommendation into a
  real application folder, then hands the saved JD into the write workflow.
---

# Start Application Skill

## Input

$ARGUMENTS — recommendation rank, URL, or a selected role reference from the current recommendation list.

## Steps

### 1. Promote the selected recommendation

Use the recommendation surface when possible:

```bash
python3 -m ops.scripts.start_application --rank <rank>
```

If rank is unavailable, URL is acceptable:

```bash
python3 -m ops.scripts.start_application --url "<selected-job-url>"
```

This must create:
- application folder
- `jd.md`
- tracker entry in `drafting`

### 2. Hand off into write

Use the promoted `jd.md` as the input for the write workflow.

The user should experience this as:
- choose role
- application starts
- iShine begins tailoring

Do not make the user manually discover queue slugs or internal folder names.
