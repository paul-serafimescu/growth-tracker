import "../styles/index.scss";
// eslint-disable-next-line no-unused-vars
import React from 'react';
import ReactDOM from 'react-dom';

export const App = () => <h1>world!</h1>;

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);
