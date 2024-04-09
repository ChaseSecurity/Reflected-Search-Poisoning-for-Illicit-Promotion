# Telegram Account Infiltrator

This `time_machine_telegram.py` script utilizes [Telethon](https://github.com/LonamiWebs/Telethon) to do Telegram account crawling.

## Usage

Telethon is a Python library, which means you need to download and install Python from https://www.python.org/downloads/ if you haven’t already. Once you have Python installed, upgrade pip and run:

```
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade telethon
```

...to install or upgrade the library to the latest version.

Before working with Telegram’s API, **you need to get your own API ID and hash, and fill them into the code.**

> 1. Login to your Telegram account with the phone number of the developer account to use.
> 2. Click under API Development tools.
> 3. A Create new application window will appear. Fill in your application details. There is no need to enter any URL, and only the first two fields (App title and Short name) can currently be changed later.
> 4. Click on Create application at the end. Remember that your API hash is secret and Telegram won’t let you revoke it. Don’t post it anywhere!



To crawl related information based on a bunch of Telegram contacts and save the results in RESULT_DIR, you can store them in a file CONTACT_File with each contact one line, specify a task tag TASK_TAG. Then, run the following command:

```bash
python time_machine_telegram.py CONTACT_File TASK_TAG RESULT_DIR
```

To crawl a single contact CONTACT_NAME, run the tool as below:

```bash
python time_machine_telegram.py CONTACT_NAME -iu TASK_TAG RESULT_DIR
```

If you are the first time to run this program, you will be asked to enter your Telegram account and a verification code to log in, then the `.session` file will be generated.

## Output

The running status can be found in `result_stats_{TASK_TAG}.json` in RESULT_DIR, each line records the running result of one contact, and it is formatted as follows:

`{"username":..., "is_success":..., "is_fuzzy":..., "err_message":..., "provider":...}`

The `is_success` field indicates whether contact was successfully crawled. 

The `is_fuzzy` field indicates whether the crawling result of the contact is the result of a fuzzy search. When the exact search for contact does not match the corresponding account, the fuzzy search strategy is adopted and the crawling results are stored in a subfolder.

If one contact fails to be crawled due to an exception in the process, the reason for the error can be found in the `err_message` field.

If one contact succeeds to be crawled, in the RESULT_DIR/`provider`/`username` folder, you can find the crawling result described below for the different account types:

### User

`info.json` and the profile_photos (if any)

```json
{
  "username": "ak5537",
  "type": "user",
  "first_name": "谷歌seo@杨,认准飞机号,其余骗子",
  "last_name": null,
  "about": "博彩，网赚，股票，trx挖矿理财，各个国家语言定做谷歌SEO优化！进频道看优化案例：https://t.me/ak55378"
}
```

### Bot

`info.json` and the profile_photos (if any)

```json
{
  "username": "bailufakabot",
  "type": "bot",
  "first_name": "白鹿平台【官方认证】24小时人工客服【非机器人】有事直接滴滴",
  "last_name": null,
  "about": null
}
```

### Channel

`info.json` and profile_photos (if any)
```json
{
  "username": "bailufaka",
  "type": "channel",
  "title": "国内外账号批发 🅥【仅此一个频道，请勿上当】",
  "about": "先少量购买测试，需要大量批发联系24小时人工客服  祝各位老板发大财",
  "subscribers": 13287
}
```

`messages.json` which records the message history of the last 3 days and the images sent in the messages (if any)
```json
{"datetime": "2022-12-14 07:11:53+00:00", "message": "【白鹿联盟】\nTG最大最全 【国内外账号批发刷粉联盟】\n国内APP账号🔥🔥🔥🔥🔥🔥🔥🔥🔥\n\n👑微信账号\n👑微信企业号\n👑微信公众号\n👑QQ账号\n👑支付宝账号\n👑陌陌账号\n👑抖音账号\n👑快手账号\n👑小红书账号\n👑知乎账号\n👑头条账号\n👑百合网账号\n👑世纪佳缘账号\n👑soul灵魂账号\n👑探探账号\n👑他趣账号\n👑钉钉实名账号\n👑百度贴吧账号\n👑微博账号\n👑蝙蝠账号\n👑趣约会账号\n👑积目账号\n👑花田账号\n👑伊对账号\n👑珍爱网账号\n👑京东账号\n👑闲鱼账号\n👑淘宝\n👑陌陌\n👑搜狐\n👑58同城\n👑拼多多\n👑阿里云实名账户\n👑腾讯云实名账户\n👑华为云实名账户\n👑天翼云实名账户\n\n\n\n海外账号组👤👤👤👤👤👤👤👤👤👤\n\n👑WhatsApp号\n👑Facebook号\n👑友缘号\n👑instagram号\n👑twitter号\n👑telegram电报小号 协议号\n👑Linkedin 领英号\n👑Discord不和谐号\n👑YouTube油管号\n👑TikTok号\n👑谷歌GV号\n👑谷歌邮箱Gmail账户\n👑火种账号 蓝V定制\n👑Wechat海外微信\n👑Facebook商城号\n👑vpn订阅节点\n👑海外苹果ID\n👑礼品卡卷\n👑三网实名手机卡\n👑海外邮箱\n\n\n💥💥💥💥💥💥💥💥💥💥\n全球国家APP 实卡虚拟卡 接码注册\n👑短信接码\n👑APP手机号注册\n\n🙀🙀TG刷粉低至1元1000粉🙀🙀🙀🙀\n\nTG、ins、TikTok、领英、\n推特、脸书、油管、\n刷粉、刷浏览、刷关注、刷评论👍🏻\nTG一手稳定新老号批发，信誉质量第一。", "media": {"type": "<class 'telethon.tl.types.MessageMediaPhoto'>"}}
{"datetime": "2022-12-14 07:12:31+00:00", "message": "购买须知：如需批量购买请先拿个测试，无问题再继续拿，售出后非售后问题无退无换", "media": {"type": "<class 'NoneType'>"}}
```


### Group

`info.json` and profile_photos (if any)
```json
{
  "username": "DataFBI",
  "type": "group",
  "title": "FBI.IO数据讨论群",
  "about": "【FBI数据，各大网站用户数据免费领取，助力增长！支持验证！】\n     🚀 核心通过LSP技术精准读取置顶目标近期全站活跃数据🚀拿到最真实热数据！\n          🔥  最强短信通道，三网通，0.1/条 ☎️\n官网：FBI.IO🚀\nTelegram: @FBICN1",
  "members": 332,
  "online": 6
}
```

`members.json`
```json
{"id": 963413476, "username": "Shanks10086", "first_name": "shanks-国际短信", "last_name": null, "is_bot": false}
{"id": 1540256136, "username": "hxl955", "first_name": "信用盘改单", "last_name": null, "is_bot": false}
{"id": 729551272, "username": "aniuniu88", "first_name": "萌", "last_name": "NIU 《转账需语音确认》", "is_bot": false}
{"id": 5633778229, "username": "TrustCha600", "first_name": "Telegram 专业调查机构", "last_name": null, "is_bot": false}
{"id": 5578399214, "username": null, "first_name": "海外", "last_name": "专业引流各种粉", "is_bot": false}
```

`messages.json` which records the message history of the last 3 days and the images sent in the messages (if any)
```json
{"datetime": "2023-01-10 08:58:27+00:00", "message": "泡泡数据谁会抓啊", "media": {"type": "<class 'NoneType'>"}}
{"datetime": "2023-01-10 08:58:33+00:00", "message": "", "media": {"type": "<class 'telethon.tl.types.MessageMediaDocument'>", "mime_type": "image/webp"}}
{"datetime": "2023-01-12 12:55:07+00:00", "message": "【博度认证商家】&放心购\nOK数码(手机专卖店)\n手机/平板/笔记本/苹果/华为/安卓 \n全线产品  正品全新  原封未激活\n   (马尼拉片区)\n（甲米地岛内可送）\n   (克拉克可送)\n\n以上地区当日下单当日送到\n\n产品报价@ok_shouji\n下单找我：@ok_ph 👈🏻\n微信下单➕ok_shouji 👈🏽.", "media": {"type": "<class 'telethon.tl.types.MessageMediaPhoto'>"}}
```