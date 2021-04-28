import json


def get_db_credentials(config: str, test: bool = False) -> str:
    if test:
        return config
    with open(config) as file:
        config_file = json.load(file)

    username = config_file["username"]
    password = config_file["password"]
    dbname = config_file["dbname"]
    host = config_file["host"]

    res = "postgresql://%s:%s@%s/%s" % (username, password, host, dbname)
    return res


credentials = get_db_credentials("core/config.json")
