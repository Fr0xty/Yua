import { Message, MessageEmbed } from 'discord.js';
import { BaseCommand } from 'yuna';
import { Yuna } from '../../config.js';

class help implements BaseCommand {
    name: string;
    description: string;

    constructor() {
        this.name = 'help';
        this.description = 'get info on my commands.';
    }

    async execute(msg: Message<boolean>, args: string[]): Promise<any> {
        const embed = new MessageEmbed()
            .setColor(Yuna.color)
            .setFooter({ text: '<args> are required, [args] are optional.' })
            .setAuthor({ name: 'Yuna', iconURL: Yuna.user!.displayAvatarURL() }).setDescription(`
I host **24 hour** music channels! I'm only in a *few selected servers*.
My prefix is \`yuna\`
Github Repo: https://github.com/Fr0xty/Yuna

\`setup\`
To setup me in the server

\`serverreset\` • reset the whole server's settings (irreversible)
\`addsong <url>\` • add song to serverplaylist
\`remsong <index>\` • remove song from serverplaylist
\`changevc\` • change which voice channel I will be playing in
\`serverplaylist\` \`sp\` • view serverplaylist
\`clearplaylist\` • reset serverplaylist (irreversible)
\`vc\` • get which voice channel I'm playing in
\`nowplaying\` \`np\` • view current playing song
\`skip [skip_to_index]\` • skip current song
\`shuffle\` • shuffle the serverplaylist
\`queue\` \`q\` • view current song queue
            `);

        await msg.reply({ embeds: [embed] });
    }
}

export default new help();
