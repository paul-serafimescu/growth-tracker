import * as React from 'react';

import * as Types from '../common/types';
import * as Components from '../components';

export interface GuildsProps {
  readonly guilds: Types.Guild[];
}

export const Guilds: React.FC<GuildsProps> = ({guilds}: GuildsProps) => {

  return (
    <Components.Container className="guild-container">
      <h1 className="guild-list-title">Your Guilds</h1>
      {guilds.length ? guilds.map((guild, idx) => (
        <a href={`/servers/${guild.guild_id}`} key={idx} className="inline-card">
          <Components.GuildPreview {...guild} />
        </a>
      )) : <h2 className="empty-guild-list-msg">Join a guild to track its progress!</h2>}
    </Components.Container>
  );
};

export default Guilds;
