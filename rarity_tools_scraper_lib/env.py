from pathlib import Path
import environ
import os


root = environ.Path(__file__) - 2

# Fetch env vars
os.environ.setdefault("ENV_FILE", root(".env"))
env = environ.Env(DEBUG=(bool, False))
if os.path.isfile(os.environ["ENV_FILE"]):
    env.read_env(os.environ["ENV_FILE"])
