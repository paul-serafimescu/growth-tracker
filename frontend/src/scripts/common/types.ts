export interface Guild {
  id: number;
  name: string;
  guild_id: string;
  icon: string;
  permissions: string;
  members: number | null;
}
