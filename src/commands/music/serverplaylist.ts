import { Message, MessageEmbed } from 'discord.js';
import { BaseCommand } from 'yuna';
import { Yuna } from '../../config.js';
import { checkSetup, paginator } from '../../utils.js';

class serverplaylist implements BaseCommand {
    name: string;
    description: string;
    aliases: string[];

    constructor() {
        this.name = 'serverplaylist';
        this.description = 'get serverplaylist.';
        this.aliases = ['sp'];
    }

    async execute(msg: Message<boolean>, args: string[]) {
        /**
         * return if not setup
         */
        const isSetup = await checkSetup(msg.guildId!);
        if (!isSetup) return await msg.reply({ embeds: [Yuna.notSetupYetEmbed] });

        const queue = Yuna.player.getQueue(msg.guild!);

        /**
         * return if no song in serverplaylist
         */
        if (!queue)
            return await msg.reply(
                'There is no song in serverplaylist, add songs using `yuna addsong <url/keywords>`.'
            );

        /**
         * only 1 song in queue
         */
        if (!queue.tracks.length) {
            const embed = new MessageEmbed()
                .setColor(Yuna.color)
                .setAuthor({
                    name: `Music queue for ${queue.guild.name}`,
                    iconURL: queue.guild.iconURL() ? queue.guild.iconURL()! : Yuna.user!.displayAvatarURL(),
                })
                .setTitle('Now Playing:')
                .setDescription(
                    `
[${queue.nowPlaying().title}](${queue.nowPlaying().url}) - \`${queue.nowPlaying().duration}\`
no more songs in queue...
                `
                )
                .setFooter({ text: `Requested by ${msg.author.tag}`, iconURL: msg.author.displayAvatarURL() })
                .setTimestamp();
            return await msg.reply({ embeds: [embed] });
        }

        /**
         * paginator
         */
        let songNum = 2;
        let page = `[${queue.nowPlaying().title}](${queue.nowPlaying().url})\n\n`;
        const pages: MessageEmbed[] = [];
        queue.tracks.forEach((track) => {
            page += `**${songNum++}.** [${track.title}](${track.url})\n`;

            if (songNum % 15 === 0) {
                const embed = new MessageEmbed()
                    .setColor(Yuna.color)
                    .setAuthor({
                        name: `Music queue for ${queue.guild.name} | Page ${pages.length + 1} / ${Math.ceil(
                            (queue.tracks.length + 1) / 15
                        )}`,
                        iconURL: queue.guild.iconURL() ? queue.guild.iconURL()! : Yuna.user!.displayAvatarURL(),
                    })
                    .setDescription(page)
                    .setTimestamp()
                    .setFooter({ text: `Requested by ${msg.author.tag}`, iconURL: msg.author.displayAvatarURL() });
                if (!pages.length) embed.setTitle('Now Playing:');

                pages.push(embed);
                page = '';
            }
        });
        if (page) {
            const embed = new MessageEmbed()
                .setColor(Yuna.color)
                .setAuthor({
                    name: `Music queue for ${queue.guild.name} | Page ${pages.length + 1} / ${Math.ceil(
                        (queue.tracks.length + 1) / 15
                    )}`,
                    iconURL: queue.guild.iconURL() ? queue.guild.iconURL()! : Yuna.user!.displayAvatarURL(),
                })
                .setDescription(page)
                .setTimestamp()
                .setFooter({ text: `Requested by ${msg.author.tag}`, iconURL: msg.author.displayAvatarURL() });
            if (!pages.length) embed.setTitle('Now Playing:');

            pages.push(embed);
        }
        await paginator(msg, pages, 120_000);
    }
}

export default new serverplaylist();
