# Property24 Webscraper
Webscraping property24 website for homes for sale, extracting data of each property given a suburb link.

## Requirements
- Python 3.7+
- Tesseract (pytesseract)
- opencv (cv2)
- BeautifulSoup
- Numpy

Make sure to install all of the above requirements before trying to run this script.

## How to run
```commandline
python main.py
```

## How it works
In the file you will see a main method at the bottom with a suburb link specified. This script
will webscrape this link and extract information on all properties listed in that suburb.

The output is the `properties.csv` file that contains the `address`, `Last sold Date`, `Last sold Price` and `url link` for every property found.

Simply run the script and wait for everything to parse. You will see output of each url being parsed and updates as the webscrape continues.

**Note: This was thrown together in an afternoon, so don't judge the code too much ;)**
