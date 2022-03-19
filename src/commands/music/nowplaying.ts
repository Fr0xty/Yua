import { Message, MessageEmbed } from 'discord.js';
import { BaseCommand } from 'yuna';
import { Yuna } from '../../config.js';
import { checkSetup } from '../../utils.js';

class nowplaying implements BaseCommand {
    name: string;
    description: string;
    aliases: string[];

    constructor() {
        this.name = 'nowplaying';
        this.description = 'get now playing song information.';
        this.aliases = ['np'];
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
         * create embed and send
         */
        const npMusic = queue.nowPlaying();
        if (!npMusic) return await msg.reply('There is no more music in queue, use `play` to add more songs.');

        const progress = queue.createProgressBar();
        const timestamp = queue.getPlayerTimestamp();

        const embed = new MessageEmbed()
            .setColor(Yuna.color)
            .setAuthor({
                name: `Music queue for ${queue.guild.name}`,
                iconURL: queue.guild.iconURL() ? queue.guild.iconURL()! : Yuna.user!.displayAvatarURL(),
            })
            .setThumbnail(npMusic.thumbnail)
            .setTitle('Now Playing:')
            .setDescription(
                `
[${npMusic.title}](${npMusic.url}) - \`${npMusic.duration}\`
${progress}
[**${timestamp.progress}**%]
                    `
            )
            .addFields(
                { name: 'Source', value: npMusic.source },
                { name: 'Artist', value: npMusic.author },
                { name: 'Views', value: String(npMusic.views) },
                { name: 'Requested by', value: `<@${npMusic.requestedBy.id}>` }
            );
        await msg.reply({ embeds: [embed] });
    }
}

export default new nowplaying();
