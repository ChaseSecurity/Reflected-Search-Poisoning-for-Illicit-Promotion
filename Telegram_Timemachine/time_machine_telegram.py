import argparse
import asyncio
import typing
from telethon import TelegramClient
from telethon import functions, types, errors
import logging
import os
import json
import time
import datetime


class TelegramTimeMachine:
    # get from 'https://my.telegram.org'
    api_id = 19367738
    api_hash = '145e319508dba03a5f5a7a903fd667c5'
    
    client = TelegramClient('anon', api_id, api_hash)
    today = datetime.date.today()

    def __init__(self):
        pass

    async def get_account_type(
        self,
        username: str
    ):
        try:
            time.sleep(10)
            input_entity = await self.client.get_input_entity(username)
            entity = await self.client.get_entity(input_entity)
            if isinstance(input_entity, types.InputPeerUser):
                if entity.bot == False:
                    return ['user', entity]
                else:
                    return ['bot', entity]
            elif isinstance(input_entity, types.InputPeerChannel):
                if entity.megagroup == False:
                    return ['channel', entity]
                else:
                    return ['group', entity]
        except errors.FloodWaitError as e:
            logging.info(f"Have to sleep {e.seconds}s")
            time.sleep(e.seconds)
            return ['', None]
        except Exception as e:
            # print(type(e), e)
            return ['invalid', None]
    

    async def get_fuzzy_search_results(
        self,
        username: str,
    ):
        usernames = []
        search_results = await self.client(functions.contacts.SearchRequest(username, limit=100))
        # print(search_results.stringify())
        for result in search_results.chats:
            usernames.append(result.username)
        for result in search_results.users:
            usernames.append(result.username)
        # print(len(usernames))
        return usernames


    async def get_user_info(
        self,
        entity,
        result_dir,
    ):  
        with open(os.path.join(result_dir, "info.json"), "w", encoding='utf-8', newline='\n') as fd:
            full_info = await self.client(functions.users.GetFullUserRequest(entity))
            fd.write(json.dumps({
                "username": full_info.users[0].username,
                "type": "user",
                "first_name": full_info.users[0].first_name,
                "last_name": full_info.users[0].last_name,
                "about": full_info.full_user.about,
            }, ensure_ascii=False, indent=2))
        
        photos = await self.client.get_profile_photos(entity)
        for photo in photos:
            await self.client.download_media(photo, result_dir)


    async def get_bot_info(
        self,
        entity,
        result_dir
    ):    
        with open(os.path.join(result_dir, "info.json"), "w", encoding='utf-8', newline='\n') as fd:
            full_info = await self.client(functions.users.GetFullUserRequest(entity))
            fd.write(json.dumps({
                "username": full_info.users[0].username,
                "type": "bot",
                "first_name": full_info.users[0].first_name,
                "last_name": full_info.users[0].last_name,
                "about": full_info.full_user.about,
            }, ensure_ascii=False, indent=2))
        
        photos = await self.client.get_profile_photos(entity)
        for photo in photos:
            await self.client.download_media(photo, result_dir)


    async def get_channel_info(
        self,
        entity,
        result_dir
    ):
        with open(os.path.join(result_dir, "info.json"), "w", encoding='utf-8', newline='\n') as fd:
            full_info = await self.client(functions.channels.GetFullChannelRequest(entity))
            for chat in full_info.chats:
                if chat.username == entity.username:
                        fd.write(json.dumps({
                            "username": chat.username,
                            "type": "channel",
                            "title": chat.title,
                            "about": full_info.full_chat.about,
                            "subscribers": full_info.full_chat.participants_count,
                        }, ensure_ascii=False, indent=2))

        with open(os.path.join(result_dir, "messages.json"), "w", encoding='utf-8', newline='\n') as fd:
            async for message in self.client.iter_messages(entity, reverse = True, offset_date=self.today-datetime.timedelta(days=1), wait_time=1):
                if message.date > datetime.datetime(self.today.year, self.today.month, self.today.day, 0, 0, 0, 0, tzinfo=datetime.timezone.utc):
                    break
                if isinstance(message, types.Message):
                    if isinstance(message.media, types.MessageMediaWebPage) and isinstance(message.media.webpage, types.WebPage):
                        fd.write(json.dumps({
                            "datetime": message.date,
                            "message": message.message,
                            "media": {
                                "type": type(message.media),
                                "url": message.media.webpage.url,
                                "webpage_type": message.media.webpage.type,
                                "site_name": message.media.webpage.site_name,
                                "title": message.media.webpage.title,
                                "description": message.media.webpage.description
                            }
                        }, ensure_ascii=False, default=str) + '\n')
                    elif isinstance(message.media, types.MessageMediaDocument):
                        fd.write(json.dumps({
                            "datetime": message.date,
                            "message": message.message,
                            "media": {
                                "type": type(message.media),
                                "mime_type": message.media.document.mime_type
                            }
                        }, ensure_ascii=False, default=str) + '\n')
                    else:
                        fd.write(json.dumps({
                            "datetime": message.date,
                            "message": message.message,
                            "media": {
                                "type": type(message.media),
                            }
                        }, ensure_ascii=False, default=str) + '\n')
                        if isinstance(message.media, types.MessageMediaPhoto):
                            await client.download_media(message, result_dir)

        photos = await self.client.get_profile_photos(entity)
        for photo in photos:
            await self.client.download_media(photo, result_dir)


    async def get_group_info(
        self,
        entity,
        result_dir
    ):      
        with open(os.path.join(result_dir, "info.json"), "w", encoding='utf-8', newline='\n') as fd:
            full_info = await self.client(functions.channels.GetFullChannelRequest(entity))
            for chat in full_info.chats:
                if chat.username == entity.username:
                        fd.write(json.dumps({
                            "username": chat.username,
                            "type": "group",
                            "title": chat.title,
                            "about": full_info.full_chat.about,
                            "members": full_info.full_chat.participants_count,
                            "online": full_info.full_chat.online_count,
                        }, ensure_ascii=False, indent=2))
        
        with open(os.path.join(result_dir, "messages.json"), "w", encoding='utf-8', newline='\n') as fd:
            async for message in self.client.iter_messages(entity, reverse = True, offset_date=self.today-datetime.timedelta(days=3), wait_time=1):
                if message.date > datetime.datetime(self.today.year, self.today.month, self.today.day, 0, 0, 0, 0, tzinfo=datetime.timezone.utc):
                    break
                if isinstance(message, types.Message):
                    if isinstance(message.media, types.MessageMediaWebPage) and isinstance(message.media.webpage, types.WebPage):
                        fd.write(json.dumps({
                            "datetime": message.date,
                            "message": message.message,
                            "media": {
                                "type": type(message.media),
                                "url": message.media.webpage.url,
                                "webpage_type": message.media.webpage.type,
                                "site_name": message.media.webpage.site_name,
                                "title": message.media.webpage.title,
                                "description": message.media.webpage.description
                            }
                        }, ensure_ascii=False, default=str) + '\n')
                    elif isinstance(message.media, types.MessageMediaDocument):
                        fd.write(json.dumps({
                            "datetime": message.date,
                            "message": message.message,
                            "media": {
                                "type": type(message.media),
                                "mime_type": message.media.document.mime_type
                            }
                        }, ensure_ascii=False, default=str) + '\n')
                    else:
                        fd.write(json.dumps({
                            "datetime": message.date,
                            "message": message.message,
                            "media": {
                                "type": type(message.media),
                            }
                        }, ensure_ascii=False, default=str) + '\n')
                        if isinstance(message.media, types.MessageMediaPhoto):
                            await client.download_media(message, result_dir)

        with open(os.path.join(result_dir, "members.json"), "w", encoding='utf-8') as fd:
            members = await self.client.get_participants(entity)
            for member in members:
                fd.write(json.dumps({
                    "id": member.id,
                    "username": member.username,
                    "first_name": member.first_name,
                    "last_name": member.last_name,
                    "is_bot": member.bot,
                }, ensure_ascii=False) + '\n')

        photos = await self.client.get_profile_photos(entity)
        for photo in photos:
            await self.client.download_media(photo, result_dir)


    async def get_account_info(
        self,
        username: str,
        account_type: str,
        entity,
        result_dir: str,
    ):
        logging.info(f"[{account_type}] {username}")
        result_dir = os.path.join(result_dir, username)
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)
        
        if account_type == 'user':
            await self.get_user_info(entity, result_dir)
        elif account_type == 'bot':
            await self.get_bot_info(entity, result_dir)
        elif account_type == 'channel':
            await self.get_channel_info(entity, result_dir)
        elif account_type == 'group':
            await self.get_group_info(entity, result_dir)


    async def profile(
        self,
        username: str,
        result_dir: str,
    ) -> typing.Tuple[bool, bool, str]:
    # return [is_success, is_fuzzy, e_msg]
        try:
            logging.info(f"Start to profile {username}")
            account_type = ''
            while account_type == '':
                [account_type, entity] = await self.get_account_type(username)

            if account_type == 'invalid':
                fuzzy_results = await self.get_fuzzy_search_results(username)
                if fuzzy_results == []:
                    raise Exception("Not Found")
                for fuzzy_username in fuzzy_results:
                    [account_type, entity] = await self.get_account_type(fuzzy_username)
                    await self.get_account_info(fuzzy_username, account_type, entity, os.path.join(result_dir, username))
                return (True, True, "")
            else:
                await self.get_account_info(username, account_type, entity, result_dir)
                return (True, False, "")

        except Exception as e:
            e_message = f"Got exception {type(e)}: {e}"
            return (False, False, e_message)
            


