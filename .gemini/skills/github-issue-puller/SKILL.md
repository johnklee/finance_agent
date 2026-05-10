---
name: github-issue-puller
description: Pulls a list of issues or a specific issue from a GitHub repository, including title and body.
---

# GitHub Issue Puller

Use this skill when the user asks to "pull," "fetch,", "get" or "list" issues from a GitHub repository.

## Instructions
1. **Identify Repository:** If the user doesn't specify a repository, assume the current directory's repository (which is `https://github.com/johnklee/finance_agent`).
2. **List Recent Issues:** To get a list of the most recent issues with their titles and bodies, run:
   ```bash
   gh issue list --limit 10 --json title,body,number
   ```
3. **Pull Specific Issue:** If a specific issue number is mentioned, run:
   ```bash
   gh issue view <NUMBER> --json title,body
   ```
4. **Formatting:** When presenting the results, clearly separate the Title and the Body. If the body is long, summarize it unless the user asks for the full text.

## Constraints
- Only fetch from public repositories or those the user has authenticated access to via `gh auth`.
- Default to the last 10 issues unless specified otherwise.
