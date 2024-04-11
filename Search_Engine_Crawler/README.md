# Search Engine Crawler

## Methodology

Two search strategies applied:

- Query with keywords extracted from known IPTs. (Google, Bing, Baidu, Sogou)

- Query with URL reflection schemes which have been abused. (only Google supports)

## Usage

For each crawling round

- run `FromContact_parallel_$all_SEs.py` and `FromSite_parallel_Google.py` to get crawling results

    ```shell
    $ python FromContact_parallel_$SE.py -h
    usage: FromContact_parallel_Baidu.py [-h] --seed_path SEED_PATH --result_dir RESULT_DIR [--model_dir MODEL_DIR]
    
    options:
    -h, --help          show this help message and exit
    --seed_path SEED_PATH
                        The crawling seed filepath
    --result_dir RESULT_DIR
                        The crawling results directory
    --model_dir MODEL_DIR
                        The binary_IPT_classifier directory
    ```

- run `get_keywords.py` and `get_links.py` to get crawling seeds for next round

    ```shell
    $ python get_keywords.py -h
    usage: get_keywords.py [-h] --output OUTPUT --result_dir RESULT_DIR [--model_dir MODEL_DIR]
    
    options:
    -h, --help          show this help message and exit
    --output OUTPUT     The keywords extracted output file
    --result_dir RESULT_DIR
                        The obtained crawling results directory
    --model_dir MODEL_DIR
                        The IPT_keyword_extractor directory


    $ python get_links.py -h
    usage: get_links.py [-h] --output OUTPUT --result_dir RESULT_DIR

    options:
    -h, --help          show this help message and exit
    --output OUTPUT     The links extracted output file
    --result_dir RESULT_DIR
                        The obtained crawling results directory
    ```