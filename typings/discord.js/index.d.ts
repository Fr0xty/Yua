import { Player } from 'discord-player';
import { Client } from 'discord.js';

declare module 'discord.js' {
    export interface Client {
        player: Player;
        color: ColorResolvable;
    }
}
