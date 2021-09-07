from abc import ABC, abstractmethod
from requests import get, post
from typing import Any, Callable, Union
from .exceptions import ResponseError

class RequestModule(ABC):
  def __init__(self, token: str, token_type: str = 'Bearer'):
    self.token = token
    self.headers = {
      'Authorization': f'{token_type} {token}'
    }

  @abstractmethod
  def __str__(self) -> str:
    raise NotImplementedError()

  def get(self, url: str) -> dict[str, Any]:
    return get(url, headers=self.headers).json()

  def post(self, url: str, data: dict[str, Any] = {}) -> dict[str, Any]:
    return post(url, data=data, headers=self.headers)

def raise_on_error(func: Callable[..., Union[list[dict[str, Any]], dict[str, Any]]]):
  def wrapped_func(*args, **kwargs):
    if (message := result.get('message') if isinstance((result := func(*args, **kwargs)), dict) else None) is not None:
      raise ResponseError(message)
    return result
  return wrapped_func
