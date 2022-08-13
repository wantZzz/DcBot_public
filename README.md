# DcBot_public

This program is used to deploy discord bots, it can:

> Stores information about each deleted message and displays its content, attachment picture, sender
 
> Generate emoticons and anime pictures in random

> check every urls in message aren't safely

> Join in voice channel give the correct time, translate word message to sound


What command in here?
---
* find
  * find near [Page]
    * Find recently deleted message data
  * find user @user
    * Find data from '@user' recently deleted messages today
  * find list_user @user [1~15]
    * Find 1~15 messages recently deleted by '@user' today
  * find edit
    * Find edit data for messages replied to by this command
  * find info
    * Find messages replied to by this command Delete data
* randomwaifu
  * randomwaifu list
    * View topic categories (automatically deleted after 15)
  * randomwaifu meme
    * generate the theme wife
  * randomwaifu favorites
    * View Favorites List
* randomeme
  * randomeme list [Page]
    * View meme categories
  * randomeme meme [Category number]
    * Generate memes of this category
* voice
  * voice_in/out
    * call the bot into the channel
  * onvoice/stopvoice
    * Switch robot voice message
  * listen_only
    * Join/leave member's voice receiving list
  * voice_nick [Chinese and English numerals with a limit of 8] (can't have emjio)
    * Nickname short name to be called when the bot is notified by voice messages
---
The following commands are available with administrator status：

* onrecord/stoprecord
  * Switch record function
* on_findEvent/stop_findEvent
  * Switch message query
* delete_event_mode [Mode code]
  * Delete message mode (all: all/ nopicture :no picture)
* voice_mode [Mode code]
  * Robot voice mode (all: all/ only: members in the list receive)
* ask_log [yyyymmdd]
  * Download system log
  
Before deploy this program......
---

There are steps you must complete to make sure your bot is running

### 1. Setting administrator

Open `users_datafile/state.json` , pasted your discord id in `administrator` and `Maintainer`

```
{"noise": true, 
 "administrator": [<pasted to here>], 
 "Maintainer": [<pasted to here>], 
 "voice": true, ......
```
### 2. Setting your discord bot token

There are three value you should prepare

| key | value |
|------|-------|
| dc_key | Discord bot token |
| credentials | Firebase admin sdk json fie content |
| virustotal_key | VirusTotal API key |

---

* If you are deploy on **Replit**
  1. Click the side bar and choise `Secrets`
  2. Fill in the key and value

* If you are deploy on **Heroku**
  1. Click `Settings` and find `Config Vars`
  2. Fill in the key and value
