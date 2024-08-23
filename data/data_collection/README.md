### 📂 **`data_collection` Subfolder**

This subfolder contains two essential subdirectories:

1. **`scraping_code`**: Houses Python scripts used for web scraping:
   - **`practice.py`**: Initial script for practicing web scraping techniques.
   - **`extract_buyrent.py`**: Script for extracting house data from *buyrentkenya.com*.
   - **`extract_propertypro.py`**: Script for extracting house data from *propertypro.co.ke*.

2. **`scraped_data`**: Contains the data obtained from scraping the above sites. 
   - **`consolidated_data.csv`**: A combined dataset used during the cleaning and EDA process.

---

**Note:**

To scrape data from websites, you can use various libraries. Below are the main ones and tutorials on how to use them:

- **BeautifulSoup**: An HTML and XML parser ideal for extracting data from static web pages. It's a great starting point for beginners. [Check out this tutorial](https://youtu.be/XVv6mJpFOb0?si=1UIeaYshLNt-FcVw) for more on using BeautifulSoup.
  
- **Selenium**: Best for handling user interactions and JavaScript-heavy websites, making it suitable for dynamic websites. [Check out this tutorial](https://youtu.be/j7VZsCCnptM?si=t8mkPxCMVSgQ5xeG) for more on using Selenium.
  
- **Scrapy**: Designed for large-scale, concurrent data extraction with built-in features for requests, parsing, crawling, and organizing data. [Check out this tutorial](https://youtu.be/s4jtkzHhLzY?si=_JMA2v4Xh-IgtsgC) for more on using Scrapy.

For this project, **BeautifulSoup** was used to extract data from static websites (*buyrentkenya.com* and *propertypro.co.ke*), as it provided an efficient and straightforward solution.
