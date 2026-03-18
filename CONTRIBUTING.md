# Contributing to Yildiz Cipher

Thank you for contributing. This repository is an educational cryptography project, so clarity, reproducibility, and tests matter more than feature volume.

## Project Scope

- Keep changes aligned with educational value and code readability.
- Do not position this cipher as production-grade cryptography.
- Prefer standard-library-first solutions unless a dependency is clearly justified.

## Development Setup

1. Fork and clone the repository.
2. Create and switch to a branch:
```bash
git checkout -b feature/short-topic
```
3. Run tests before and after your change:
```bash
python3 -m unittest test_cipher.py
```

## Branch Naming

- `feature/<short-topic>` for new functionality
- `fix/<short-topic>` for bug fixes
- `docs/<short-topic>` for documentation-only changes
- `test/<short-topic>` for test improvements

## Coding Expectations

- Keep functions focused and reversible where cryptographic transforms are involved.
- Preserve compatibility for current ECB/CBC workflows unless discussed in an issue first.
- Update docs when behavior or CLI usage changes.
- Add or update tests for each behavioral change.

## Testing Expectations

- All existing tests must pass.
- New behavior should include positive and negative test cases when applicable.
- Bug fixes should include regression coverage.

## Commit Messages

Use clear, scoped commit messages. Conventional Commits are recommended:

- `feat: add deterministic avalanche report format`
- `fix: validate CBC ciphertext length before decrypt`
- `docs: clarify CBC IV format in README`

## Pull Request Checklist

Before opening a PR, confirm:

- [ ] Tests pass locally (`python3 -m unittest test_cipher.py`)
- [ ] New behavior is covered by tests
- [ ] README and/or docstrings are updated when needed
- [ ] PR description explains motivation and impact
- [ ] Changes are limited to the stated scope

## Reporting Bugs and Ideas

- Use GitHub issue templates for bug reports and feature requests.
- Include reproducible steps, actual behavior, and expected behavior.
- For cryptography-related changes, include sample input/output where possible.

## Security Notes

- Do not post exploit details publicly before maintainers can assess impact.
- Prefer private reporting through GitHub Security Advisories:
  - https://github.com/Yigtwxx/bsglab/security/advisories/new
