# Abbreviations
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-3-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

A repository of abbreviations for references, e.g., for conferences, journals, institutes, etc.
Currently, a number of [journal lists](journals/) are offered.

## Format of the file

Since October 2019, the data files are in CSV format (using semicolons as separators):

 ```csv
<full name>;<abbreviation>[;<shortest unique abbreviation>[;<frequency>]]
```

The abbreviation should follow the ISO4 standard, see <https://marcinwrochna.github.io/abbrevIso/> for details on the abbreviation rules and a search form for title word abbreviations.
The last two fields are optional, and you can safely omit them.
JabRef supports the third field, which contains the "shortest unique abbreviation".
The last field is not currently used; its intention is to give publication frequency (e.g., `M` for monthly).

For instance:

```csv
Accounts of Chemical Research;Acc. Chem. Res.;ACHRE4;M
```

*If you want to **add a list or submit corrections**, see the [contribution guidelines](CONTRIBUTING.md).*

## Relation to JabRef

JabRef can help you refactor your reference list by automatically abbreviating or unabbreviating journal names.
This requires that you keep one or more lists of journal names and their respective abbreviations.
To set up these lists, choose Options -> Manage journal abbreviations.
See <https://docs.jabref.org/fields/journalabbreviations> for an extensive documentation.

At each release of JabRef, the available journal lists are combined into two lists that are made available to the users:

* ``journalList.csv`` - contains all lists that follow the ISO4 standard with dots (currently ``acs``, ``ams``, ``geology_physics``, ``mathematics``, ``mechanical``, ``meteorology``, ``sociology``, and ``general``)
* ``journalList_dotless.csv`` - contains all lists that follow the ISO4 standard without dots (currently ``entrez`` and ``medicus``)

In case of duplicate appearances in the journal lists, the last occuring abbreviation is chosen.

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/jlaehne"><img src="https://avatars1.githubusercontent.com/u/7076057?v=4" width="100px;" alt=""/><br /><sub><b>Jonas Lähnemann</b></sub></a><br /><a href="#content-jlaehne" title="Content">🖋</a> <a href="https://github.com/JabRef/abbrv.jabref.org/commits?author=jlaehne" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/dominicelse"><img src="https://avatars0.githubusercontent.com/u/17165189?v=4" width="100px;" alt=""/><br /><sub><b>dominicelse</b></sub></a><br /><a href="#content-dominicelse" title="Content">🖋</a></td>
    <td align="center"><a href="https://github.com/wolfgang-noichl"><img src="https://avatars0.githubusercontent.com/u/294780?v=4" width="100px;" alt=""/><br /><sub><b>Wolfgang Noichl</b></sub></a><br /><a href="#content-wolfgang-noichl" title="Content">🖋</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
