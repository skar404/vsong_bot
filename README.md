# vsong bot 
[![Build Status](https://cloud.drone.io/api/badges/skar404/vsong_bot/status.svg)](https://cloud.drone.io/skar404/vsong_bot)

run app:
```bash
pip install -r requirements.txt
python manage.py web
```
---

### Contributing:

 1. run postgres and rabbitmq:
```bash
docker-compose -f docker-compose.dev.yml
```

 2. run https proxy, ngrok.host -> localhost:8000:
```bash
ngrok http 8000
```

 3. create env file
```bash
echo '
BOT_TOKEN=000000000:AAAAAAA_AAAA_AAAAAAAAAAAAAAAA_AAAAAA

# need to leave '{secret_url}' for the function .format
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
```

 4. run postgres migration
```bash
alembic
 upgrade head
```

 5. run bot app: 
```bash
pip install -r requirements.txt
python manage.py web
```

---

src telegram bot: [@vsong_bot](https://telegram.me/vsong_bot)
