# Git Flow Strategy - Descubre Boyacá Backend

This project follows **Git Flow** branching strategy for organized development and releases.

## 📊 Branch Structure

```
main (production-ready)
  ├── develop (integration)
  │   ├── feature/* (new features)
  │   ├── enhancement/* (improvements)
  │   └── bugfix/* (bug fixes in develop)
  ├── release/* (release preparation)
  └── hotfix/* (critical production fixes)
```

---

## 🌳 Branch Types

### `main` - Production Branch
- **Purpose**: Production-ready code only
- **Protected**: Yes
- **Accepts merges from**: `release/*`, `hotfix/*` only
- **Never commit directly**: Always merge via PR
- **Naming**: `main`

### `develop` - Integration Branch
- **Purpose**: Latest development changes
- **Protected**: Yes
- **Accepts merges from**: `feature/*`, `enhancement/*`, `bugfix/*` only
- **Never commit directly**: Always merge via PR
- **Naming**: `develop`

### `feature/*` - New Features
- **Purpose**: Develop new features
- **Branch from**: `develop`
- **Merge to**: `develop`
- **Naming**: `feature/feature-name`
- **Examples**:
  - `feature/menus`
  - `feature/favorites-system`
  - `feature/reviews`
  - `feature/user-profiles`

### `enhancement/*` - Improvements
- **Purpose**: Improve existing features (not bugs)
- **Branch from**: `develop`
- **Merge to**: `develop`
- **Naming**: `enhancement/what-to-improve`
- **Examples**:
  - `enhancement/restaurant-filters`
  - `enhancement/performance-optimization`
  - `enhancement/api-documentation`

### `bugfix/*` - Bug Fixes (Development)
- **Purpose**: Fix bugs found in develop branch
- **Branch from**: `develop`
- **Merge to**: `develop`
- **Naming**: `bugfix/bug-description`
- **Examples**:
  - `bugfix/pagination-count`
  - `bugfix/auth-token-expiry`

### `release/*` - Release Preparation
- **Purpose**: Prepare for production release
- **Branch from**: `develop`
- **Merge to**: `main` AND `develop`
- **Naming**: `release/vX.Y.Z` (semantic versioning)
- **Examples**:
  - `release/v1.0.0`
  - `release/v1.1.0`
  - `release/v2.0.0`

### `hotfix/*` - Critical Production Fixes
- **Purpose**: Fix critical bugs in production
- **Branch from**: `main`
- **Merge to**: `main` AND `develop`
- **Naming**: `hotfix/critical-bug-description`
- **Examples**:
  - `hotfix/security-vulnerability`
  - `hotfix/payment-failure`
  - `hotfix/data-corruption`

---

## 🔄 Workflows

### New Feature Development

```bash
# 1. Create feature branch from develop
git checkout develop
git pull origin develop
git checkout -b feature/menus

# 2. Develop and commit
git add .
git commit -m "[ADD]: Menu system implementation"

# 3. Push to remote
git push -u origin feature/menus

# 4. Create PR to develop
# Go to GitHub and create Pull Request: feature/menus → develop

# 5. After PR approval and merge, delete branch
git checkout develop
git pull origin develop
git branch -d feature/menus
git push origin --delete feature/menus
```

### Enhancement Development

```bash
# Same as feature, but use enhancement/* prefix
git checkout -b enhancement/optimize-restaurant-queries
# ... develop, commit, push, PR to develop
```

### Release Process

```bash
# 1. Create release branch from develop
git checkout develop
git pull origin develop
git checkout -b release/v1.0.0

# 2. Version bump, changelog, final fixes
# Update version in pyproject.toml
# Update CHANGELOG.md

# 3. Commit and push
git commit -am "[RELEASE]: Version 1.0.0"
git push -u origin release/v1.0.0

# 4. Create PR to main
# Go to GitHub: release/v1.0.0 → main

# 5. After merge to main, also merge to develop
# Create PR: release/v1.0.0 → develop

# 6. Tag the release on main
git checkout main
git pull origin main
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# 7. Delete release branch
git branch -d release/v1.0.0
git push origin --delete release/v1.0.0
```

### Hotfix Process

