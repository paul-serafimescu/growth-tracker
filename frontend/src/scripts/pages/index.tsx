/* {DOMAIN_ROOT} */

import * as React from 'react';
import * as Components from '../components';
import * as BaseData from './common';
import Page from '../common/page';

export const HomePage = new Page({
  'navbar': <Components.NavBar user={BaseData.session_user} logged_in={BaseData.logged_in} guilds={BaseData.all_guilds} />,
  'home-page': <Components.Index />,
  'footer': <Components.Footer />,
});
