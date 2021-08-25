export class JSONError extends Error {
  constructor(message?: string) {
    super(message);
  }
}

export function parse_object<T = unknown>(id: string): T {
  const element = document.getElementById(id);
  if (element) {
    const retval: T = JSON.parse(element.innerText);
    return retval;
  } else {
    throw new JSONError();
  }
}

export function* range(start: number, end: number, step = 1): Generator<number, void, boolean | undefined> {
  for (let i = start - step; i < end - step; yield (i += step));
}
