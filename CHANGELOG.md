# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
The project is versioned using [CalVer](https://calver.org/).

## [Unreleased]

## [2025-01-07]

### Added

- Added checker "Escaped Ampersands": `check_ampersands.py` which checks all CSV journals in the folder `journals` to make sure all instances of ampersands are unescaped

### Changed

- `.github/workflows/tests.yml` contains the script `check_ampersands.py`
- Minor format changes in `README.md` and `LISENSE.md` as the old GitHub actions check was already failing
- Found an escaped ampersand using the new script in `journal_abbreviations_dainst.csv` so this was amended.

### Removed

- `[;<frequency>]` was removed, because it was used very seldom - and the data should be collected at other places.
- "Web of Science" abbreviation list was removed. The [data source](https://su.figshare.com/articles/dataset/Journal_abbreviations_from_Web_of_Science/3207787) is from 2016 and had serious issues. [#176](https://github.com/JabRef/abbrv.jabref.org/issues/176)

## 2021-09

Initial tagged release

<!-- markdownlint-disable-file MD012 MD024 MD033 -->

[Unreleased]: https://github.com/JabRef/abbrv.jabref.org/compare/2025-01-07...main
[2025-01-07]: https://github.com/JabRef/abbrv.jabref.org/compare/2021-09...2025-01-07
