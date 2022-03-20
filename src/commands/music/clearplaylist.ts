import { Message, MessageEmbed } from 'discord.js';
import { BaseCommand } from 'yuna';
import { Yuna } from '../../config.js';
import { checkSetup } from '../../utils.js';

class clearplaylist implements BaseCommand {
    name: string;
    description: string;

    constructor() {
        this.name = 'clearplaylist';
        this.description = 'clear the entire serverplaylist. (irreversible)';
    }

    async execute(msg: Message<boolean>, args: string[]) {
        console.log('command called');

        /**
         * return if not setup
         */
        const isSetup = await checkSetup(msg.guildId!);
        if (!isSetup) return await msg.reply({ embeds: [Yuna.notSetupYetEmbed] });

        /**
         * return if no song in serverplaylist
         */
        const queue = Yuna.player.getQueue(msg.guild!);
        if (!queue)
            return await msg.reply(
                'There is no song in serverplaylist, add songs using `yuna addsong <url/keywords>`.'
            );

        /**
         * confirmation
         */
        let embed = new MessageEmbed().setColor(Yuna.color).setTitle('⚠️ARE YOU SURE⚠️').setDescription(`
This command will **CLEAR** __every song in the server playlist__ **FOREVER**!
Your action is inreversable.

Write "CONFIRM" to confirm your change.
                 `);

        const confirmationMsg = await msg.reply({ embeds: [embed] });
        const filter = (m: Message) => m.content === 'CONFIRM' && m.author.id === msg.author.id;
        try {
            await msg.channel.awaitMessages({ filter, max: 1, time: 60_000, errors: ['time'] });
        } catch {
            try {
                await confirmationMsg.delete();
            } catch {}
            return await msg.reply('Back to safety! If you decide to clear, do `yuna clearplaylist` again.');
        }

        /**
         * confirmed, update to database
         */
        const guildDocument = await Yuna.database.collection('guilds').doc(msg.guildId).get();
        const guildDocumentData = guildDocument.data();
        guildDocumentData.songs = [];
        await Yuna.database.collection('guilds').doc(msg.guildId).update(guildDocumentData);

        /**
         * stop playing
         */
        queue.destroy(true);

        /**
         * success embed
         */
        embed = new MessageEmbed()
            .setColor(Yuna.color)
            .setTitle('Cleared Successfully')
            .setDescription('Server Playlist has been cleared \n do `yuna addsong <url>` to add new songs!')
            .setTimestamp();
        await msg.reply({ embeds: [embed] });
    }
}

export default new clearplaylist();
