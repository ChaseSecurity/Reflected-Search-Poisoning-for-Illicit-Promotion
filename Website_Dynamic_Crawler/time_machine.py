import asyncio
import argparse
from asyncio import coroutines
import json
import logging
import os
import playwright
from playwright.async_api import async_playwright
import traceback
import time
import typing
import requests
import re

def search_the_next_hop(
    current_page: dict
) -> typing.Tuple[bool, str]:
    if current_page != {}:
        # server redirect
        status_code = current_page["response"]["status"]
        if 300 <= status_code < 400:
            nextUrl = current_page["response"]["redirectURL"]
            return [True, nextUrl]
        # meta redirect
        metas = re.findall(r'<meta.*?>', str(current_page["response"]["content"]))
        for meta in metas:
            if 'refresh' in str(meta):
                pattern = re.compile(r'(?<=url=).*(?=")', re.I)
                result = re.findall(pattern, str(meta))
                if result == []:
                    return [False, ""]
                nextUrl = re.findall(pattern, str(meta))[0]
                if not re.match(r'(?:http|https)://', nextUrl):
                    nextUrl = current_page["request"]["url"] + nextUrl
                return [True, nextUrl]
        # js redirect
        scripts = re.findall(r'<script.*?</script>', str(current_page["response"]["content"]))
        for script in scripts:
            pattern = re.compile(r'(?<=location.href=").*?(?=")|(?<=location=").*?(?=")|(?<=location.replace\(").*?(?="\))|(?<=location.assign\(").*?(?="\))', re.I)
            result = re.findall(pattern, str(script).replace(' ', '').replace('\'', '"'))
            if result != []:
                nextUrl = result[0]
                # print(nextUrl)
                return [True, nextUrl]
    # no hop
    return [False, ""]

def get_next_hops(
        har_file_path: str
) -> typing.Tuple[bool, str]:
    with open(har_file_path, encoding='utf-8') as fr:
        har_file = json.load(fr)
        
        entries = har_file["log"]["entries"]
        urls = []

        current_page = entries[0]
        urls.append(current_page["request"]["url"])
        # jump to the page
        [result, nextUrl] = search_the_next_hop(current_page)
        index = 0
        while result == True:
            current_page = {}
            for i in range(index + 1, len(entries)):
                entry = entries[i]
                if entry["request"]["url"] == nextUrl:
                    current_page = entry
                    urls.append(nextUrl)
                    index = i
                    break
            [result, nextUrl] = search_the_next_hop(current_page)

        with open(os.path.join(os.path.dirname(har_file_path), "hops.txt"), "w") as fw:
            for url in urls:
                fw.write(url+'\n')      

    urls.pop(0)
    if len(urls) == 0:
        return [False, ""]
    else:
        return [True, ",".join(urls)]


