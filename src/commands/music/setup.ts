import {
    GuildMember,
    Message,
    MessageActionRow,
    MessageButton,
    MessageEmbed,
    VoiceBasedChannel,
    VoiceChannel,
} from 'discord.js';
import { BaseCommand } from 'yuna';
import { Yuna } from '../../config.js';
import { checkSetup } from '../../utils.js';

class setup implements BaseCommand {
    name: string;
    description: string;

    constructor() {
        this.name = 'setup';
        this.description = 'to set me up in your server.';
    }

    async execute(msg: Message<boolean>, args: string[]) {
        /**
         * return if already setup
         */
        const isSetup = await checkSetup(msg.guildId!);
        if (isSetup) return await msg.reply('Server is already setup!');

        let vc: VoiceBasedChannel;
        /**
         * setup vc
         */
        let embed = new MessageEmbed()
            .setColor(Yuna.color)
            .setTitle('Setup voice channel')
            .setDescription(
                `
Please join the voice channel you want me to play music in, and click on the button.

__Timeout in 1 minute__
            `
            )
            .setAuthor({ name: Yuna.user!.username, iconURL: Yuna.user!.displayAvatarURL() });

        const vcSetupEmbed = await msg.reply({
            embeds: [embed],
            components: [
                new MessageActionRow().addComponents(
                    new MessageButton().setCustomId('selectVC').setEmoji('885845968048779304').setStyle('SUCCESS')
                ),
            ],
        });
        const collector = vcSetupEmbed.createMessageComponentCollector({ time: 60_000 });
        collector.on('collect', async (i) => {
            /**
             * not author
             */
            if (i.user.id !== msg.author.id) {
                await i.reply('Only the one that invoked this command can choose the voice channel!');
                return;
            }
            /**
             * author is not in a vc
             */
            const memberVC = (i.member as GuildMember).voice.channel;
            if (!memberVC) {
                await i.reply('Please join a voice channel first then click the button.');
                return;
            }
            /**
             * author selected a vc
             */
            vc = memberVC;
            collector.stop('selected');
        });
        collector.on('end', async (collected, reason) => {
            await vcSetupEmbed.delete();
            if (reason !== 'selected') {
                await msg.reply('You took too long! Please do `yuna setup` again when you made up your mind.');
                return;
            }

            /**
             * register gulid into firebase
             */
            await Yuna.database.collection('guilds').doc(msg.guildId).set({
                voiceChannelId: vc.id,
                songs: [],
            });

            embed = new MessageEmbed()
                .setTitle('Your server has been successfully setup!')
                .setColor(Yuna.color)
                .setDescription(
                    `
From now on I will be playing in <#${vc.id}>!

Please add songs to the server playlist using the \`addsong\` command!
                `
                )
                .setTimestamp();
            await msg.reply({ embeds: [embed] });
            await msg.react('918494275728179251');
        });
    }
}

export default new setup();
