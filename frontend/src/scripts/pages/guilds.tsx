/* {DOMAIN}/servers */

import * as React from 'react';
import * as Components from '../components';
import * as BaseData from './common';
import Page from '../common/page';

export const GuildsListPage = new Page({
  'guilds-main': <Components.Guilds guilds={BaseData.all_guilds} />,
  'navbar': <Components.NavBar user={BaseData.session_user} logged_in={BaseData.logged_in} guilds={BaseData.all_guilds} />,
  'footer': <Components.Footer />,
});
