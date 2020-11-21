# TCP based Web Scraper

Client-server CLI application where client passes URL to the server. Server does web scraping using BeautifulSoup and finds number of leap paragraphs and images in the web page. Then, these numbers are sent to the client.



## Installation

To download app, you need to type following command:

```bash
git clone https://github.com/aydansheydayeva/web_scraper_TCP
```
 Then install requirements to have all packets needed for this project:

```bash
pip install requirements.txt
```

## Usage

To use this app, 2 terminals should be opened. Next 2 commands should be run in terminals:

**Server terminal:**
```
python3 web_scraper.py server
```


**Client terminal:**
```
python3 web_scraper.py client -p [URL]
```

Service is running on port 4444 at 127.0.0.1.