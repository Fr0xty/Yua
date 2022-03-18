import { Snowflake } from 'discord.js';
import { Yuna } from './config.js';

export const checkSetup = async (guildId: Snowflake) => {
    const fetchedGuild = await Yuna.database.collection('guilds').doc(guildId).get();
    if (fetchedGuild.exists) return true;
    return false;
};
