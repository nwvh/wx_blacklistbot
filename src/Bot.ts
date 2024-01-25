import {BotToken, GuildID, BlacklistedRoleID} from './bot_config'
import { Client, ClientOptions } from "discord.js";
import ready from "./listeners/ready";
import { deployCommands } from "./deployCommands";
import { commands } from "./commands";
import { isBlacklisted } from './utils/blacklistHandler';


const client = new Client({
  intents: [
    'Guilds',
    'GuildMembers',
  ],
});
ready(client)
// onJoin(client)
deployCommands({ guildId: GuildID });

client.on("interactionCreate", async (interaction) => {
    if (!interaction.isCommand()) {
      return;
    }
    const { commandName } = interaction;
    if (commands[commandName as keyof typeof commands]) {
      commands[commandName as keyof typeof commands].execute(interaction);
    }
  });
client.login(BotToken);