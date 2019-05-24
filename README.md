# Intrepid RAS log dataset
This project is a parser for Intrepid RAS log dataset from Blue Gene/P.

```Intrepid_RAS_0901_0908_scrubbed``` is the RAS log dataset. The original dataset is available at https://www.usenix.org/cfdr. However, there are some encoding problems when I extract the dataset from the .tar file, which is why I decided to parse it.

The parser parses it into dictionaries in Python. The parser is in the ```parse.py```. It is based on Python 2, but it is also easy to be translated into Python 3.

The parsing results are stored in a .json file, namely ```Intrepid_RAS_0901_0908_scrubbed.json```. You can use it directly.
