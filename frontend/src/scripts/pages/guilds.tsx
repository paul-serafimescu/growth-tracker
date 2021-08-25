/* {DOMAIN}/servers */

import * as React from 'react';

import { parse_object, User, Guild, Page } from '../common';
import * as Components from '../components';

/* context data */
const session_user = parse_object<User>('user');
const logged_in = Boolean(Object.keys(session_user).length);
const all_guilds = parse_object<Guild[]>('guilds');

const _GuildsListPage = new Page({
  'guilds-main': <Components.Guilds guilds={all_guilds} />,
  'navbar': <Components.NavBar user={session_user} logged_in={logged_in} guilds={all_guilds} />,
  'footer': <Components.Footer test="hi" />,
});
