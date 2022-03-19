import { Message, MessageEmbed } from 'discord.js';
import { BaseCommand } from 'yuna';
import { Yuna } from '../../config.js';
import { checkSetup } from '../../utils.js';

class addsong implements BaseCommand {
    name: string;
    description: string;

    constructor() {
        this.name = 'addsong';
        this.description = 'add song to server playlist.';
    }

    async execute(msg: Message<boolean>, args: string[]) {}
}

export default new addsong();
