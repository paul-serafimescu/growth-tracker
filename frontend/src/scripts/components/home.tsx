import React, {
  FunctionComponent
} from 'react';

import {
  Container, Row, Col as Column, Image
} from 'react-bootstrap';

import * as Types from '../common/types';
import { range } from '../common/util';
import '../../styles/index.scss';

export interface IndexProps {
  readonly user: Types.User;
  readonly guilds: Types.Guild[];
}

export interface UserCardProps {
  readonly avatar: string;
  readonly discord_id: string;
  readonly number_guilds: number;
  readonly username: string;
  readonly discriminator: string;
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
    <Column className="px-1 col-md-auto user-card">
      <div className="float-right user-card-body">
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
    <Column className="px-1 col-md-auto user-card user-card-body">
        <div className="float-left">
          <p></p>
          <h3 className="avatar-name">{props.username}
            <div className="descriptor">#{props.discriminator}{[...range(0, 10)].map((_, idx) => <span key={idx}>&nbsp;</span>)}</div>
          </h3>
          <h5 className="faint-subtitle">{props.number_guilds} Guilds</h5>
        </div>
    </Column>
  </>
);

export const Index: FunctionComponent<IndexProps> = ({user, guilds}: IndexProps) => {
  const invite = "";
  return (
    <>
      <Container>
        <Row className="align-items-center">
          <Column className="about">
            <Container className="about-content">
              <Row className="about-title align-self-center">
                <Column>
                  <div className="display-2">A Discord Bot that tracks server growth with ease.</div>
                </Column>
              </Row>
              <hr className="mt-2 mb-3" />
              <Row>
                <UserCard
                  username={user.username}
                  avatar={user.avatar}
                  number_guilds={guilds.length}
                  discord_id={user.discord_id}
                  discriminator={user.discriminator}
                />
              </Row>
              <Row>
                <Column>
                  hi
                </Column>
                <Column>
                  <h4 className="display-7 mg-10"><a href={invite}>Add Growth Tracker</a></h4>
                </Column>
              </Row>
            </Container>
          </Column>
        </Row>
      </Container>
    </>
  );
};

export default Index;
