# Abbreviations

A repository of abbreviations for references, e.g., for conferences, journals, institutes, etc.

JabRef can help you refactor your reference list by automatically abbreviating or unabbreviating journal names.
This requires that you keep one or more lists of journal names and their respective abbreviations.
To set up these lists, choose Options -> Manage journal abbreviations.
See also <https://help.jabref.org/en/JournalAbbreviations>.

Currently, only [journal lists](journals/) are offered.

## Format of the file

    <full name> = <abbreviation>;[<shortest unique abbreviation>[;<frequency>]]

The two last fields are not currently used, and you can actually safely omit them.
The intention of the third field is to contain the "shortest unique abbreviation" and the fourth field gives frequency (e.g., `M` for monthly).

For instance:

      Accounts of Chemical Research=Acc. Chem. Res.;ACHRE4;M

This was done in old versions of the "general journals list" primarily because the information was available.
In the current version shipped with jabref (<https://github.com/JabRef/jabref/blob/master/src/main/resources/journals/journalList.txt>), this is not the case any more.
