export interface Guild {
  id: number;
  name: string;
  guild_id: string;
  icon: string;
  permissions: string;
  members: number | null;
}

export interface User {
  id: number;
  username: string;
  discord_id: string;
  avatar: string;
  discriminator: string;
}
