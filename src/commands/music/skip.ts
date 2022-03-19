import { Message } from 'discord.js';
import { BaseCommand } from 'yuna';
import { Yuna } from '../../config.js';
import { checkSetup } from '../../utils.js';

class skip implements BaseCommand {
    name: string;
    description: string;

    constructor() {
        this.name = 'skip';
        this.description = 'skip current song.';
    }

    async execute(msg: Message<boolean>, args: string[]) {
        /**
         * return if not setup
         */
        const isSetup = await checkSetup(msg.guildId!);
        if (!isSetup) return await msg.reply({ embeds: [Yuna.notSetupYetEmbed] });

        const queue = Yuna.player.getQueue(msg.guild!);

        if (!queue)
            return await msg.reply(
                'There is no song in serverplaylist, add songs using `yuna addsong <url/keywords>`.'
            );
        queue.skip();
    }
}

export default new skip();
