from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.test.client import CONTENT_TYPE_RE
from django.views import View
from django.urls import resolve
from abc import abstractclassmethod, ABCMeta
from typing import Any, Callable, Union, Type
from json import dumps

class ViewTest(TestCase, metaclass=ABCMeta):
  user: Union[AbstractBaseUser, AnonymousUser]
  factory: RequestFactory

  @abstractclassmethod
  def setUpTestData(cls) -> None:
    raise NotImplementedError()

class DecoratorError(Exception):
  def __init__(self, message: str, *args: Any, **kwargs: Any):
    self.message = message

  def __str__(self) -> str:
    return f"invalid decorator usage: '{self.message}'"

def route(request_type: str, url: str, view: Type[View], headers: dict[str, Any] = {}, data: dict[str, Any] = {}, logged_in: bool = False):
  """ this is totally nuts

      i can't believe i spent time on this
  """
  def inner_function(function: Callable[..., Any]):
    def wrapped(self, *args, **kwargs):
      if not isinstance(self, ViewTest):
        raise DecoratorError('argument is not an instance method')
      _, _args, _kwargs = resolve(url)
      _data = dumps(data)
      request_types = {
        'patch': self.factory.patch(url, _data, content_type='application/json'),
        'get': self.factory.get(url),
        'post': self.factory.post(url, _data, content_type='application/json'),
        'put': self.factory.put(url, _data, content_type='application/json'),
        # 'head': self.factory.head(url, _data, content_type='application/json'),
        'delete': self.factory.delete(url, _data, content_type='application/json'),
        'options': self.factory.options(url, _data, content_type='application/json'),
        'trace': self.factory.trace(url),
      }
      if (request := request_types.get(request_type)) is None:
        raise KeyError('invalid request type')
      if logged_in:
        request.user = self.user
      request.headers = headers
      return function(self, view.as_view()(request, *_args, **_kwargs), *args, **kwargs)
    return wrapped
  return inner_function
