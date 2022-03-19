import { Snowflake, Message, MessageActionRow, MessageButton, MessageEmbed } from 'discord.js';
import { Yuna } from './config.js';

export const checkSetup = async (guildId: Snowflake) => {
    const fetchedGuild = await Yuna.database.collection('guilds').doc(guildId).get();
    if (fetchedGuild.exists) return true;
    return false;
};

/**
 * paginator
 */
const _aquaButtons = new MessageActionRow().addComponents(
    new MessageButton().setCustomId('pageLeft').setEmoji('879530551038603264').setStyle('SECONDARY'),
    new MessageButton().setCustomId('pageRight').setEmoji('879530551881637930').setStyle('SECONDARY')
);

export const paginator = async (msg: Message, pages: MessageEmbed[], timeout: number) => {
    if (pages.length === 1) return await msg.channel.send({ embeds: [pages[0]] });

    let currentPage = 0;
    const sentMsg = await msg.channel.send({ embeds: [pages[currentPage]], components: [_aquaButtons] });
    const collector = sentMsg.createMessageComponentCollector({ idle: timeout, dispose: true });
    collector.on('collect', async (i) => {
        if (i.customId === 'pageLeft' && currentPage !== 0) currentPage--;
        else if (i.customId === 'pageRight' && currentPage !== pages.length - 1) currentPage++;
        else if (i.customId === 'pageLeft' && currentPage === 0) currentPage = pages.length - 1;
        else if (i.customId === 'pageRight' && currentPage === pages.length - 1) currentPage = 0;

        await sentMsg.edit({ embeds: [pages[currentPage]] });
        await i.deferUpdate();
    });
    collector.on('end', async (collected) => {
        try {
            await msg.react(Yuna.okEmoji);
            await sentMsg.edit({ components: [] });
        } catch {}
    });
};
