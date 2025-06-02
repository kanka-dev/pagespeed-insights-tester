# PageSpeed Insights Bulk Testing Tool

This tool allows you to automatically test multiple URLs from a sitemap using Google's PageSpeed Insights API and save the results to a CSV file.

## Features

- Automatically fetches all URLs from a sitemap (including sitemap index files)
- Tests each URL with Google PageSpeed Insights
- Collects performance metrics:
  - Performance Score
  - Accessibility Score
  - Best Practices Score
  - SEO Score
- Saves results to a CSV file for easy analysis

## Prerequisites

- Python 3.x
- Google PageSpeed Insights API key ([Get it here](https://developers.google.com/speed/docs/insights/v5/get-started))

## Installation

1. Clone this repository:
`bash git clone [https://github.com/yourusername/pagespeed-bulk-testing.git](https://github.com/yourusername/pagespeed-bulk-testing.git) cd pagespeed-bulk-testing`

2. Install the required dependencies:
`bash pip install requests python-dotenv`

3. Create a `.env` file in the project root with your API key and sitemap URL:
`PAGESPEED_API_KEY=your_api_key_here SITEMAP_URL=[https://example.com/sitemap.xml](https://example.com/sitemap.xml)`

## Usage

Simply run the script:
`bash python pagespeed_test.py`

The script will:
1. Load all URLs from the specified sitemap
2. Test each URL with PageSpeed Insights
3. Save the results to `pagespeed_report.csv`

## Output Format

The generated CSV file contains the following columns:
- `url`: The tested URL
- `performance`: Performance score (0-100)
- `accessibility`: Accessibility score (0-100)
- `best_practices`: Best Practices score (0-100)
- `seo`: SEO score (0-100)

## Rate Limiting

The script includes a 1.2-second delay between requests to avoid hitting API rate limits. Adjust the `time.sleep()` value in the main function if needed.

## Error Handling

- If a URL cannot be tested, it will still appear in the CSV with `None` values for scores
- Error messages will be displayed in the console during execution
- The script will continue running even if individual tests fail

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

[MIT License](LICENSE)