# ReflectedBlackhatSEO-Cybercrime

This `time_machine.py` script utilizes playwright to do webpage rendering through headless browsers. 

## Setup

Install playwright and headless browsers by following [the up-to-date instructions on Playwright official website](https://playwright.dev/python/docs/intro)
Key commands to run are listed below:

```
pip install pytest-playwright

playwright install
```

## Usage

### Help

```bash
# python time_machine.py  -h

2022-11-15 13:44:10,770 INFO inited
usage: Time machine [-h] [--is_domain] [--enable_multi_screen] [--multi_screen_limit MULTI_SCREEN_LIMIT] domain_file provider result_dir

positional arguments:
  domain_file
  provider
  result_dir

optional arguments:
  -h, --help            show this help message and exit
  --is_domain, -id      Given if the first arg is a domain
  --enable_multi_screen, -ems
  --multi_screen_limit MULTI_SCREEN_LIMIT, -msl MULTI_SCREEN_LIMIT
```

To screenshot the landing page of a bunch of domains and save the results in RESULT_DIR, store them in a file DOMAIN_File with each domain one line, specify a task tag TASK_TAG,  Then, run the following command:

```bash
python time_machine.py DOMAIN_File TASK_TAG RESULT_DIR
```

To screenshot a single domain DOMAIN_NAME, run the tool as below:

```bash
python time_machine.py DOMAIN_NAME -id TASK_TAG RESULT_DIR
```



### Output

The running status can be found in `result_stats_{TASK_TAG}.json` in RESULT_DIR, each line records the running result of one url, and it is formatted as follows:

`{"domain": ..., "is_success": ..., "err_message": ..., "result_basedir": ..., "provider": ..., "has_hops": ..., "hops": ...}`

The `is_success` field records whether the url page was successfully crawled. 

If one url fails to be crawled due to an exception in the process, the reason for the error can be found in the `err_message` field.

If one url succeeds to be crawled, in the RESULT_DIR/`provider`/`result_basedir` folder, you can find the `page_screenshot.png` which is the screenshot of landing page, the `test.har` file which logs a web browser’s interaction with a site, and the `hops.txt` which records the whole redirection path.
