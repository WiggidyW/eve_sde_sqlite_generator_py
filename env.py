import os

def get_or_panic(env_var):
    value = os.environ.get(env_var)
    if value is None:
        raise Exception(f'{env_var} environment variable not set')
    return value
