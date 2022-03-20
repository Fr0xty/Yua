import { GuildMember, Message, MessageActionRow, MessageButton, MessageEmbed, VoiceBasedChannel } from 'discord.js';
import { BaseCommand } from 'yuna';
import { Yuna } from '../../config.js';
import { checkSetup } from '../../utils.js';

class changevc implements BaseCommand {
    name: string;
    description: string;

    constructor() {
        this.name = 'changevc';
        this.description = 'change server vc where I will play songs.';
    }

    async execute(msg: Message<boolean>, args: string[]) {
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
    }
}

export default new changevc();
