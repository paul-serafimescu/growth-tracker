export interface Guild {
  readonly id: number;
  readonly name: string;
  readonly guild_id: string;
  readonly icon: string;
  readonly members: number | null;
}

export interface User {
  readonly id: number;
  readonly username: string;
  readonly discord_id: string;
  readonly avatar: string;
  readonly discriminator: string;
}
