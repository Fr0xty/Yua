declare module 'yuna' {
    import { Message } from 'discord.js';

    export interface BaseCommand {
        name: string;
        description: string;
        aliases?: string[];
        execute(msg: Message, args: string[]): Promise<any>;
    }
}
