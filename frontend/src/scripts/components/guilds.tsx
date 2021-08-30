import * as React from 'react';

import * as Types from '../common/types';
import * as Components from './index';

export interface GuildsProps {
  readonly guilds: Types.Guild[];
}

export const Guilds: React.FC<GuildsProps> = ({guilds}: GuildsProps) => {

  return (
    <Components.Container className="guild-container">
      <h1 className="guild-list-title">Your Guilds</h1>
      {guilds.map((guild, idx) => (
        <a href={`/servers/${guild.guild_id}`} key={idx} className="inline-card">
          <Components.GuildPreview {...guild} />
        </a>
      ))}
    </Components.Container>
  );
};

export default Guilds;
