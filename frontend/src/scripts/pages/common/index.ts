import { parse_object, User, Guild } from '../../common';

export const session_user = parse_object<User>('user');
export const logged_in = Boolean(Object.keys(session_user).length);
export const all_guilds = parse_object<Guild[]>('guilds');
