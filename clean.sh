rm -rf ./migrations
rm -f db.sqlite3

aerich init -t aerich_config.TORTOISE_ORM
aerich init-db
poetry run python server.py create-superuser --fullname String --username string --email user@user.com --password string