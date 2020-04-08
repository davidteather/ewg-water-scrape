# ewg-water-scrape 
A commissioned project to scrape the EWG water ratings for water across the US.

## Installation

Execute
```
pip install -r requirements.txt
```

Install chromedriver [here](https://sites.google.com/a/chromium.org/chromedriver/) and add to your environment path.

## Running
Execute
```
python main.py
```

## Data Notes
Not all fields are reported such as [this](https://www.ewg.org/tapwater/system.php?pws=MO6010276) water company is missing the source. Unreported source will be replaced with "N/A"


