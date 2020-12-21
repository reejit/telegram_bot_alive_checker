### telegram bot alive checker

this is simple web server that allow you to check that your bot is alive

script send /ping command to bot and check that answer is pong after response with 200 if all ok otherwise 400

environment variable:
- API_ID
- API_HASH
- TELEPHONE - telephone number for account that create api_id/api_hash

web server start on 8088

the body is always `ok`