import * as React from 'react';

import {
  Container, Row, Col as Column, Image, Button
} from 'react-bootstrap';

import { range } from '../common/util';
import '../../styles/index.scss';

export interface UserCardProps {
  readonly avatar: string;
  readonly discord_id: string;
  readonly number_guilds: number;
  readonly username: string;
  readonly discriminator: string;
}

export interface FullWidthProps {
  children?: JSX.Element;
}

export const fetchElementWidth = (id: string): number => {
  const element = document.getElementById(id);
  if (element == undefined) {
    throw Error();
  }
  return element.clientWidth;
};

export const Divider: React.FC = () => <hr className="mt-2 mb-3" />;

export const FullWidth: React.FC<FullWidthProps> = ({children}: FullWidthProps) => <div className="d-grid gap-2">{children}</div>;

export const UserCard: React.FC<UserCardProps> = (props: UserCardProps) => (
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

export const Index: React.FC = () => {
  return (
    <>
      <Container>
        <Row className="align-items-center">
          <Column className="about">
            <Container className="about-content">
              <Row className="about-title align-self-center">
                <Column>
                  <div className="display-2 bot-title">A Discord Bot that measures server growth with ease.</div>
                </Column>
              </Row>
              <Divider />
              <div className="links-header">
                <h4 className="display-5">Helpful Links</h4>
              </div>
              <Row className="btn-links">
                <Column>
                  <FullWidth>
                    <Button href="/api" variant="primary" size="lg">API Reference</Button>
                  </FullWidth>
                </Column>
                <Column>
                  <FullWidth>
                    <Button href="/commands" variant="primary" size="lg">Commands</Button>
                  </FullWidth>
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
