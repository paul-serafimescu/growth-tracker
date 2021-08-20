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
          <Navbar.Brand href="#navbar">Growth Tracker</Navbar.Brand>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Navbar.Collapse id="responsive-navbar-nav">
            <Nav fill variant="pills" defaultActiveKey="/">
              {[
                'Test',
                'Test Again',
                'Test Once More',
              ].map((navlink, idx) => (
                <Nav.Link key={idx} className="navbar-item" href="https://google.com" target="_blank">{navlink}</Nav.Link>
              ))}
              <NavDropdown title="See Guilds" id="navbarScrollingDropdown">
                {guilds.map((guild, idx) => (
                  <NavDropdown.Item key={idx} href="#action">{guild.name}</NavDropdown.Item>
                ))}
              </NavDropdown>
            </Nav>
          </Navbar.Collapse>
          <Navbar.Collapse className="justify-content-end">
            {logged_in ? <Navbar.Text>
              Signed in as: <a href="/">{user.username}</a>
            </Navbar.Text> :
            <Navbar.Text><a href="/">Login</a></Navbar.Text>}
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </Container>
  );
};
