/* {DOMAIN}/servers/{guild_id} */

import * as React from 'react';

import "../../styles/index.scss";
import * as Components from '../components';
import { parse_object, User, Guild, Page } from '../common';

/* context data */
const session_user = parse_object<User>('user');
const logged_in = Boolean(Object.keys(session_user).length);
const all_guilds = parse_object<Guild[]>('guilds');

const _GuildViewPage = new Page({
  'guild-main': <Components.Guild />,
  'navbar': <Components.NavBar user={session_user} logged_in={logged_in} guilds={all_guilds} />,
  'footer': <Components.Footer />,
});
