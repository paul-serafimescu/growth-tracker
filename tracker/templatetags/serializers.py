from django import template
from django.db import models
from typing import Any, Union

register = template.Library()

@register.filter
def serialize(value: Union[models.Model, list]) -> Union[dict[str, Any], list[dict[str, Any]]]:
  if isinstance(value, models.Model):
    try:
      return value.serialize()
    except AttributeError:
      return {}
  elif isinstance(value, list):
    return list(map(lambda model: model.serialize(), value))
  else:
    raise ValueError() # figure this out later
