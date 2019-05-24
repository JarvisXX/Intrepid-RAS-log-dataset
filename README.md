# Intrepid RAS log dataset
This project is a parser for Intrepid RAS log dataset from Blue Gene/P.

The original dataset is available at https://www.usenix.org/cfdr. After decompression,  you can get the RAS log dataset ```Intrepid_RAS_0901_0908_scrubbed```. However, there are some encoding problems in the decompressed dataset, which is why I decided to parse it.

The parser parses it into dictionaries in Python. The parser is in the ```parse.py```. It is based on Python 2, but it is also easy to be translated into Python 3.

The parsing results are stored in a .json file, namely ```Intrepid_RAS_0901_0908_scrubbed.json```.
