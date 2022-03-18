import {
    GuildMember,
    Message,
    MessageActionRow,
    MessageButton,
    MessageEmbed,
    VoiceBasedChannel,
    VoiceChannel,
} from 'discord.js';
import { BaseCommand } from 'yuna';
import { Yuna } from '../../config.js';
import { checkSetup } from '../../utils.js';

class serverreset implements BaseCommand {
    name: string;
    description: string;

    constructor() {
        this.name = 'serverreset';
        this.description = 'to set me up in your server.';
    }

    async execute(msg: Message<boolean>, args: string[]) {
        /**
         * return if not setup
         */
        const isSetup = await checkSetup(msg.guildId!);
        if (!isSetup) return await msg.reply({ embeds: [Yuna.notSetupYetEmbed] });

        /**
         * confirmation
         */
        let embed = new MessageEmbed().setColor(Yuna.color).setTitle('⚠️ARE YOU SURE⚠️').setDescription(`
This command will **REMOVE** your __Voice Channel__ and __Server Playlist__ data **FOREVER**!
Your action is inreversable.

You might want to:
> \`yuna changevc\`
> \`yuna resetplaylist\`

Write "CONFIRM" to confirm your change.
        `);

        const confirmationMsg = await msg.reply({ embeds: [embed] });
        const filter = (m: Message) => m.content === 'CONFIRM' && m.author.id === msg.author.id;
        try {
            await msg.channel.awaitMessages({ filter, max: 1, time: 60_000, errors: ['time'] });
        } catch {
            return await msg.reply('Back to safety! If you really want to reset, please try again.');
        }

        /**
         * confirmed
         */
        await Yuna.database.collection('guilds').doc(msg.guildId).delete();
        embed = new MessageEmbed()
            .setColor(Yuna.color)
            .setTitle('Reset Successful')
            .setDescription('Every server data has been reset! \n do `yuna setup` to setup again!')
            .setTimestamp();
        await msg.reply({ embeds: [embed] });
    }
}

export default new serverreset();
