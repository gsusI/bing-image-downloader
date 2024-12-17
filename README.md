# Bing Image Downloader

A Python script to download high-resolution images from Bing Image Search.

## Features

- Search and download high-resolution images from Bing
- Automatically creates organized directories for each search query
- Filters for large images (2000x2000 or larger)
- Skips duplicate downloads
- Handles failed downloads gracefully
- User-agent spoofing to prevent blocks

## Requirements

- Python 3.6+
- Selenium WebDriver
- Chrome Browser
- ChromeDriver

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/bing-image-downloader.git
cd bing-image-downloader
```

2. Install required packages:
```bash
pip install selenium requests
```

3. Make sure you have Chrome and ChromeDriver installed. The ChromeDriver version should match your Chrome browser version.

## Usage

Run the script with a search query and the number of images you want to download:

```bash
python image_downloader.py "search query" number_of_images
```

Example:
```bash
python image_downloader.py "cute cats" 10
```

Images will be downloaded to an `images` directory, organized in subdirectories named after your search queries.

## Notes

- The script uses Selenium with Chrome to scrape image URLs from Bing
- Images are downloaded in their original resolution when available
- The script includes rate limiting and error handling to be respectful to servers
- Downloaded images are organized in directories based on search queries

## License

MIT License

## Contributing

Feel free to open issues or submit pull requests with improvements.
