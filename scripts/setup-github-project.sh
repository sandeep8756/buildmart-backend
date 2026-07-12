#!/usr/bin/env bash
# Link both M&P repos to GitHub Project #2 and add open issues to the board.
# Requires: gh CLI authenticated with project + repo scopes.
set -euo pipefail

OWNER="sandeep8756"
PROJECT_NUMBER=2
REPOS=("buildmart" "buildmart-backend")

echo "==> Checking gh auth (needs project + repo scopes)..."
if ! gh auth status >/dev/null 2>&1; then
  echo "Run: gh auth login"
  exit 1
fi

echo "==> Project info"
gh project view "$PROJECT_NUMBER" --owner "$OWNER" || {
  echo "Cannot access project. Update PAT at https://github.com/settings/tokens"
  echo "Required scopes: project, repo"
  exit 1
}

echo "==> Link repositories to project"
for repo in "${REPOS[@]}"; do
  echo "  Linking $OWNER/$repo ..."
  gh project link "$PROJECT_NUMBER" --owner "$OWNER" --repo "$OWNER/$repo" || true
done

echo "==> Add open issues from both repos to project board"
PROJECT_ID=$(gh api graphql -f query='
  query($login: String!, $number: Int!) {
    user(login: $login) { projectV2(number: $number) { id title } }
  }' -f login="$OWNER" -F number="$PROJECT_NUMBER" --jq '.data.user.projectV2.id')

for repo in "${REPOS[@]}"; do
  gh issue list --repo "$OWNER/$repo" --state open --json id,number,title --jq '.[] | "\(.number)\t\(.title)"' | while IFS=$'\t' read -r num title; do
    echo "  Adding issue #$num from $repo: $title"
    ISSUE_ID=$(gh api graphql -f query='
      query($owner: String!, $name: String!, $number: Int!) {
        repository(owner: $owner, name: $name) {
          issue(number: $number) { id }
        }
      }' -f owner="$OWNER" -f name="$repo" -F number="$num" --jq '.data.repository.issue.id')
    gh api graphql -f query='
      mutation($projectId: ID!, $contentId: ID!) {
        addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
          item { id }
        }
      }' -f projectId="$PROJECT_ID" -f contentId="$ISSUE_ID" >/dev/null || true
  done
done

echo "==> Done. Open: https://github.com/users/$OWNER/projects/$PROJECT_NUMBER"
