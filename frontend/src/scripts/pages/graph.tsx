/* {DOMAIN}/servers/{guild_id} */

import * as React from 'react';
import * as Components from '../components';
import * as BaseData from './common';
import '../../styles/index.scss';
import Page from '../common/page';

export const GuildViewPage = new Page({
  'graph-root': <Components.Graph />,
  'navbar': <Components.NavBar user={BaseData.session_user} logged_in={BaseData.logged_in} guilds={BaseData.all_guilds} />,
  'footer': <Components.Footer />,
});
