import * as React from 'react';
import {
  Container, Col as Column, Row,
  Card, CardImgProps, Image, ImageProps,
  Spinner
} from 'react-bootstrap';

import parse_object from '../common/util';

export interface GuildProps {
  readonly id: number,
  readonly name: string,
  readonly bot_joined: boolean,
  readonly members: number | null,
  readonly icon: string | null,
  readonly guild_id: string,
  readonly created: string,
}

export interface GuildPreviewProps {
  readonly name: string;
  readonly icon: string | null;
  readonly guild_id: string;
}

export enum IconType {
  Blank, Exists
}

export class Icon {
  public readonly type: IconType;
  private readonly _url: string | undefined;
  private readonly _name: string;

  constructor(icon: string | null, name: string, guild_id: string) {
    switch (typeof icon) {
      case "string":
        this.type = IconType.Exists;
        this._url = `https://cdn.discordapp.com/icons/${guild_id}/${icon}.png`;
        break;
      default:
        this.type = IconType.Blank;
    }
    this._name = name;
  }

  public url = (large = false): string => (this._url ?? "https://upload.wikimedia.org/wikipedia/commons/8/89/HD_transparent_picture.png") + (large ? "?size=4096" : "");

  public renderCard = (props: CardImgProps, onHover: React.MouseEventHandler): JSX.Element => {
    return (
      <div className="card-img-caption">
        {!this._url && <h2 className="card-text">{this._name.split(/\s+/).map(element => element[0])}</h2>}
        <Card.Img {...props} onMouseEnter={onHover} onMouseLeave={onHover} />
      </div>
    );
  }

  public renderImage = (props: ImageProps): JSX.Element => {
    return (
      <div className="card-img-caption">
        {!this._url && <h2 className="card-text">{this._name.split(/\s+/).map(element => element[0])}</h2>}
        <Image id="guild-image" className="guild-image" {...props} />
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

    return _icon.renderCard(props, handleHover);
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

export const Guild: React.FC = () => {
  const [guild, _setGuild] = React.useState<GuildProps>(parse_object('guild'));

  const invite = "";

  const GuildJoinedView: React.FC<GuildProps> = ({guild_id, members, created}: GuildProps) => {
    return (
      <Container className="guild-view">
        <ul>
          <li><p className="display-6">Member count: {members}</p></li>
          <li><p className="display-6">Tracking since: {new Date(created).toLocaleDateString()}</p></li>
          <li><a href={`/servers/${guild_id}/graph`} className="display-6">See graph</a></li>
          {/* TODO: any other basic metadata or statistics which can be computed from basic properties */}
        </ul>
      </Container>
    );
  };

  const GuildDefaultView: React.FC = () => {
    return (
      <Container className="guild-view-default">
        <Container className="align-items-center">
          <h2 className="text-info">You have not added Growth Tracker to this guild!</h2>
          <a className="text-info invite-link" href={invite}><h3>Click to invite</h3></a>
        </Container>
      </Container>
    );
  };

  const renderGuildView = ({bot_joined, icon, name, guild_id, ...props}: GuildProps): JSX.Element => {
    const _icon = new Icon(icon, name, guild_id);
    const [loading, setLoading] = React.useState(true);

    const handleLoad = (event: React.ChangeEvent<HTMLImageElement>) => {
      event.preventDefault();
      setLoading(false);
    };

    return (
      <>
        <Column className="align-items-center" md>
          {loading && (
            <Spinner className="loading-spinner" animation="border" role="status" >
              <span className="visually-hidden">Loading...</span>
            </Spinner>
          )}
          {_icon.renderImage({ src: _icon.url(true), width: "75%", onLoad: handleLoad })}
        </Column>
        <Column>
          {bot_joined ?
            <GuildJoinedView bot_joined={bot_joined} icon={icon} name={name} guild_id={guild_id} {...props} /> :
            <GuildDefaultView />}
        </Column>
      </>
    );
  };

  return (
    <Container>
      <Container>
        <h1 className="mgt-50">{guild.name}</h1>
      </Container>
      <Row>
        {renderGuildView(guild)}
      </Row>
    </Container>
  );
};
