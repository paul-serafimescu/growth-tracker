class EnvNotFoundError(Exception):
  def __init__(self, message: str = '.env file not found', *args, **kwargs):
    self.message = message
    super().__init__(*args, **kwargs)

  def __str__(self) -> str:
    return self.message

class EnvKeyNotFoundError(Exception):
  def __init__(self, key: str, *args, **kwargs):
    self.key = key
    super().__init__(*args, **kwargs)

  def __str__(self) -> str:
    return f"'{self.key}' not found in .env file"
