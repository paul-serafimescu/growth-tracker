export class JSONError extends Error {
  constructor(message?: string) {
    super(message);
  }
}

export function parse_object<T = Object>(id: string): T {
  let element = document.getElementById(id);
  if (element) {
    let retval: T = JSON.parse(element.innerText);
    return retval;
  } else {
    throw new JSONError();
  }
}
