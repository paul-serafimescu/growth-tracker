import React, {
  FunctionComponent
} from 'react';

import {
  Container, Row, Col as Column, Image
} from 'react-bootstrap';

import * as Types from '../common/types';
import '../../styles/index.scss';

export interface IndexProps {
  readonly user: Types.User;
  readonly guilds: Types.Guild[];
}

export interface UserCardProps {
  avatar: string;
  discord_id: string;
  number_guilds: number;
  username: string;
  discriminator: string;
}

export const fetchElementWidth = (id: string): number => {
  const element = document.getElementById(id);
  if (element == undefined) {
    throw Error();
  }
  return element.clientWidth;
};

export const UserCard: FunctionComponent<UserCardProps> = (props: UserCardProps) => (
  <>
    <Column className="px-1 col-md-auto">
      <div className="float-right">
        <Image className="icon-main"
          src={
            `https://cdn.discordapp.com/avatars/${props.discord_id}/${props.avatar}.${props.avatar.startsWith("a_")
              ? "gif" :
              "png"}?size=${fetchElementWidth('body') > 600 ? 128 : 64}`
          }
          alt="user-avatar"
          width="110"
          height="110"
        />
      </div>
    </Column>
    <Column className="px-1 col-md-auto">
        <div className="float-left">
          <p></p>
          <h3 className="avatar-name">{props.username}
            <div className="descriptor">#{props.discriminator}</div>
          </h3>
          <h5 className="faint-subtitle">{props.number_guilds} Guilds</h5>
        </div>
    </Column>
  </>
);

export const Index: FunctionComponent<IndexProps> = ({user, guilds}: IndexProps) => {
  return (
    <Container>
      <Row>
        <UserCard
          username={user.username}
          avatar={user.avatar}
          number_guilds={guilds.length}
          discord_id={user.discord_id}
          discriminator={user.discriminator}
        />
      </Row>
    </Container>
  );
};

export default Index;
