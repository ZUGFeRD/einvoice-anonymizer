# einvoice-anonymizer
A python script to remove personal data from EN16931 XML CII e-invoices 

[Andreas Starke](http://4s4u.de/additional_data/impressum/impressum.html) created this file as a pythonesk response to a [feature suggestion](https://github.com/ZUGFeRD/quba-viewer/issues/48)
for [Quba viewer](https://quba-viewer.org/). It can be applied to the XML of e.g. ZUGFeRD 2 invoices or the XML of 
CII XRechnungen and will `shuffle` (i.e. replace a lowercase character by a random lowercase character, 
same with uppercase and number) the text contents of the xpaths defined in testdaten_cii.csv.

## Install

```
python -m venv anon

anon\Scripts\activate.bat

pip install -r requirements.txt
```

## Run 
(but be careful, **this will overwrite the original file**!!)

```
python3 anonymize.py zugferd-invoice.xml ./testdaten_cii.csv shuffle
```

## Maintainer

We're looking for a maintainer :-)