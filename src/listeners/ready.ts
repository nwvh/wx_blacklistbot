import { Client } from "discord.js";
import {blacklistedUsers} from '../utils/blacklistHandler'
const textColor = {
    reset: '\x1b[0m',
    bright: '\x1b[1m',
    dim: '\x1b[2m',
    underscore: '\x1b[4m',
    blink: '\x1b[5m',
    reverse: '\x1b[7m',
    hidden: '\x1b[8m',
    
    black: '\x1b[30m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    magenta: '\x1b[35m',
    cyan: '\x1b[36m',
    white: '\x1b[37m',
  };
export default (client: Client): void => {
    client.on("ready", async () => {
        if (!client.user || !client.application) {
            return;
        }
        client.user.setPresence({ activities: [{ name: `with ${blacklistedUsers}` }], status: 'idle' });   
        console.log(`
        ${textColor.red}
        db   d8b   db db    db      d8888b. db       .d8b.   .o88b. db   dD db      d888888b .d8888. d888888b 
        88   I8I   88 \`8b  d8'      88  \`8D 88      d8' \`8b d8P  Y8 88 ,8P' 88        \`88'   88'  YP \`~~88~~' 
        88   I8I   88  \`8bd8'       88oooY' 88      88ooo88 8P      88,8P   88         88    \`8bo.      88    
        Y8   I8I   88  .dPYb.       88~~~b. 88      88~~~88 8b      88\`8b   88         88      \`Y8b.    88    
        \`8b d8'8b d8' .8P  Y8.      88   8D 88booo. 88   88 Y8b  d8 88 \`88. 88booo.   .88.   db   8D    88    
         \`8b8' \`8d8'  YP    YP      Y8888P' Y88888P YP   YP  \`Y88P' YP   YD Y88888P Y888888P \`8888Y'    YP    
         ${textColor.reset}                                                                                                                                                                              
        `);
        console.log(`Logged in as ${client.user.username}!`);
    });
    // client.on("guildMemberAdd", async (member:any) => {
    // });
};