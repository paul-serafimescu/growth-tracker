import * as React from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import ListGroup from 'react-bootstrap/ListGroup';
import Container from 'react-bootstrap/Container';
import { range } from '../common';

export interface FooterProps {
  [link: string]: string | number;
}

export const Footer: React.FC<FooterProps> = (props: FooterProps) => {
  return (
    <div className="footer">
      <Container>
        <Row>
          <Col className="d-none d-lg-block">
            <div></div>
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
            <div></div>
          </Col>
          <Col>
            <ListGroup variant="flush">
              {[...range(0, 5)].map((_, idx) => (
                <ListGroup.Item key={idx} className="list-item-mod">
                  <p className="list-item-text">{props.test}</p>
                </ListGroup.Item>
              ))}
            </ListGroup>
          </Col>
          <Col>
            <ListGroup variant="flush">
              {[...range(0, 5)].map((_, idx) => (
                <ListGroup.Item key={idx} className="list-item-mod">
                  <p className="list-item-text">{props.test}</p>
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
