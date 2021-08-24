/* {DOMAIN_ROOT} */

import React from 'react';

import { parse_object, User, Guild, Page } from '../common';
import * as Components from '../components';

/* context data */
const session_user = parse_object<User>('user');
const logged_in = Boolean(Object.keys(session_user).length);
const all_guilds = parse_object<Guild[]>('guilds');

const _HomePage = new Page({
  'navbar': <Components.NavBar user={session_user} logged_in={logged_in} guilds={all_guilds} />,
  'home-page': <Components.Index user={session_user} guilds={all_guilds} />,
});
