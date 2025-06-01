# Python Utilities

This repository contains various Python utilities:

1. Web Scraper Application - Fetches data from websites, extracts specific information, and saves it to CSV files
2. MKV to MP4 Converter - Converts MKV video files to MP4 format using FFmpeg

## Features

- Scrape data from news websites and product listings
- Extract headlines, dates, and summaries from news sites
- Extract product names, prices, and ratings from e-commerce sites
- Save extracted data to CSV files
- User-friendly GUI built with PyQt6

## Requirements

- Python 3.6 or higher
- PyQt6
- Requests
- BeautifulSoup4

## Installation

1. Clone this repository or download the source code
2. Install the required dependencies using one of the following methods:

### Method 1: Using pip directly

```bash
pip install PyQt6==6.5.3 requests beautifulsoup4
```

### Method 2: Using requirements.txt (recommended)

```bash
pip install -r requirements.txt
```

If you encounter a "ModuleNotFoundError: No module named 'requests'" or similar error, it means you need to install the required dependencies using one of the methods above.

## Usage

1. Run the application:

```bash
python main.py
```

### Web Scraper Tab

1. Select the "Web Scraper" tab
2. Enter a website URL in the input field
3. Select the type of data to extract (News or Products)
4. Click "Fetch Data" to scrape the website
5. Review the extracted data in the table
6. Click "Save to CSV" to save the data to a CSV file

### MKV to MP4 Converter Tab

1. Select the "MKV to MP4 Converter" tab
2. Click "Open MKV to MP4 Converter" to launch the converter window
3. Use the converter interface to:
   - Select an input MKV file
   - Optionally specify an output MP4 file
   - Configure conversion options (codecs, quality, subtitles, etc.)
   - Start the conversion process
   - Monitor conversion progress

## Example Websites

### News Websites
- Hacker News: https://news.ycombinator.com/
- BBC News: https://www.bbc.com/news
- CNN: https://www.cnn.com/

### Product Websites
- Books to Scrape: https://books.toscrape.com/
- Amazon: https://www.amazon.com/ (may require additional configuration)
- eBay: https://www.ebay.com/ (may require additional configuration)

## Notes

- The application uses both specific selectors for example websites and generic CSS selectors for other websites
- The scraper is optimized for Hacker News (news.ycombinator.com) and Books to Scrape (books.toscrape.com)
- For other websites, the application attempts to use generic selectors and fallback mechanisms
- Some websites may block web scraping attempts
- Always respect the website's robots.txt file and terms of service
- For more complex websites, you may need to customize the scraper.py file
- The application suppresses a PyQt6 deprecation warning related to "sipPyTypeDict()" which is an internal PyQt6 issue
- PyQt6 version 6.5.3 is specifically required to avoid compatibility issues with Qt libraries

## Customizing Selectors

If you want to scrape a website that isn't working with the default selectors, you can customize the selectors in the `scraper.py` file:

1. For news websites, modify the `extract_news_data` method
2. For product websites, modify the `extract_product_data` method

You can add specific selectors for a website by adding a condition like:

```python
if "example.com" in self.url:
    # Custom selectors for example.com
    articles = soup.select('your-custom-selector')
    # ...
```

Use browser developer tools (F12) to inspect the HTML structure of the website and identify the appropriate CSS selectors.

## Project Structure

- `main.py`: The main application with a tabbed GUI for web scraping and video conversion
- `scraper.py`: The web scraping module with functionality to fetch, extract, and save data
- `mkv_to_mp4_converter.py`: Core functionality for converting MKV video files to MP4 format
- `converter_gui.py`: PyQt6-based GUI for the MKV to MP4 converter
- `test_gui.py`: Test script for the GUI application
- `requirements.txt`: List of Python dependencies required for the applications

# MKV to MP4 Converter

A Python script that converts MKV video files to MP4 format using FFmpeg.

## Features

