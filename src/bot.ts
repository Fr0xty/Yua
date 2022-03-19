import 'dotenv/config';
import fs from 'fs';
import { Yuna } from './config.js';

const events = fs.readdirSync('./dist/events');
events.forEach(async (event) => {
    await import(`./events/${event}`);
});

const commandCategories = fs.readdirSync('./dist/commands');
commandCategories.forEach((category) => {
    const commands = fs.readdirSync(`./dist/commands/${category}`);
    commands.forEach(async (command) => {
        const { default: importCommand } = await import(`./commands/${category}/${command}`);

        Yuna.commands.set(importCommand.name, importCommand);
        if (importCommand.aliases)
            importCommand.aliases.forEach((alias: string) => {
                Yuna.commands.set(alias, importCommand);
            });
    });
});

import './server.js';
Yuna.login(process.env.TOKEN);
