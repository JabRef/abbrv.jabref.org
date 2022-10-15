# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## 2021-09

Initial tagged release

## 2022-10

Added Escaped Ampersands Checker

### Added

- check_ampersands.py which checks all csv journals in the journals folder to make
sure all instances of ampersands are unescaped

### Changed

- `.github/workflows/tests.yml` added the above script to the GitHub workflow so the check runs every time the main branch is pushed to
- Minor format changes in `README.md` and `LISENSE.md` as the old GitHub actions check was already failing
- Found an escaped ampersands using the new script in `journal_abbreviations_dainst.csv` so this was ammended

<!-- markdownlint-disable-file MD012 MD024 MD033 -->
