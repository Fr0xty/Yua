import { Player } from 'discord-player';
import { Client, Collection, Snowflake } from 'discord.js';

declare module 'discord.js' {
    export interface Client {
        player: Player;
        color: ColorResolvable;
        prefix: string;

        commands: Collection<string, any>;
        database: FirebaseFirestore;

        notSetupYetEmbed: MessageEmbed;
        utils: any;
    }
}
