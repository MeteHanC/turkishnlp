# Turkish NLP

Very early version of the TurkishNLP. For now it has basically 2 main functions; Detecting Turkish Language and correcting typos in Turkish words.

## Dataset
Dataset was created by parsing and filtering a Turkish wikipedia dump. 

## Getting Started
To get started first you need to install the package. With using pip;
```
pip install turkishnlp
```
After installing the package succesfully try and import the package.

```
import turkishnlp
```
### Downloading the data
To download the data first we need to create an instance of TurkishNLP class. So we need to ;
```
from turkishnlp import detector
obj = detector.TurkishNLP()
```
After creating the instance we can simply call the download function like this;

```
obj.download()
```
It will take shortly and after the download it will print out "Download succesful". You won't have to download the data again.

### Creating the wordset
To create the wordset from data you need to ;
```
obj.create_word_set()
```
And it will create the wordset and necesary dictionaries.

### Example Usage
So there are 2 main functions, detecting if the language is Turkish and Turkish typo correction. For detecting the language;
```
print(obj.is_turkish("Ben bugün ankaraya gideceğim belki birşeyler alırım"))
```
Will return us "True" along with the accuracy point which is 0.85

For the other function which is "Typo Correction", you can simply do;

```
lwords = obj.list_words("vri kümsi idrae edre ancaka daha güezl oalbilir")
print(obj.auto_correct(lwords))
```
Which will print out ['veri', 'kümesi', 'idare', 'eder', 'ancak', 'daha', 'güzel', 'olabilir']. You can simply use "join" to make it a sentence again like this;

```
lwords = obj.list_words("vri kümsi idrae edre ancaka daha güezl oalbilir")
corrected_words = obj.auto_correct(lwords)
corrected_string = " ".join(corrected_words)
```
Which will print out 'veri kümesi idare eder ancak daha güzel olabilir'. 
