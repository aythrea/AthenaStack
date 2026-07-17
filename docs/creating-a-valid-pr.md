# Creating a Valid AthenaStack Pull Request

This guide explains the complete AthenaStack change process.

Follow the steps in order. Do not begin by editing `main`.

---

## The Required Process

Every AthenaStack change follows this path:

```text
Create Issue
    ↓
Create Branch
    ↓
Make Changes
    ↓
Commit and Push
    ↓
Open Pull Request
    ↓
Pass PR Policy and CI Checks
    ↓
Merge into main
```

---

## Step 1: Create a GitHub Issue

Before creating a branch or editing files, create an Issue describing the work.

In GitHub:

1. Open the AthenaStack repository.
2. Select **Issues**.
3. Select **New issue**.
4. Give the issue a clear title.
5. Describe the intended change.
6. Create the issue.

Example:

```text
Issue title:
Document the AthenaStack platform standards
```

After creating it, GitHub assigns an issue number.

Example:

```text
#12
```

Write down that number. It will be used in the branch name, pull-request title, and pull-request description.

The issue must remain **open** until the pull request is merged.

---

## Step 2: Create a Working Branch

Never make the change directly on `main`.

Create a branch from the latest version of `main`.

Recommended branch format:

```text
<issue-number>-<short-description>
```

Example:

```text
12-platform-documentation
```

The branch-name format is currently a convention rather than an automated requirement, but using it makes the work easy to identify.

### Command-line example

```bash
git switch main
git pull
git switch -c 12-platform-documentation
```

This does three things:

1. Switches to `main`.
2. downloads the latest version of `main`;
3. creates and switches to the new working branch.

Confirm the active branch:

```bash
git branch --show-current
```

Expected output:

```text
12-platform-documentation
```

Do not continue if the output is:

```text
main
```

---

## Step 3: Make the Change

Edit only the files needed for the issue.

For example:

```text
docs/
├── README.md
├── stack-standards.md
├── github-governance.md
└── roadmap.md
```

Before committing, inspect the changes:

```bash
git status
git diff
```

Confirm that:

* the expected files changed;
* unrelated files did not change;
* no credentials or secrets were added;
* the change matches the issue.

---

## Step 4: Commit the Change

Stage the intended files:

```bash
git add docs/
```

Create a commit with a clear description:

```bash
git commit -m "Add AthenaStack platform documentation"
```

A good commit message describes what the commit does.

Good:

```text
Add AthenaStack platform documentation
```

Avoid:

```text
changes
update
stuff
fix
```

---

## Step 5: Push the Branch

Push the branch to GitHub:

```bash
git push -u origin 12-platform-documentation
```

The `-u` option connects the local branch to the matching GitHub branch. Later pushes can use:

```bash
git push
```

---

## Step 6: Open the Pull Request

Open a pull request from the working branch into `main`.

Confirm:

```text
Base branch: main
Compare branch: 12-platform-documentation
```

Do not reverse these.

The intended direction is:

```text
12-platform-documentation
        ↓
       main
```

---

## Step 7: Format the Pull-Request Title

The title must begin with the issue number.

Required format:

```text
#<issue-number> <description>
```

Example:

```text
#12 Add AthenaStack platform documentation
```

Correct:

```text
#12 Add AthenaStack platform documentation
```

Incorrect:

```text
Add AthenaStack platform documentation
```

Incorrect:

```text
12 Add AthenaStack platform documentation
```

Incorrect:

```text
Issue #12 - Add AthenaStack documentation
```

Incorrect:

```text
#12
```

There must be:

1. a number sign;
2. the open issue number;
3. a space;
4. a meaningful title.

---

## Step 8: Link the Issue in the PR Description

Under the **Ticket** heading, enter:

```text
Closes #12
```

Use the same issue number that appears at the beginning of the title.

Complete example:

```markdown
## Ticket

Closes #12

## Summary

Adds the initial AthenaStack platform standards, GitHub governance,
and CI/CD roadmap documentation.

## Validation

- [ ] MegaLinter passes.
- [ ] Docker Compose validation passes.
- [ ] AthenaStack policy validation passes.
- [x] The documentation was reviewed for accuracy.

## Operational considerations

Documentation-only change. No running containers or production services
are affected.
```

