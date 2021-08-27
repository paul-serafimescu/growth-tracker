import React, {
  useState,
  useEffect,
} from 'react';

import {
  Navbar, Nav, Container, NavDropdown
} from 'react-bootstrap';

import * as Types from '../common/types';

export interface NavBarProps {
  readonly user: Types.User;
  readonly logged_in: boolean;
  readonly guilds: Types.Guild[];
}

export const NavBar: React.FC<NavBarProps> = ({user, logged_in, guilds}: NavBarProps) => {
  const [display, setDisplay] = useState(true);
  const [height, setHeight] = useState<number | undefined>(undefined);

  const onScroll: EventListener =  (event: Event): void => {
    event.preventDefault();
    if (!height) return;
    setDisplay(window.scrollY <= height);
  };

  useEffect(() => {
    window.addEventListener('scroll', onScroll);
    const nav = document.getElementsByTagName('nav')?.item(0);
    if (nav) {
      setHeight(nav.clientHeight * 2);
    }
  });

  const inviteLink = "";

  return display ? (
    <Container>
      <Navbar id="navbar" className="navbar-main" collapseOnSelect fixed="top" expand="lg" bg="primary" variant="dark">
        <Container>
          <Navbar.Brand href="/">Growth Tracker</Navbar.Brand>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Navbar.Collapse id="responsive-navbar-nav">
            <Nav fill variant="pills" defaultActiveKey="/">
              <Nav.Link className="navbar-item" href="/servers">Guild List</Nav.Link>
              <Nav.Link className="navbar-item" href="">Join Support Discord</Nav.Link>
              <Nav.Link className="navbar-item" href="">Status</Nav.Link>
              <Nav.Link className="navbar-item" href={inviteLink}>Invite</Nav.Link>
              <NavDropdown title="Quick Access" id="navbarScrollingDropdown">
                {guilds.map((guild, idx) => (
                  <NavDropdown.Item key={idx} href={`/servers/${guild.guild_id}`}>{guild.name}</NavDropdown.Item>
                ))}
              </NavDropdown>
            </Nav>
          </Navbar.Collapse>
          <Navbar.Collapse className="justify-content-end">
            {logged_in ? <Navbar.Text>
              Signed in as: <a href="/">{user.username}#{user.discriminator}</a>
              <img
                className="icon-navbar"
                src={`https://cdn.discordapp.com/avatars/${user.discord_id}/${user.avatar}.${user.avatar.startsWith("a_") ? "gif" : "png"}?size=32`}
                alt="icon"
              />
              <a className="btn btn-info logout-btn justify-content-end" href="accounts/logout">
                <i className="icon fa">&#xf08b;</i>
              </a>
            </Navbar.Text> :
            <Navbar.Text><a href="/">Login</a></Navbar.Text>}
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </Container>
  ) : null;
};

export default NavBar;
