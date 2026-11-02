> [!IMPORTANT]
> This project does not accept fully AI-generated pull requests. AI tools may only be used for assistance. You must understand and take responsibility for every change you submit.
>
> Read and follow:
> • [AGENTS.md](https://github.com/JabRef/jabref/blob/main/AGENTS.md)
> • [CONTRIBUTING.md](../CONTRIBUTING.md)

# Conference abbreviations

`conference_abbreviations_general.csv` contains manually maintained examples from
[JabRef's conference abbreviation issue](https://github.com/JabRef/jabref/issues/12728#issuecomment-2720749311)
and its [INDIN example](https://github.com/JabRef/jabref/issues/12728#issuecomment-2720749399).

Records use the same CSV columns as journal lists:
`"<full name>","<abbreviation>"[,"<shortest unique abbreviation>"]`.
The file has no header and is ordered by full name.

The INDIN record describes the specific 2023 proceedings title. Other years and
title variants need their own records; this data does not imply heuristic title parsing.
Keep conference data separate from `journals/`.

<!-- markdownlint-disable-file MD041 -->
