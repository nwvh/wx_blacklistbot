import { Client } from "discord.js";
import {isBlacklisted} from '../utils/blacklistHandler'
import {BlacklistedRoleID} from '../bot_config'

export default (client: Client): void => {

    client.on('guildMemberAdd', (member) => {
        console.log('Member joined:', member.user.tag);
    
        const guild = member.guild;
        const roleToAdd = guild.roles.cache.get(BlacklistedRoleID);
    
        if (isBlacklisted(member.user.id)) {
            console.log('User is blacklisted');
    
            if (roleToAdd) {
                console.log('Role to add found:', roleToAdd.name);
    
                member.roles.add(roleToAdd)
                    .then(() => {
                        console.log(`Added role ${roleToAdd.name} to ${member.user?.tag}`);
                    })
                    .catch((error) => {
                        console.error(`Error adding role to member: ${error}`);
                    });
            } else {
                console.error(`Role with ID ${BlacklistedRoleID} not found in the guild`);
            }
        }
    });
}