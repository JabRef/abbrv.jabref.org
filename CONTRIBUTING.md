# How to contribute to the journal abbreviation lists

If you find errors or missing journals in the journal abbreviation list used by JabRef, this is the place to submit a correction. If you have an extensive list for your subject area that is not covered by the existing lists, you can consider to add a journal list.

## Corrections and additions to existing journal lists

In any case, you need a [GitHub account](https://github.com/login).

If you don't feel comfortable to touch the lists and create a pull request, [open an issue](https://github.com/JabRef/abbrv.jabref.org/issues) listing the errors and proposed changes or missing entries.

With a little extra effort you can directly edit one of the journal abbreviation files and create a pull request:
1. Go to https://github.com/JabRef/abbrv.jabref.org/tree/master/journals and select the correct file that is most appropriate to your subject area. If none of the files fits your subject, edit `journal_abbreviations_general.csv`.
2. Use the *pencil icon* to start editing the file.
3. Make your corrections. If you add a journal, keep in mind that the list is ordered alphabetically. Make sure to adhere to the [format described below](#format-of-the-file).
4. When done editing, fill out the commit description at the bottom and click *Commit changes*.
5. Create a pull request for your changes.
6. You should now find it in the list of [pull requests](https://github.com/JabRef/abbrv.jabref.org/pulls).

***Note:** For use in JabRef, the topical lists are merged alphabetically with preference given to the last occurence of duplicate journal titles. The general list currently overrides all other lists. Also, an abbreviation might be present in several lists. If you are submitting a correction, check if it exists in several lists due to overlapping subjects or in the general list and make sure all occurences are corrected.*

## Adding a journal list

1. Get a [GitHub account/sign in](https://github.com/login).
2. Add the file to https://github.com/JabRef/abbrv.jabref.org/tree/master/journals (make sure to use the `.csv` format [described below](#format-of-the-file); for importing TXT data files, you should use [this script](../convert_txt2csv.py) before).
3. Add the file to https://github.com/JabRef/abbrv.jabref.org/blob/master/journals/README.md (sorted in alphabetically).
4. Create a pull request on this repository.


## Format of the file

Since October 2019, the data files are in CSV format (using semicolons as separators):

    <full name>;<abbreviation>[;<shortest unique abbreviation>[;<frequency>]]

The abbreviation should follow the ISO4 standard, see <https://marcinwrochna.github.io/abbrevIso/> for details on the abbreviation rules and a search form for title word abbreviations. 
The last two fields are optional, and you can safely omit them.
JabRef supports the third field, which contains the "shortest unique abbreviation".
The last field is not currently used; its intention is to give publication frequency (e.g., `M` for monthly).

For instance:

    Accounts of Chemical Research;Acc. Chem. Res.;ACHRE4;M
