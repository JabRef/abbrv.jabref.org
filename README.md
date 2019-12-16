# Abbreviations

A repository of abbreviations for references, e.g., for conferences, journals, institutes, etc.
Currently, [journal lists](journals/) are offered.

## Format of the file

Since October 2019, the data files are in CSV format (using semicolons as separators):

    <full name>;<abbreviation>[;<shortest unique abbreviation>[;<frequency>]]

The two last fields are optional, and you can actually safely omit them.
JabRef supports the third field, which contains the "shortest unique abbreviation".
The last field is not currently used; its intention is gives frequency (e.g., `M` for monthly).

For instance:

    Accounts of Chemical Research;Acc. Chem. Res.;ACHRE4;M

## Relation to JabRef

JabRef can help you refactor your reference list by automatically abbreviating or unabbreviating journal names.
This requires that you keep one or more lists of journal names and their respective abbreviations.
To set up these lists, choose Options -> Manage journal abbreviations.
See <https://docs.jabref.org/fields/journalabbreviations> for an extensive documentation.

At each release of JabRef, all available journal lists are combined into one and made available to the users.
For more inforamtion see https://app.gitbook.com/@jabref/s/jabref/~/drafts/-LwFEP7BAMSOI10uPlmB/fields/journalabbreviations
