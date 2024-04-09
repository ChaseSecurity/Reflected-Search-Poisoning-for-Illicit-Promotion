# Search Engine Crawler

## Methodology

Two search strategies applied:

- Query with keywords extracted from known IPTs. (Google, Bing, Baidu, Sogou)

- Query with URL reflection schemes which have been abused. (only Google supports)

## Usage

For each crawling round

- run `FromContact_parallel_$all_SEs$.py` and `FromSite_parallel_Google.py` to get crawling results

- run `get_keywords.py` and `get_links.py` to get crawling seeds for next round