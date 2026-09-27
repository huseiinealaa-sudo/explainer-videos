# Privacy check of the pull request (the repository is PUBLIC)

Run after the PR is opened, over everything it contains; fix, push to the same PR and say
so in its description if anything is found.

1. List what the PR adds: `git diff --stat origin/main...HEAD` and
   `git diff origin/main...HEAD --name-only`.
2. Search the added text for real identifiers (review every hit by eye):
   ```bash
   git diff origin/main...HEAD -U0 | grep '^+' | grep -nEi \
     '[A-Z]{2,}-?[0-9]{3,}|serial|s/n|tag[: ]|[0-9]{1,2}[/.-][0-9]{1,2}[/.-](19|20)[0-9]{2}|@[a-z0-9.-]+\.[a-z]{2,}|\b([0-9]{1,3}\.){3}[0-9]{1,3}\b|lat|lon|gps|km ?[0-9]'
   ```
   Illustrative values are fine when the project's `CLAUDE.md` or data module marks them as
   illustrative (e.g. `PRV-DEMO-001`); anything else that looks like a real serial, tag,
   meter or site name, date, location, person or measured value is removed or replaced.
3. Every number on screen or in the narration comes from the data module, and the data
   module holds illustrative inputs or published manual values only.
4. Look through the contact sheets of the final QA run: no screenshots of real screens, no
   real names or identifiers in drawn windows, reports or tables (simplified drawings only).
5. `sources/*.md` hold public references (URL, document number, page), never private
   documents or site notes.
6. Videos under 100 MB; only final videos in `output/`; no `media/`, audio or `tmp/`.