async def profile_telegram(
    usernames: str,
    result_dir: str,
    provider: str,
):
    start_time = time.time()
    result_stat_file = os.path.join(result_dir, f"result_stats_{provider}.json")
    sub_result_dir = os.path.join(result_dir, provider)
    if not os.path.exists(sub_result_dir):
        os.makedirs(sub_result_dir)
    
    usernames_done = set()
    if os.path.exists(result_stat_file):
        with open(result_stat_file, "r") as fd:
            for line in fd:
                item = json.loads(line)
                usernames_done.add(item["username"])
    usernames_to_profile = list(set(usernames) - usernames_done)
    logging.info(
        f"Among {len(usernames)} usernames,"
        f"{len(usernames_to_profile)} are left for profiling"
    )

    # time_machine = TelegramTimeMachine()
    overall_results = []
    # async with time_machine.client:
    with open(result_stat_file, "a") as fd:
        for username in usernames_to_profile:
            profile_result = await time_machine.profile(
                username=username,
                result_dir=sub_result_dir
            )
            overall_results.append(profile_result)
            fd.write(json.dumps({
                "username": username,
                "is_success": profile_result[0],
                "is_fuzzy": profile_result[1],
                "err_message": profile_result[2],
                "provider": provider
            }) + '\n')
            fd.flush()
    
    logging.info(
        "Done screening %s with %d successes, and %d failures",
        provider,
        sum(1 for item in overall_results if item[0] == True),
        sum(1 for item in overall_results if item[0] == False),
    )
    end_time = time.time()
    logging.info(
        "Done profiling %s with time cost of %d seconds",
        provider,
        end_time - start_time,
    )
            

if __name__ == '__main__':
    logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)
    logging.getLogger('telethon').setLevel(logging.CRITICAL)
    logging.info("inited")
    parser = argparse.ArgumentParser("Time machine for Telegram")
    parser.add_argument("username_file", type=str)
    parser.add_argument("provider", type=str)
    parser.add_argument("result_dir", type=str)
    parser.add_argument("--is_username", "-iu", action="store_true", help="Given if the first arg is a username")
    options = parser.parse_args()

    usernames = []
    if not options.is_username:
        lines = open(options.username_file, "r").read().splitlines()
        for line in lines:
            usernames.append(line.replace('@', '').lower())
    else:
        usernames = [options.username_file]

    time_machine = TelegramTimeMachine()
    with time_machine.client as client:
        client.loop.run_until_complete(profile_telegram(
            usernames,
            options.result_dir,
            options.provider,
        ))
