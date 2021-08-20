import React, {
  FunctionComponent
} from 'react';

import {
  parse_object
} from '../common';

export interface GuildProps {
  id: number,
  name: string,
}

export const _Guild: FunctionComponent<GuildProps> = ({id, name}: GuildProps) => {
  return (
    <>
      <h1>{id}</h1>
      <h1>{name}</h1>
    </>
  );
};

export const Guild: FunctionComponent<{}> = () => {
  let _guild = parse_object<GuildProps>('guild');
  return (
    <_Guild id={_guild.id} name={_guild.name} />
  );
};
