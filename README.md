# Abbreviations

A repository of abbreviations for references, e.g., for conferences, journals, institutes, etc.
Currently, a number of [journal lists](journals/) are offered.

## Format of the file

Since October 2019, the data files are in CSV format (using semicolons as separators):

    <full name>;<abbreviation>[;<shortest unique abbreviation>[;<frequency>]]

The abbreviation should follow the ISO4 standard, see <https://marcinwrochna.github.io/abbrevIso/> for details on the abbreviation rules and a search form for title word abbreviations. 
The last two fields are optional, and you can safely omit them.
JabRef supports the third field, which contains the "shortest unique abbreviation".
The last field is not currently used; its intention is to give publication frequency (e.g., `M` for monthly).

For instance:

    Accounts of Chemical Research;Acc. Chem. Res.;ACHRE4;M

## Relation to JabRef

JabRef can help you refactor your reference list by automatically abbreviating or unabbreviating journal names.
This requires that you keep one or more lists of journal names and their respective abbreviations.
To set up these lists, choose Options -> Manage journal abbreviations.
See <https://docs.jabref.org/fields/journalabbreviations> for an extensive documentation.

At each release of JabRef, the available journal lists are combined into two lists that are made available to the users:
* ``journalList.csv`` - contains all lists that follow the ISO4 standard with dots (currently ``acs``, ``ams``, ``geology_physics``, ``mathematics``, ``mechanical``, ``meteorology``, ``sociology``, and ``general``)
* ``journalList_dotless.csv`` - contains all lists that follow the ISO4 standard without dots (currently ``entrez`` and ``medicus``)

In case of duplicate appearances in the journal lists, the last occuring abbreviation is chosen.
