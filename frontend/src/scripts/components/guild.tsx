import * as React from 'react';
import {
  Container, Col as Column, Row,
  Card, CardImgProps
} from 'react-bootstrap';

import {
  parse_object
} from '../common';

export interface GuildProps {
  id: number,
  name: string,
}

export interface GuildPreviewProps {
  name: string;
  icon: string | null;
  guild_id: string;
}

export enum IconType {
  Blank, Exists
}

export class Icon {
  type: IconType;
  #url: string | undefined;
  #name: string;

  constructor(icon: string | null, name: string, guild_id: string) {
    switch (typeof icon) {
      case "string":
        this.type = IconType.Exists;
        this.#url = `https://cdn.discordapp.com/icons/${guild_id}/${icon}.png`;
        break;
      default:
        this.type = IconType.Blank;
    }
    this.#name = name;
  }

  url = (): string => this.#url ?? "https://upload.wikimedia.org/wikipedia/commons/8/89/HD_transparent_picture.png";

  render = (props: CardImgProps, onHover: React.MouseEventHandler): JSX.Element => {
    return (
      <div className="card-img-caption">
        {!this.#url && <h2 className="card-text">{this.#name.split(/\s+/).map(element => element[0])}</h2>}
        <Card.Img {...props} onMouseEnter={onHover} onMouseLeave={onHover} />
      </div>
    );
  }
}

export const GuildPreview: React.FC<GuildPreviewProps> = ({name, icon, guild_id}: GuildPreviewProps) => {
  const _icon = new Icon(icon, name, guild_id);

  const [hovering, toggleHover] = React.useState(false);
  const [imageURL, setURL] = React.useState(_icon.url());

  const renderIcon = (icon: string | null, guild_id: string): JSX.Element => {
    const props: CardImgProps = {
      src: imageURL,
      variant: "top",
      alt: `${name} icon`,
      height: 128,
    };

    const handleHover = (event: React.MouseEvent<HTMLImageElement>): void => {
      event.preventDefault();
      if (!icon) return;
      if (!hovering) {
        setURL(`https://cdn.discordapp.com/icons/${guild_id}/${icon}.${icon.startsWith("a_") ? "gif" : "png"}`);
        toggleHover(true);
      } else {
        setURL(`https://cdn.discordapp.com/icons/${guild_id}/${icon}.png`);
        toggleHover(false);
      }
    };

    React.useEffect(() => {
      if (icon) props.src = imageURL;
    });

    return _icon.render(props, handleHover);
  };

  return (
    <Card className="guild-preview" bg="primary">
      {renderIcon(icon, guild_id)}
      <Card.Body className="guild-body">
        <Card.Text>{name}</Card.Text>
      </Card.Body>
    </Card>
  );
};

const _Guild: React.FC<GuildProps> = ({id, name}: GuildProps) => {
  return (
    <>
      <h1>{id}</h1>
      <h1>{name}</h1>
    </>
  );
};

export const Guild: React.FC<Record<string, unknown>> = () => {
  const _guild = parse_object<GuildProps>('guild');

  return (
    <Container>
      <Row>
        <Column>
          <_Guild id={_guild.id} name={_guild.name} />
        </Column>
        <Column>
          <h1>hi</h1>
        </Column>
      </Row>
    </Container>
  );
};
