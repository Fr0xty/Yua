import { Yuna } from '../config.js';

Yuna.on('messageCreate', async (msg): Promise<any> => {
    if (!msg.content.startsWith(Yuna.prefix) || msg.author.bot) return;

    const prefixlessMsg = msg.content.slice(Yuna.prefix.length);
    if (!prefixlessMsg) return;

    const commandName = prefixlessMsg.split(/ +/)[0];
    const args = prefixlessMsg.slice(commandName.length).trim().split(/ +/);

    const command = Yuna.commands.get(commandName);
    if (!command)
        return await msg.reply(`No command named \`${commandName}\` found. Please use \`yuna help\` for help.`);

    try {
        await command.execute(msg, args);
    } catch (err) {
        await msg.reply(String(err));
        console.log(err);
    }
});
