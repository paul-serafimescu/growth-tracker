import * as React from 'react';
import ReactDOM from 'react-dom';

export interface PageProps {
  readonly [key: string]: JSX.Element | string;
}

export class Page<T extends PageProps> {
  constructor(props: T) {
    Object.entries(props).forEach(([key, value]) => {
      ReactDOM.render(
        <React.StrictMode>{value}</React.StrictMode>,
        document.getElementById(key)
      );
    });
  }
}

export default Page;
