---
name: github-issue-puller
description: Pulls a list of issues or a specific issue from a GitHub repository, including title and body.
---

# GitHub Issue Puller

Use this skill when the user asks to "pull," "fetch," or "list" issues from a GitHub repository.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQGWv9TcQcbg6ECBcaUktQf8cnylLvUdcTOCwKki7goZxQMln6ZkicmyP1UFiTJpmiBc-DaBzuKYdeYU89q63N09M54DVGF02EHWgdBsVGdJ3aCJV4-e9uYnHIR2Et6ovvDpBKk4VRr5NvT7EwYa3SNXXgTO)]

## Instructions
1. **Identify Repository:** If the user doesn't specify a repository, assume the current directory's repository or ask for one (e.g., `owner/repo`).[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQGWv9TcQcbg6ECBcaUktQf8cnylLvUdcTOCwKki7goZxQMln6ZkicmyP1UFiTJpmiBc-DaBzuKYdeYU89q63N09M54DVGF02EHWgdBsVGdJ3aCJV4-e9uYnHIR2Et6ovvDpBKk4VRr5NvT7EwYa3SNXXgTO)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQE2Vj2OFD0staQn4HnSnrSHG30Hndirbf2F-27vhOwosy8CgkemfSq9Adiyqvf9W3RhONlDC26RbeUgzeodMT7MoQxkk8IzLtdICtlrKxCIT_zhtczB1BUvRK8TJST6fJ8h1KGSLUs%3D)]
2. **List Recent Issues:** To get a list of the most recent issues with their titles and bodies, run:
   ```bash
   gh issue list --limit 10 --json title,body,number
   ```[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQGWv9TcQcbg6ECBcaUktQf8cnylLvUdcTOCwKki7goZxQMln6ZkicmyP1UFiTJpmiBc-DaBzuKYdeYU89q63N09M54DVGF02EHWgdBsVGdJ3aCJV4-e9uYnHIR2Et6ovvDpBKk4VRr5NvT7EwYa3SNXXgTO)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQE2Vj2OFD0staQn4HnSnrSHG30Hndirbf2F-27vhOwosy8CgkemfSq9Adiyqvf9W3RhONlDC26RbeUgzeodMT7MoQxkk8IzLtdICtlrKxCIT_zhtczB1BUvRK8TJST6fJ8h1KGSLUs%3D)]
3. **Pull Specific Issue:** If a specific issue number is mentioned, run:
   ```bash
   gh issue view <NUMBER> --json title,body
   ```[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQGWv9TcQcbg6ECBcaUktQf8cnylLvUdcTOCwKki7goZxQMln6ZkicmyP1UFiTJpmiBc-DaBzuKYdeYU89q63N09M54DVGF02EHWgdBsVGdJ3aCJV4-e9uYnHIR2Et6ovvDpBKk4VRr5NvT7EwYa3SNXXgTO)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQE2Vj2OFD0staQn4HnSnrSHG30Hndirbf2F-27vhOwosy8CgkemfSq9Adiyqvf9W3RhONlDC26RbeUgzeodMT7MoQxkk8IzLtdICtlrKxCIT_zhtczB1BUvRK8TJST6fJ8h1KGSLUs%3D)]
4. **Formatting:** When presenting the results, clearly separate the Title and the Body. If the body is long, summarize it unless the user asks for the full text.

## Constraints
- Only fetch from public repositories or those the user has authenticated access to via `gh auth`.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQGWv9TcQcbg6ECBcaUktQf8cnylLvUdcTOCwKki7goZxQMln6ZkicmyP1UFiTJpmiBc-DaBzuKYdeYU89q63N09M54DVGF02EHWgdBsVGdJ3aCJV4-e9uYnHIR2Et6ovvDpBKk4VRr5NvT7EwYa3SNXXgTO)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQE2Vj2OFD0staQn4HnSnrSHG30Hndirbf2F-27vhOwosy8CgkemfSq9Adiyqvf9W3RhONlDC26RbeUgzeodMT7MoQxkk8IzLtdICtlrKxCIT_zhtczB1BUvRK8TJST6fJ8h1KGSLUs%3D)]
- Default to the last 10 issues unless specified otherwise.
