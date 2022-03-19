import { Message, MessageEmbed } from 'discord.js';
import { BaseCommand } from 'yuna';
import { Yuna } from '../../config.js';
import { checkSetup } from '../../utils.js';

class vc implements BaseCommand {
    name: string;
    description: string;

    constructor() {
        this.name = 'vc';
        this.description = "get voice channel that I'm playing in in the server.";
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

        /**
         * send vc
         */
        const guildProfile = await Yuna.database.collection('guilds').doc(msg.guildId).get();
        const embed = new MessageEmbed()
            .setColor(Yuna.color)
            .setTitle('Voice Channel')
            .setDescription(`I'm currently playing music in <#${guildProfile.data().voiceChannelId}> in this server!`)
            .setAuthor({ name: Yuna.user!.username, iconURL: Yuna.user!.displayAvatarURL() });
        await msg.reply({ embeds: [embed] });
    }
}

export default new vc();
