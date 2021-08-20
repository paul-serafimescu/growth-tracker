import React, {
  useState, useEffect
} from 'react';

import {
  Navbar, Nav, Container,
} from 'react-bootstrap';

import {
  parse_object, Guild
} from '../common';

export const NavBar = () => {
  let [state, setState] = useState<Guild | null>(null);
  state;
  useEffect(
    () => setState(parse_object('guild')), []
  );

  return (
    <>
      <Navbar className="navbar-main" collapseOnSelect fixed="top" expand="sm" bg="primary" variant="dark">
        <Container>
          <Navbar.Brand href="#navbar">Growth Tracker</Navbar.Brand>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Navbar.Collapse id="responsive-navbar-nav">
            <Nav fill>
              {[
                'Test',
                'Test Again',
                'Test Once More',
              ].map((navlink, idx) => (
                <Nav.Link key={idx} className="navbar-item" href="https://google.com" target="_blank">{navlink}</Nav.Link>
              ))}
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </>
  );
};
