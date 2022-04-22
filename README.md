# spotify-crawler

Since we couldn't find the ranking data for songs by region and their corresponding characteristics, we decided to scrape the data from Spotify by ourselves. The data is divided into two parts. The first part is crawled from Spotifychart. The data includes the daily ranking of the top singles in each region since 2017.

The second part comes from the Spotify web api. According to the data obtained from the first part, the albums are deduplicated according to the songid (unique identification on Spotify). We post the processed data to the Spotify api in the required format and save the feature data returned by the interface.

For the first part, we use selenium to scrape the data. Since the data URL of the Spotify chart is structured, we can easily construct URL links to all the datasets. We called the webdriver through selenium, visited various URLs and clicked the download button on the page to download the file. On average, it takes nearly three seconds per country to process a day's worth of data.

For the second part, we only need to read the official documentation of Spotify web api carefully, register the application on the Spotify developer and complete the relevant configuration, and then we can call the web api for free.
