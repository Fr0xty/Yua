import { GuildMember, Message, MessageActionRow, MessageButton, MessageEmbed, VoiceBasedChannel } from 'discord.js';
import { BaseCommand } from 'yuna';
import { Yuna } from '../../config.js';
import { checkSetup } from '../../utils.js';

class changevc implements BaseCommand {
    name: string;
    description: string;

    constructor() {
        this.name = 'changevc';
        this.description = 'change server vc where I will play songs.';
    }

    async execute(msg: Message<boolean>, args: string[]) {
        /**
         * return if not setup
         */
        const isSetup = await checkSetup(msg.guildId!);
        if (!isSetup) return await msg.reply({ embeds: [Yuna.notSetupYetEmbed] });

        /**
         * resetup voice channel
         */
        let vc: VoiceBasedChannel;
        let embed = new MessageEmbed()
            .setColor(Yuna.color)
            .setTitle('Resetup voice channel')
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
            try {
                await vcSetupEmbed.delete();
            } catch {}

            if (reason !== 'selected') {
                await msg.reply('You took too long! Please do `yuna changevc` again when you made up your mind.');
                return;
            }

            /**
             * change vc in firebase
             */
            const guildDocument = Yuna.database.collection('guilds').doc(msg.guildId);
            const guildDocumentData = await guildDocument.get();

            guildDocumentData.voiceChannelId = vc;
            await guildDocument.update(guildDocumentData);

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
            await msg.react(Yuna.okEmoji);
        });
    }
}

export default new changevc();
