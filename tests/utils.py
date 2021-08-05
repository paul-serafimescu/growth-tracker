from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.views import View
from django.urls import resolve
from abc import abstractclassmethod, ABCMeta
from typing import Any, Callable, Union, Type

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

def route(request_type: str, url: str, view: Type[View], data: dict[str, Any] = {}, logged_in: bool = False):
  """ this is totally nuts

      i can't believe i spent time on this
  """
  def inner_function(function: Callable[..., Any]):
    def wrapped(self, *args, **kwargs):
      if not isinstance(self, ViewTest):
        raise DecoratorError('argument is not an instance method')
      _, _args, _kwargs = resolve(url)
      request_types = {
        'patch': self.factory.patch(url, data),
        'get': self.factory.get(url),
        'post': self.factory.post(url, data),
        'put': self.factory.put(url, data),
        'head': self.factory.head(url, data),
        'delete': self.factory.delete(url, data),
      }
      if (request := request_types.get(request_type)) is None:
        raise KeyError('invalid request type')
      if logged_in:
        request.user = self.user
      return function(self, view.as_view()(request, *_args, **_kwargs), *args, **kwargs)
    return wrapped
  return inner_function