```bash
# 1. Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b hotfix/critical-auth-bug

# 2. Fix the bug
git add .
git commit -m "[HOTFIX]: Fix critical authentication bug"

# 3. Push to remote
git push -u origin hotfix/critical-auth-bug

# 4. Create PR to main (urgent!)
# Go to GitHub: hotfix/critical-auth-bug → main

# 5. After merge to main, also merge to develop
# Create PR: hotfix/critical-auth-bug → develop

# 6. Tag the hotfix on main
git checkout main
git pull origin main
git tag -a v1.0.1 -m "Hotfix: Critical auth bug"
git push origin v1.0.1

# 7. Delete hotfix branch
git branch -d hotfix/critical-auth-bug
git push origin --delete hotfix/critical-auth-bug
```

---

## 🛡️ Branch Protection Rules

Configure these rules in GitHub Settings → Branches:

### `main` Branch Protection

- ✅ Require pull request before merging
- ✅ Require approvals: 1
- ✅ Require status checks to pass:
  - CI tests must pass
  - Code coverage minimum
- ✅ Require branches to be up to date
- ✅ Require conversation resolution before merging
- ✅ Do not allow bypassing the above settings
- ✅ Restrict who can push to matching branches
- ✅ Allow only merge commits from: `release/*`, `hotfix/*`

### `develop` Branch Protection

- ✅ Require pull request before merging
- ✅ Require approvals: 1
- ✅ Require status checks to pass:
  - CI tests must pass
  - Linting must pass
- ✅ Require branches to be up to date
- ✅ Do not allow bypassing the above settings
- ✅ Allow only merge commits from: `feature/*`, `enhancement/*`, `bugfix/*`, `release/*`, `hotfix/*`

---

## 📋 Commit Message Convention

Follow the project's commit convention:

```
[VERB]: Short description

Detailed description (optional)
```

### Verbs by Branch Type:

| Branch Type | Recommended Verbs |
|-------------|-------------------|
| `feature/*` | `[ADD]`, `[IMPLEMENT]` |
| `enhancement/*` | `[UPDATE]`, `[IMPROVE]`, `[REFACTOR]` |
| `bugfix/*` | `[FIX]` |
| `hotfix/*` | `[HOTFIX]`, `[FIX]` |
| `release/*` | `[RELEASE]` |

---

## 🏷️ Semantic Versioning

Follow [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`

- **MAJOR** (v2.0.0): Incompatible API changes
- **MINOR** (v1.1.0): Add functionality (backwards compatible)
- **PATCH** (v1.0.1): Bug fixes (backwards compatible)

### Examples:

- `v1.0.0` - Initial production release
- `v1.1.0` - Add menus feature
- `v1.1.1` - Fix pagination bug
- `v1.2.0` - Add favorites system
- `v2.0.0` - Major API redesign

---

## 🚀 Quick Reference

```bash
# Start new feature
make feature name=menus

# Start new enhancement
make enhancement name=optimize-queries

# Start bugfix
make bugfix name=fix-pagination

# Start release
make release version=1.0.0

# Start hotfix
make hotfix name=critical-bug

# Update from develop
git checkout feature/menus
git merge develop

# Rebase on develop (cleaner history)
git checkout feature/menus
git rebase develop
```

---

## 📝 PR Template

When creating a Pull Request, include:

```markdown
## Type of Change
- [ ] Feature
- [ ] Enhancement
- [ ] Bugfix
- [ ] Hotfix
- [ ] Release

## Description
Brief description of changes

## Testing
- [ ] All tests pass (`make test`)
- [ ] Added new tests for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guide
- [ ] Docstrings updated
- [ ] CHANGELOG.md updated (if applicable)
- [ ] No breaking changes (or documented)
```

---

## 🎯 Best Practices

1. **Keep branches short-lived**: Merge features within 1-2 weeks
2. **Small, focused PRs**: Easier to review and test
3. **Update frequently**: Merge develop into your feature branch regularly
4. **Write descriptive commits**: Follow commit convention
5. **Test before PR**: Run `make ci` locally
6. **Clean up**: Delete merged branches
7. **Never force push**: To `main` or `develop`
8. **Rebase carefully**: Only on unshared branches

---

## 🔗 Useful Commands

```bash
# Show all branches
git branch -a

# Show current branch
git branch --show-current

# Delete local branch
git branch -d feature/old-feature

# Delete remote branch
git push origin --delete feature/old-feature

# Sync with develop
git fetch origin
git merge origin/develop

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Stash changes
git stash
git stash pop
```

---

**Last Updated**: October 26, 2025  
**Version**: 1.0.0

