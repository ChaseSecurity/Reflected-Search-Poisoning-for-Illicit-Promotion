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

Help

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



[ Updates ]

The redirect path of each URL now can be found in `result_stats.json` in the RESULT_DIR and `hops.txt` in each DOMAIN_DIR