class WebTimeMachine:
    def __init__(self):
        pass
   
    async def get_page_screenshot(
            self,
            url: str,
            is_full_page: bool = False,
    ) -> bytes:
        """
        Get the visual screenshot of a webpage
        @params
            url: str : the url to crawl
            is_full_page: bool : whether to screenshot the whole webpage,
            or the component in the current visual window
        @return
            the screenshot in bytes
        """
        async with async_playwright() as p:
            # choose firefox since chrominum was found frozen when closing the context
            # for some webpages.
            browser = await p.firefox.launch()
            context = await browser.new_context()
            page = await context.new_page()
            try:
                resp = await page.goto(url)
                screenshot = await page.screenshot(full_page=is_full_page)
                # Wait at most 10 seconds when closing the context
                asyncio.wait_for(context.close(), timeout=10)
                await browser.close()
                return screenshot
            except Exception as e:
                logging.warning(
                    "Got exception %s: %s when visiting page %s",
                    type(e),
                    e,
                    url,
                )
                return None

    async def screen_page(
            self,
            url: str,
            result_dir: str,
            enable: bool=False,
            limit: int=10,
            timeout_in_millisec: int=10000,
    ) -> typing.Tuple[bool, str]:
        """
        @return [is_success, message]
        """
        async with async_playwright() as p:
            browser = await p.firefox.launch()
            result = await self._single_page(
                url,
                result_dir,
                browser,
                timeout_in_millisec=timeout_in_millisec,
            )

            if enable:
                subSet = await retrieve_subDomain(url, browser, limit)

                logging.info(url + ' have ' + str(len(subSet)) + ' subPage')
                

                for item in iter(subSet):

                    subPath = os.path.join(result_dir, retrieve_url(item))

                    if not os.path.exists(subPath):
                        os.makedirs(subPath)
                    await self._single_page(
                        item,
                        subPath,
                        browser,
                        timeout_in_millisec=timeout_in_millisec,
                    )

            await browser.close()
            return result

    async def _single_page(
            self,
            url: str,
            result_dir: str,
            browser: playwright.async_api.Browser,
            timeout_in_millisec: int=10000,
    ) -> typing.Tuple[bool, str]:
        e_message = ""
        for retry_times in range(3):
            timeout_in_millisec += 10000
            logging.info(f"Start to screen URL {url}, Try #{retry_times+1}")
            try:
                context = await browser.new_context(
                    ignore_https_errors=True,
                    record_har_path=os.path.join(result_dir, "test.har"),
                    # uncomment if the redendering video is needed
                    # record_video_dir=result_dir,
                )

                context.set_default_timeout(timeout_in_millisec)
                page = await context.new_page()

                resp = await page.goto(
                    url,
                    timeout=timeout_in_millisec,
                    # wait_until='networkidle',
                )

                await page.wait_for_timeout(5000)

                screenshot = await page.screenshot(path=os.path.join(result_dir, "page_screenshot.png"))

                # Wait at most 120 seconds when closing the context,
                #  since context closing could hang for an endless time
                await asyncio.wait_for(context.close(), timeout=120)

                return (True, "")
            except playwright._impl._api_types.TimeoutError as e:
                e_message = f"Got exception {type(e)}: {e} when visiting page {url}"
                continue
            except Exception as e:
                e_message = f"Got exception {type(e)}: {e} when visiting page {url}"
                break
        
        return (False, e_message)

    # TODO fix the issue of "page is closed" when sharing the same browser instance
    async def screen_multi_pages(
            self,
            urls: typing.List[str],
            result_base_dir: str,
            timeout_in_millisec: int=15000,
    ) -> typing.List[typing.Tuple[bool, str]]:
        """
        @return [is_success, message]
        """
        results = []
        async with async_playwright() as p:
            browser = await p.firefox.launch()
            coroutines = []
            for url in urls:
                result_dir = os.path.join(
                    result_base_dir, self.get_dir_basename_from_url(url))
                coroutines.append(self._single_page(
                    url,
                    result_dir,
                    browser,
                    timeout_in_millisec=timeout_in_millisec,
                ))
            results = await asyncio.gather(*coroutines, return_exceptions=True)
            await browser.close()
            return results

    def get_dir_basename_from_url(self, url: str) -> str:
        return url.replace("://", "_").replace("/", "_").replace(":", "_")

    async def screen_page_in_batch(
            self,
            urls: typing.List[str],
            result_dir: str,
            enable: bool=False,
            limit: int=10,
            batch_size: int = 50,
    ) -> typing.List[typing.Tuple[bool, str]]:
        results = []
        batch_progress = 0
        while batch_progress < len(urls):
            routines = []
            batch_urls = urls[batch_progress: batch_progress + batch_size]
            
            for url in batch_urls:
                routines.append(
                    self.screen_page(
                        url=url,
                        result_dir=os.path.join(
                            result_dir, self.get_dir_basename_from_url(url)),
                        enable=enable,
                        limit=limit,
                    )
                )

            raw_batch_results = await asyncio.gather(*routines, return_exceptions=True)

            batch_results = []
            for url, result in zip(batch_urls, raw_batch_results):
                if type(result) is tuple:
                    batch_results.append(result)
                else:
                    msg = f"Got an exception {result} for url {url}"
                    logging.warning(msg)
                    batch_results.append((False, msg))
            results.extend(batch_results)                    

            logging.info(
                "Finish a sub-batch with %d successes, and %d failures",
                sum(1 for item in batch_results if item[0] == True),
                sum(1 for item in batch_results if item[0] == False),
            )
            batch_progress += batch_size
        logging.info(
            "Finish a batch with %d successes, and %d failures",
            sum(1 for item in results if item[0] == True),
            sum(1 for item in results if item[0] == False),
        )
        return results


