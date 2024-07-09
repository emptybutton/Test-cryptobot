import typenv


_env = typenv.Env()


class Env:
    telegram_bot_token = _env.str("TELEGRAM_BOT_TOKEN")
    coinmarketcap_token = _env.str("COINMARKETCAP_TOKEN")

    redis_host = _env.str("REDIS_HOST")
    redis_port = _env.int("REDIS_PORT")

    postgres_database = _env.str("POSTGRES_DATABASE")
    postgres_username = _env.str("POSTGRES_USER")
    postgres_password = _env.str("POSTGRES_PASSWORD")
    postgres_host = _env.str("POSTGRES_HOST")
    postgres_port = _env.int("POSTGRES_PORT")
    postgres_echo = _env.bool("POSTGRES_ECHO")
