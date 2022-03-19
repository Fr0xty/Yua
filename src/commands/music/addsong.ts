import { QueryType } from 'discord-player';
import { Message, MessageEmbed, VoiceBasedChannel } from 'discord.js';
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

    async execute(msg: Message<boolean>, args: string[]) {
        /**
         * return if not setup
         */
        const isSetup = await checkSetup(msg.guildId!);
        if (!isSetup) return await msg.reply({ embeds: [Yuna.notSetupYetEmbed] });

        /**
         * get guild document
         */
        const guildDocument = Yuna.database.collection('guilds').doc(msg.guildId);
        const fetchedGuildDocument = await guildDocument.get();
        const guildDocumentData = fetchedGuildDocument.data();

        /**
         * if guild has no songs (not playing), create queue
         */
        const queue = guildDocumentData.songs.length
            ? Yuna.player.getQueue(msg.guild!)
            : Yuna.player.createQueue(msg.guild!, {
                  ytdlOptions: {
                      quality: 'highest',
                      filter: 'audioonly',
                      highWaterMark: 1 << 25,
                      dlChunkSize: 0,
                  },
                  leaveOnEnd: false,
                  leaveOnStop: false,
                  leaveOnEmpty: false,
                  initialVolume: 50,
              });
        if (!guildDocumentData.songs.length) {
            queue.setRepeatMode(2);
            queue.shuffle();
        }

        /**
         * search and add to queue
         */
        const query = args.join(' ');
        const searchResults = await Yuna.player.search(query, {
            requestedBy: msg.member!,
            searchEngine: QueryType.AUTO,
        });
        /**
         * return if no result
         */
        if (!searchResults)
            return await msg.reply(
                'Sorry, the query provided did not have any results. Please try a different link / search keyword.'
            );
        /**
         * add search result to queue && add to firebase guild songs array
         */
        const oldGuildDocumentData = JSON.parse(JSON.stringify(guildDocumentData));
        if (query.includes('http')) {
            guildDocumentData.songs.push(...searchResults.tracks.map((track) => track.url));

            queue.addTracks(searchResults.tracks);
            guildDocument.update(guildDocumentData);
        } else {
            guildDocumentData.songs.push(searchResults.tracks[0].url);

            queue.addTrack(searchResults.tracks[0]);
            guildDocument.update(guildDocumentData);
        }

        /**
         * send added song embed
         */
        const addedMoreThanOneTrack =
            guildDocumentData.songs.length - oldGuildDocumentData.songs.length === 1 ? false : true;

        const embed = addedMoreThanOneTrack
            ? new MessageEmbed()
                  .setColor(Yuna.color)
                  .setAuthor({
                      name: `Music queue for ${msg.guild!.name}`,
                      iconURL: queue.guild.iconURL() ? queue.guild.iconURL()! : Yuna.user!.displayAvatarURL(),
                  })
                  .setDescription(`Added ${searchResults.tracks.length} song.`)
            : new MessageEmbed()
                  .setColor(Yuna.color)
                  .setAuthor({
                      name: `Music queue for ${queue.guild.name}`,
                      iconURL: queue.guild.iconURL() ? queue.guild.iconURL()! : Yuna.user!.displayAvatarURL(),
                  })
                  .setThumbnail(searchResults.tracks[0].thumbnail)
                  .setTitle('Added to queue:')
                  .setDescription(`[${searchResults.tracks[0].title}](${searchResults.tracks[0].url})`);
        await msg.reply({ embeds: [embed] });

        if (!queue.playing) {
            const vc = (await Yuna.channels.fetch(guildDocumentData.voiceChannelId)) as VoiceBasedChannel;
            await queue.connect(vc);
            await queue.play();
        }
    }
}

export default new addsong();
