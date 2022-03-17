import { Message, MessageEmbed } from 'discord.js';
import { BaseCommand } from 'yuna';
import { Yuna } from '../../config.js';

class evaluation implements BaseCommand {
    name: string;
    description: string;

    constructor() {
        this.name = 'eval';
        this.description = 'run code in discord.';
    }

    async execute(msg: Message<boolean>, args: string[]): Promise<any> {
        if (msg.author.id !== '395587171601350676') return;
        let script = args.join(' ').trim();

        if (msg.author.id !== '395587171601350676') return;
        if (script.startsWith('```') && script.endsWith('```')) script = script.replace(/(^.*?\s)|(\n.*$)/g, '');

        try {
            // @ts-ignore
            let result = eval(`(async () => {${script}})()`);
        } catch (err) {
            console.log(err);
            // @ts-ignore
            await msg.reply(err.message);
        }
    }
}

export default new evaluation();
