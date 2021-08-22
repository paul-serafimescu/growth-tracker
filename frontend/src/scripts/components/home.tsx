import React, {
  FunctionComponent
} from 'react';

import {
  Container, Row, Col as Column, Image
} from 'react-bootstrap';

import * as Types from '../common/types';
import '../../styles/index.scss';

export interface IndexProps {
  user: Types.User;
}

export const Index: FunctionComponent<IndexProps> = ({user}: IndexProps) => {
  return (
    <Container>
      <Row>
        <Column>
          <Image className="icon-main"
            src={`https://cdn.discordapp.com/avatars/${user.discord_id}/${user.avatar}.${user.avatar.startsWith("a_") ? "gif" : "png"}?size=128`}
            alt="user-avatar"
            width="110"
            height="110"
          />
          <h4 className="avatar-name">{user.username}</h4>
          <h4 className="descriptor">#{user.discriminator}</h4>
        </Column>
      </Row>
    </Container>
  );
};

export default Index;
