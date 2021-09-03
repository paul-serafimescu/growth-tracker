import * as React from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import ListGroup from 'react-bootstrap/ListGroup';
import Container from 'react-bootstrap/Container';
import Image from 'react-bootstrap/Image';

export function getOffsetTop(element: HTMLElement | null): number {
  return !element || element === document.body ?
    0 :
    element.offsetTop + element.clientHeight + getOffsetTop(element.parentElement);
}

export const Footer: React.FC = () => {

  const [height, setHeight] = React.useState({
    clientHeight: document.body.clientHeight,
    innerHeight: window.innerHeight,
  });

  React.useEffect(() => {

    window.addEventListener('resize', () => setHeight({
      clientHeight: document.body.clientHeight,
      innerHeight: window.innerHeight
    }));

    const footer = document.getElementById('footer');
    if (getOffsetTop(footer) < height.innerHeight)
      if (footer)
        footer.className = "place-bottom";

    return function() {
      if (footer)
        footer.className = "";
    };
  });

  return (
    <div className="footer">
      <Container>
        <Row>
          <Col className="d-none d-lg-block">
            <p className="footer-header"></p>
          </Col>
          <Col>
            <p className="footer-header">GROWTH TRACKER</p>
          </Col>
          <Col>
            <p className="footer-header">MISCELLANEOUS</p>
          </Col>
        </Row>
        <Row>
          <Col className="d-none d-lg-block">
            <Row className="gt-logo">
              <Col>
                <Image src="https://via.placeholder.com/100" width="100" height="100" />
              </Col>
            </Row>
            <Row>
              <small className="social-header">GET IN TOUCH</small>
              {[
                ['fab fa-discord', 'https://discord.com'], // this should be changed to whatever support server invite
                ['fab fa-twitter', 'https://twitter.com'], // likewise, with whatever twitter
                ['fab fa-reddit', 'https://reddit.com'],
                ['fad fa-envelope-square', 'https://mail.google.com'], // and likewise, with email
              ].map(([icon, link], idx) => (
                <Col key={idx} md="auto">
                  <a className="footer-link" href={link} target="_blank" rel="noreferrer">
                    <i className={`${icon} social-icon`}></i>
                  </a>
                </Col>
              ))}
            </Row>
          </Col>
          <Col>
            <ListGroup variant="flush">
              {[
                ['API', '/api'],
                ['Help', '/commands'],
                ['Public Servers', '/public'],
                ['User Policy', '/policy'],
              ].map(([text, link], idx) => (
                <ListGroup.Item key={idx} className="list-item-mod">
                  <p className="list-item-text">
                    <a className="footer-link" href={link} target="_blank" rel="noreferrer">{text}</a>
                  </p>
                </ListGroup.Item>
              ))}
            </ListGroup>
          </Col>
          <Col>
            <ListGroup variant="flush">
              {[
                ['Discord', 'https://discord.com'],
                ['Discord API Root', 'https://discord.com/api/v8'],
                ['Discord Developer Docs', 'https://discord.com/developers/docs/intro'],
                ['discord.py API Docs', 'https://discordpy.readthedocs.io/en/stable/'],
              ].map(([text, link], idx) => (
                <ListGroup.Item key={idx} className="list-item-mod">
                  <p className="list-item-text">
                    <a className="footer-link" href={link} target="_blank" rel="noreferrer">{text}</a>
                  </p>
                </ListGroup.Item>
              ))}
            </ListGroup>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default Footer;
