import React, {
  FunctionComponent
} from 'react';
import {
  Container, Col as Column, Row
} from 'react-bootstrap';

import {
  parse_object
} from '../common';

export interface GuildProps {
  id: number,
  name: string,
}

const _Guild: FunctionComponent<GuildProps> = ({id, name}: GuildProps) => {
  return (
    <>
      <h1>{id}</h1>
      <h1>{name}</h1>
    </>
  );
};

export interface GuildPreviewProps {
  name: string;
  icon: string;
  guild_id: string;
}

export const GuildPreview: FunctionComponent<GuildPreviewProps> = ({name, icon, guild_id}: GuildPreviewProps) => {
  return (
    <>
      <h2>{name}</h2>
      <p>{icon}</p>
      <p>{guild_id}</p>
    </>
  );
};

export const Guild: FunctionComponent<{}> = () => {
  let _guild = parse_object<GuildProps>('guild');
  return (
    <Container>
      <Row>
        <Column>
          <_Guild id={_guild.id} name={_guild.name} />
        </Column>
        <Column>
          <h1>hi</h1>
        </Column>
      </Row>
    </Container>
  );
};
