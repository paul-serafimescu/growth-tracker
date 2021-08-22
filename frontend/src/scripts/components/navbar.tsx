import React, {
  FunctionComponent,
} from 'react';

import {
  Navbar, Nav, Container, NavDropdown
} from 'react-bootstrap';

import * as Types from '../common/types';

export interface NavBarProps {
  user: Types.User;
  logged_in: boolean;
  guilds: Types.Guild[];
}

export const NavBar: FunctionComponent<NavBarProps> = ({user, logged_in, guilds}: NavBarProps) => {
  return (
    <Container>
      <Navbar className="navbar-main" collapseOnSelect fixed="top" expand="sm" bg="primary" variant="dark">
        <Container>
          <Navbar.Brand href="/">Growth Tracker</Navbar.Brand>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Navbar.Collapse id="responsive-navbar-nav">
            <Nav fill variant="pills" defaultActiveKey="/">
              <Nav.Link className="navbar-item" href="/servers">Guild List</Nav.Link>
              <NavDropdown title="Quick Access" id="navbarScrollingDropdown">
                {guilds.map((guild, idx) => (
                  <NavDropdown.Item key={idx} href={`/servers/${guild.guild_id}`}>{guild.name}</NavDropdown.Item>
                ))}
              </NavDropdown>
              <Nav.Link className="navbar-item" href="/accounts/logout">Logout</Nav.Link>
            </Nav>
          </Navbar.Collapse>
          <Navbar.Collapse className="justify-content-end">
            {logged_in ? <Navbar.Text>
              Signed in as: <a href="/">{user.username}#{user.discriminator}</a>
              <img
                src={`https://cdn.discordapp.com/avatars/${user.discord_id}/${user.avatar}.${user.avatar.startsWith("a_") ? "gif" : "png"}?size=32`}
                alt="icon"
              />
            </Navbar.Text> :
            <Navbar.Text><a href="/">Login</a></Navbar.Text>}
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </Container>
  );
};

export default NavBar;
