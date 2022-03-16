import { Player } from 'discord-player';
import Discord, { Collection, Intents } from 'discord.js';
import firebaseAdmin from 'firebase-admin';

/**
 * Yuna instance
 */
const Yuna = new Discord.Client({
    intents: [
        Intents.FLAGS.GUILDS,
        Intents.FLAGS.GUILD_MEMBERS,
        Intents.FLAGS.GUILD_MESSAGES,
        Intents.FLAGS.GUILD_VOICE_STATES,
    ],
});

/**
 * Yuna's properties
 */
Yuna.color = '#F7BD72';
Yuna.prefix = 'yuna ';

/**
 * to store all Yuna's commands
 */
Yuna.commands = new Collection();

/**
 * player from discord-player
 */
Yuna.player = new Player(Yuna);

/**
 * connect to firebase
 */
const app = firebaseAdmin.initializeApp({
    credential: firebaseAdmin.credential.cert(JSON.parse(process.env.FIREBASE_CREDENTIALS!)),
});
Yuna.database = app.firestore();
await Yuna.database.collection('guilds').doc('guildId').delete();

export { Yuna };
