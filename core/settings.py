from environ import Env
from dataclasses import dataclass

@dataclass
class Bots:
  bot_token: str
  admin_id: int
  allowed_users: list


@dataclass
class Settings:
  bots: Bots


def get_settings(path: str):
  env = Env() 
  env.read_env(path)

  return Settings(
    bots=Bots(
      bot_token=env.str('TOKEN'),
      admin_id=env.str('ADMIN_ID'),
      allowed_users=env.list('ALLOWED_USERS')
    )
  )

settings = get_settings('input')