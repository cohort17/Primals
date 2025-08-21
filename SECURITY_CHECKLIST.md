# Primals Security Checklist

## Python Backend
- [ ] Linting (flake8)
- [ ] Unit tests (pytest)
- [ ] Dependency checks (pip-audit)
- [ ] Input validation for all sensitive endpoints

## Solidity Contracts
- [ ] Linting (solhint)
- [ ] Unit tests (Hardhat)
- [ ] Static analysis (Slither, MythX)
- [ ] Artifact upload for audit logs

## React Frontend
- [ ] Linting (eslint)
- [ ] Unit tests (Jest)
- [ ] Production build
- [ ] Input validation and error handling

## General
- [ ] Secrets managed via GitHub Actions (`secrets`)
- [ ] Audit logs and reports stored as artifacts
- [ ] CI/CD on every commit (see `.github/workflows/`)
- [ ] Automatic deployment (optional, add to workflow)
- [ ] Credits: cohort17 & GitHub Copilot
