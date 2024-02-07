import os


async def get_env():
    _env_path = os.path.join(os.path.dirname(__file__), '..', '.env')

    with open(_env_path, 'r') as file:
        for line in file:
            if '=' in line:
                key, value = line.strip().split('=')

                os.environ[key] = value
