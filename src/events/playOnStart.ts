import { QueryType, Track } from 'discord-player';
import { VoiceBasedChannel } from 'discord.js';
import { Yuna } from '../config.js';

/**
 * to start playing in guilds on ready
 */
Yuna.on('ready', async () => {
    /**
     * get every guild registered in firebase
     */
    const { docs: guilds } = await Yuna.database.collection('guilds').get();

    for (let i = 0; i < guilds.length; i++) {
        /**
         * if theres no songs in serverplaylist skip
         */
        const data = guilds[i].data()!;
        if (!data.songs.length) continue;

        /**
         * create server queue and add tracks to queue
         */
        const queue = Yuna.player.createQueue(await Yuna.guilds.fetch(guilds[i].id), {
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
        const searchResults: Track[] = [];
        for (const songURL of data.songs) {
            const search = await Yuna.player.search(songURL, {
                requestedBy: Yuna.user!, // dummy data to avoid typescript screaming at me
                searchEngine: QueryType.AUTO,
            });
            searchResults.push(search.tracks[0]);
        }
        queue.addTracks([...searchResults]);

        /**
         * join vc and start playing
         */
        const vc = (await Yuna.channels.fetch(data.voiceChannelId)) as VoiceBasedChannel;
        await queue.connect(vc);
        await queue.play();
    }
});
