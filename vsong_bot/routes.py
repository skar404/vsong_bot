from vsong_bot.views import ping


def setup_routes(app):
    app.router.add_get('/', ping, name='ping')