async def screen_webpages(
        domains: str,
        result_dir: str,
        provider: str,
        enable: bool=False,
        limit: int=10,
        batch_size: int = 100,
):
    start_time = time.time()
    result_stat_file = os.path.join(result_dir, "result_stats.json")
    sub_result_dir = os.path.join(result_dir, provider)
    if not os.path.exists(sub_result_dir):
        os.makedirs(sub_result_dir)
    # load finished domains
    domains_done = set()
    if os.path.exists(result_stat_file):
        with open(result_stat_file, "r") as fd:
            for line in fd:
                item = json.loads(line)
                domains_done.add(item["domain"])
    domains_to_screen = list(set(domains) - domains_done)
    logging.info(
        f"Among {len(domains)} domains,"
        f" {len(domains_to_screen)} are left for screening"
    )
    time_machine = WebTimeMachine()
    overall_results = []
    with open(result_stat_file, "a") as fd:
        round_index = 0
        while round_index < len(domains_to_screen):
            batch_domains_to_screen = domains_to_screen[round_index:round_index + batch_size]
            round_index += batch_size

            screen_results = await time_machine.screen_page_in_batch(
                urls=[
                    f"http://{domain}"
                    for domain in batch_domains_to_screen
                ],
                result_dir=sub_result_dir,
                enable=enable,
                limit=limit,
            )
            overall_results.extend(screen_results)
            for domain, result in zip(batch_domains_to_screen, screen_results):
                [has_hops, hops] = [False, ""]
                if result[0] == True:
                    logging.info(f"Start to get hops from {domain}")
                    [has_hops, hops] = get_next_hops(os.path.join(sub_result_dir, f"http_{domain}", "test.har"))
                fd.write(json.dumps({
                    "domain": domain,
                    "is_success": result[0],
                    "err_message": result[1],
                    "result_basedir": f"http_{domain}",
                    "provider": provider,
                    "has_hops": has_hops,
                    "hops": hops,
                }) + "\n")
            fd.flush()

            screen_results = await time_machine.screen_page_in_batch(
                urls=[
                    f"https://{domain}"
                    for domain in batch_domains_to_screen
                ],
                result_dir=sub_result_dir,
                enable=enable,
                limit=limit,
            )
            overall_results.extend(screen_results)
            for domain, result in zip(batch_domains_to_screen, screen_results):
                [has_hops, hops] = [False, ""]
                if result[0] == True:
                    logging.info(f"Start to get hops from {domain}")
                    [has_hops, hops] = get_next_hops(os.path.join(sub_result_dir, f"https_{domain}", "test.har"))
                fd.write(json.dumps({
                    "domain": domain,
                    "is_success": result[0],
                    "err_message": result[1],
                    "result_basedir": f"https_{domain}",
                    "provider": provider,
                    "has_hops": has_hops,
                    "hops": hops
                }) + "\n")
            fd.flush()
            logging.info(
                "Ongoing screening %s with %d successes, and %d failures",
                provider,
                sum(1 for item in overall_results if item[0] == True),
                sum(1 for item in overall_results if item[0] == False),
            )

    logging.info(
        "Done screening %s with %d successes, and %d failures",
        provider,
        sum(1 for item in overall_results if item[0] == True),
        sum(1 for item in overall_results if item[0] == False),
    )
    end_time = time.time()
    logging.info(
        "Done screening %s with time cost of %d seconds",
        provider,
        time.time() - start_time,
    )


async def retrieve_subDomain(url: str, browser: str, limit: int, timeout_in_millisec: int = 20000):
    async with async_playwright() as p:

        context = await browser.new_context()
        page = await context.new_page()

        context.set_default_timeout(timeout_in_millisec)

        await page.goto(
            url,
            timeout=timeout_in_millisec,
            # wait_until='networkidle',
        )

        href = await page.evaluate('() => { return Array.from(document.links).map(item => item.href)}')

        hrefSet = set(href)

        resultSet = set()

        for item in iter(hrefSet):
            if limit == 0:
                break
            if 'https' in item or 'http' in item:
                resultSet.add(item)
                limit -= 1

        return resultSet


def retrieve_url(url):
    if url.find("?") != -1:
        url = url[0: url.find("?")]
    return url.replace("://", "_").replace("/", "_").replace(":", "_")

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    logging.info("inited")
    parser = argparse.ArgumentParser("Time machine")
    parser.add_argument("domain_file", type=str)
    parser.add_argument("provider", type=str)
    parser.add_argument("result_dir", type=str)
    parser.add_argument("--is_domain", "-id", action="store_true", help="Given if the first arg is a domain")
    parser.add_argument("--enable_multi_screen", "-ems", action="store_true")
    parser.add_argument("--multi_screen_limit", "-msl", type=int, default=10)
    options = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    if not options.is_domain:
        domains = open(options.domain_file, "r").read().splitlines()
    else:
        domains = [options.domain_file]
    asyncio.run(
        screen_webpages(
            domains,
            options.result_dir,
            options.provider,
            enable=options.enable_multi_screen,
            limit=options.multi_screen_limit,
            batch_size=10
        )
    )
