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

        /**
         * return if no song in serverplaylist
         */
        const queue = Yuna.player.getQueue(msg.guild!);
        if (!queue)
            return await msg.reply(
                'There is no song in serverplaylist, add songs using `yuna addsong <url/keywords>`.'
            );

        const [skipToNumberString] = args;
        if (!skipToNumberString) {
            queue.skip();
            return await msg.react(Yuna.okEmoji);
        }

        /**
         * provided index to skip to
         */
        const skipToNumber = Number(skipToNumberString);
        if (isNaN(skipToNumber))
            return await msg.reply(
                `\`${skipToNumberString}\` is not a number! please check by doing \`yuna serverplaylist\`.`
            );
        if (skipToNumber < 2 || skipToNumber > queue.tracks.length + 1)
            return await msg.reply('That is not a valid song index, please check by doing `yuna serverplaylist`.');

        const skipToNumberIndex = skipToNumber - 2;
        queue.tracks = queue.tracks.concat(queue.tracks.splice(0, skipToNumberIndex - 1));
        queue.skip();
        await msg.react(Yuna.okEmoji);
    }
}

export default new skip();
