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
        if (query.includes('http')) {
            queue.addTracks(searchResults.tracks);
            guildDocumentData.songs.push(...searchResults.tracks.map((track) => track.url));
            guildDocument.update(guildDocumentData);
        } else {
            queue.addTrack(searchResults.tracks[0]);
            guildDocumentData.songs.push(searchResults.tracks[0].url);
            guildDocument.update(guildDocumentData);
        }

        if (!queue.playing) {
            const vc = (await Yuna.channels.fetch(guildDocumentData.voiceChannelId)) as VoiceBasedChannel;
            await queue.connect(vc);
            await queue.play();
        }
    }
}

export default new addsong();
