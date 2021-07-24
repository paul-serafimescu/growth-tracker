from typing import Any

class InvalidResponseError(Exception):
  def __init__(self, message: str = 'invalid response data from Discord API', *args, **kwargs):
    self.message = message
    super().__init__(*args, **kwargs)

  def __str__(self) -> str:
    return self.message

class ResponseParser:
  def __init__(self, json_response: dict[str, Any]):
    self.data = json_response

  def get_or_raise(self, key: str) -> Any:
    if (value := self.data.get(key)) is None:
      raise InvalidResponseError()
    return value
