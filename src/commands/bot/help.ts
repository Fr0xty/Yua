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
            .setAuthor({ name: 'Yuna', iconURL: Yuna.user!.displayAvatarURL() })
            .setDescription('help description');

        await msg.reply({ embeds: [embed] });
    }
}

export default new help();