The safest convention is always:

```text
Closes #<issue-number>
```

Do not write only:

```text
#12
```

Do not use a different issue number from the PR title.

For example, this will fail:

```text
PR title:
#12 Add platform documentation

PR body:
Closes #13
```

The issue referenced in the title and body must match.

---

## Step 9: Create the Pull Request

Before selecting **Create pull request**, verify:

```text
[ ] Base branch is main
[ ] Source branch is not main
[ ] Title starts with #<issue-number>
[ ] Title contains text after the issue number
[ ] Body contains Closes #<same-issue-number>
[ ] Referenced issue exists
[ ] Referenced issue is still open
```

Then create the pull request.

---

## Step 10: Read the Automated Checks

The PR Policy workflow checks:

* whether the title starts with an issue number;
* whether the body contains a closing reference;
* whether both references use the same number;
* whether that number identifies an existing GitHub Issue;
* whether the issue is open;
* whether the number points to an Issue rather than another PR.

Other workflows may also check:

* Markdown and YAML formatting;
* GitHub Actions syntax;
* Docker Compose validity;
* AthenaStack-specific policy.

---

## Correcting a Failed PR Policy Check

A failed policy check does not usually require a new branch or PR.

Open the PR and read the failed check.

### Failure: Invalid PR title

Example error:

```text
The title must begin with a GitHub issue number.
```

Edit the PR title.

Change:

```text
Add documentation
```

to:

```text
#12 Add documentation
```

Save the title.

The PR Policy workflow should run again automatically.

---

### Failure: Ticket not linked

Example error:

```text
The PR description must contain a closing reference to the same ticket.
```

Edit the PR description and add:

```text
Closes #12
```

Make sure `#12` matches the number at the beginning of the title.

Save the description. The policy check should run again.

---

### Failure: Referenced issue does not exist

The issue number is incorrect or was never created.

Confirm the issue number in GitHub.

Then update both:

```text
PR title
PR description
```

Example:

```text
Title:
#12 Add documentation

Body:
Closes #12
```

---

### Failure: Ticket is not open

The issue was closed before the PR was merged.

Reopen the issue, then rerun or update the PR.

The issue should remain open while the PR is under review. The `Closes #12` reference is intended to close it automatically when the PR is merged.

---

### Failure: Number points to a pull request

GitHub Issues and pull requests share the same repository number sequence.

For example, `#12` might be a PR rather than an Issue.

Create or locate the correct open Issue, then update the PR title and body with that Issue number.

---

## Updating the Pull Request

Additional commits can be made on the same branch:

```bash
git add .
git commit -m "Correct documentation"
git push
```

Pushing a new commit updates the existing pull request automatically.

Do not create a new pull request for every correction.

---

## Final Merge Checklist

Merge only when:

```text
[ ] PR Policy passes
[ ] MegaLinter passes
[ ] Compose validation passes when applicable
[ ] AthenaStack policy validation passes when applicable
[ ] The diff contains only intended changes
[ ] No secrets are present
[ ] Operational impact is documented
```

After merging:

1. Confirm the associated issue closed.
2. Delete the remote working branch when it is no longer needed.
3. Update the local repository:

```bash
git switch main
git pull
git branch -d 12-platform-documentation
```

---

## Complete Example

### Issue

```text
#12 Document AthenaStack standards
```

### Branch

```text
12-platform-documentation
```

### Commit

```text
Add AthenaStack platform documentation
```

### PR title

```text
#12 Add AthenaStack platform documentation
```

### PR body

```markdown
## Ticket

Closes #12

## Summary

Adds the AthenaStack platform standards and governance documentation.

## Validation

- [x] MegaLinter passes.
- [x] The documentation was reviewed for accuracy.

## Operational considerations

Documentation-only change. No production impact.
```

### Result

```text
PR Policy: Passed
```

---

## One-Line Memory Aid

```text
Issue #12 → branch 12-description → PR title #12 Description → body Closes #12
```
