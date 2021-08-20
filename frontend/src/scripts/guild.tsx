import * as React from 'react';
import ReactDOM from 'react-dom';

import "../styles/index.scss";
import * as Components from './components/';

Object.entries<JSX.Element>({
  'guild-main': <Components.Guild />,
  'navbar': <Components.NavBar />
}).forEach(([key, value]) => {
  ReactDOM.render(
    <React.StrictMode>{value}</React.StrictMode>,
    document.getElementById(key)
  );
});
