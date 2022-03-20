import { QueryType, Track } from 'discord-player';
import { VoiceBasedChannel } from 'discord.js';
import { ByteLengthQueuingStrategy } from 'node:stream/web';
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
        const guildDocumentSnapshot: FirebaseFirestore.QueryDocumentSnapshot = guilds[i];
        const guildId = guildDocumentSnapshot.id;
        const guildDocument = Yuna.database.collection('guilds').doc(guildId);
        const guildDocumentData = guildDocumentSnapshot.data()!;

        /**
         * if theres no songs in serverplaylist skip
         */
        if (!guildDocumentData.songs.length) continue;

        /**
         * create server queue and add tracks to queue
         */
        const queue = Yuna.player.createQueue(await Yuna.guilds.fetch(guildId), {
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

        const oldSongDataLength = guildDocumentData.songs.length;
        const searchResults: Track[] = [];
        for (const songURL of guildDocumentData.songs) {
            const search = await Yuna.player.search(songURL, {
                requestedBy: Yuna.user!, // dummy data to avoid typescript screaming at me
                searchEngine: QueryType.AUTO,
            });
            /**
             * remove faulty links with no results
             */
            if (!search.tracks.length) {
                guildDocumentData.songs.splice(guildDocumentData.songs.indexOf(songURL), 1);
                continue;
            }
            searchResults.push(search.tracks[0]);
        }
        /**
         * add all searched tracks
         */
        queue.addTracks(searchResults);
        /**
         * if found faulty links, update to firebase
         */
        if (oldSongDataLength !== guildDocumentData.songs.length) await guildDocument.update(guildDocumentData);

        /**
         * play forever and shuffle on start
         */
        queue.setRepeatMode(2);
        queue.shuffle();

        /**
         * join vc and start playing
         */
        const vc = (await Yuna.channels.fetch(guildDocumentData.voiceChannelId)) as VoiceBasedChannel;
        await queue.connect(vc);
        await queue.play();
    }
});
