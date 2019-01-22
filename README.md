# vsong bot 
[![Build Status](https://cloud.drone.io/api/badges/skar404/vsong_bot/status.svg)](https://cloud.drone.io/skar404/vsong_bot)

run app:
```bash
pip install -r requirements.txt
python manage.py web
```
---

Contributing:

```bash
// run: postgres, rabbitmq
docker-compose -f docker-compose.dev.yml

// run https proxy -> localhost:8000
ngrok http 8000

// create env file
echo '
BOT_TOKEN=000000000:AAAAAAA_AAAA_AAAAAAAAAAAAAAAA_AAAAAA
BOT_WEB_HOOK=https://000000.ngrok.io/bot/{secret_url} 

VK_APP_ID=00000
VK_LOGIN=
VK_PASSWORD=

# vk proxy
PROXY_IP=
PROXY_USER=
PROXY_PASSWORD=
PROXY_PORT=

# S3 settings
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_END_POINT_URL=
AWS_REGION_NAME=
' > .env

// run bot app
pip install -r requirements.txt
python manage.py web
```

---

src telegram bot: [@vsong_bot](https://telegram.me/vsong_bot)