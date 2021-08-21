/* {DOMAIN_ROOT} */

import React from 'react';
import ReactDOM from 'react-dom';

import { parse_object, User, Guild } from '../common';
import * as Components from '../components';

/* context data */
let session_user = parse_object<User>('user');
let logged_in = Boolean(Object.keys(session_user).length);
let all_guilds = parse_object<Guild[]>('guilds');

/* page DOM rendering */
Object.entries<JSX.Element>({
  'navbar': <Components.NavBar user={session_user} logged_in={logged_in} guilds={all_guilds} />
}).forEach(([key, value]) => {
  ReactDOM.render(
    <React.StrictMode>{value}</React.StrictMode>,
    document.getElementById(key)
  );
});
