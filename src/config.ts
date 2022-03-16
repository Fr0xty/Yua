import { Player } from 'discord-player';
import Discord, { Intents } from 'discord.js';

const Yuna = new Discord.Client({
    intents: [
        Intents.FLAGS.GUILDS,
        Intents.FLAGS.GUILD_MEMBERS,
        Intents.FLAGS.GUILD_MESSAGES,
        Intents.FLAGS.GUILD_VOICE_STATES,
    ],
});

Yuna.color = '#F7BD72';

Yuna.player = new Player(Yuna);

export { Yuna };