- Convert MKV files to MP4 format
- Preserve video and audio quality with passthrough options
- Handle subtitles (copy, burn into video, or remove)
- Maintain chapter information
- Configure video and audio codecs
- Adjust video quality settings

## Requirements

- Python 3.6 or higher
- FFmpeg (external dependency, not a Python package)

## Installation

1. Ensure FFmpeg is installed on your system:
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) or install via [Chocolatey](https://chocolatey.org/): `choco install ffmpeg`
   - **macOS**: Install via [Homebrew](https://brew.sh/): `brew install ffmpeg`
   - **Linux**: Use your distribution's package manager, e.g., `apt install ffmpeg` (Ubuntu/Debian) or `dnf install ffmpeg` (Fedora)

2. Verify FFmpeg installation by running: `ffmpeg -version`

## Usage

### GUI Usage

The MKV to MP4 converter can be accessed through the main application's GUI:

1. Run the main application:
   ```bash
   python main.py
   ```

2. Select the "MKV to MP4 Converter" tab
3. Click "Open MKV to MP4 Converter" to launch the converter window
4. In the converter window:
   - Click "Select MKV File" to choose an input file
   - Optionally click "Select Output File" to specify where to save the converted file
   - Configure conversion options:
     - Video Codec: copy (fastest), libx264 (H.264), or libx265 (H.265/HEVC)
     - Audio Codec: copy (original), aac, or mp3
     - Subtitle Mode: copy, burn into video, or none
     - Quality (CRF): 0-51 (lower is better quality, 18-28 is a good range)
     - Encoding Preset: ultrafast to veryslow (affects compression efficiency)
     - Chapter information: keep or discard
   - Click "Convert" to start the conversion process
   - Monitor the progress in the status area

### Command-line Usage

#### Basic Usage

Convert an MKV file to MP4 with default settings (preserving original quality):

```bash
python mkv_to_mp4_converter.py input.mkv
```

This will create `input.mp4` in the same directory.

#### Advanced Options

```bash
python mkv_to_mp4_converter.py input.mkv -o output.mp4 --video-codec libx264 --audio-codec aac --subtitle-mode copy --crf 23 --preset medium
```

### Command-line Arguments

- `input_file`: Path to the input MKV file (required)
- `-o, --output`: Path to the output MP4 file (default: input_file with .mp4 extension)
- `--video-codec`: Video codec to use (`copy`, `libx264`, `libx265`) (default: `copy`)
- `--audio-codec`: Audio codec to use (`copy`, `aac`, `mp3`) (default: `copy`)
- `--subtitle-mode`: How to handle subtitles (`copy`, `burn`, `none`) (default: `copy`)
- `--crf`: Constant Rate Factor for video quality (default: 23, lower is better)
- `--preset`: Encoding preset (`ultrafast` to `veryslow`) (default: `medium`)
- `--no-chapters`: Do not copy chapter information
- `-v, --verbose`: Print detailed output

### Examples

1. Simple conversion with default settings:
   ```bash
   python mkv_to_mp4_converter.py movie.mkv
   ```

2. Specify output file:
   ```bash
   python mkv_to_mp4_converter.py movie.mkv -o converted_movie.mp4
   ```

3. Re-encode video with H.264 and AAC audio:
   ```bash
   python mkv_to_mp4_converter.py movie.mkv --video-codec libx264 --audio-codec aac
   ```

4. Burn subtitles into the video:
   ```bash
   python mkv_to_mp4_converter.py movie.mkv --subtitle-mode burn
   ```

5. High-quality conversion with slow preset:
   ```bash
   python mkv_to_mp4_converter.py movie.mkv --video-codec libx264 --crf 18 --preset slow
   ```

## Notes

- Using `copy` for video and audio codecs is faster and preserves original quality
- Re-encoding allows for better compatibility but takes longer and may reduce quality
- The `crf` value controls quality (lower = better quality, higher = smaller file)
- The `preset` value affects encoding speed (faster presets = larger files)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
