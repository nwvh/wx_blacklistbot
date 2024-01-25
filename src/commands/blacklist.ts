import { CommandInteraction, SlashCommandBuilder, EmbedBuilder, PermissionFlagsBits, ButtonBuilder, ButtonStyle } from "discord.js";
import {addToDB,isBlacklisted,getBlacklistReason, getBlacklistAdmin} from '../utils/blacklistHandler'
import {Locale, BlacklistedRoleID} from '../bot_config'
export const data = new SlashCommandBuilder()
  .setName("blacklist")
  .setDescription(Locale.blacklistDesc)
  .setDefaultMemberPermissions(PermissionFlagsBits.BanMembers)
  .setDMPermission(false)
  .addUserOption(option =>
    option.setName('user')
    .setRequired(true)
    .setDescription(Locale.userDesc))
  .addStringOption(option =>
    option.setName('reason')
    .setRequired(true)
    .setDescription(Locale.reasonDesc));
    

export async function execute(interaction: CommandInteraction) {
    const target = interaction.options.getUser('user');
    const reason = interaction.options.get('reason')?.value
    const userid = String(target?.id)
    const username = String(target?.username)
    
    if (!isBlacklisted(userid)) {
        const member = interaction.guild?.members.cache.get(userid);
        
        
        if (member) {
            await interaction.guild?.roles.fetch();
            const roleToAdd = interaction.guild?.roles.cache.get(BlacklistedRoleID);
            if (roleToAdd) {
              try {
                await member.roles.add(roleToAdd);
                console.log(`Role added successfully to ${username}`);
              } catch (error) {
                const permerror = new EmbedBuilder()
                .setColor("Red")
                .setDescription(`User couldn't be blacklisted! Please ensure that:\n\n- The bot has proper permissions (Manage Roles)\n- Bot's role is higher than everyone else`)
                console.error(`Error adding role to member: ${error}`);
                return await interaction.reply({
                    embeds: [permerror]
                });
              }
            } else {
                console.log('Role not found in the guild');
            }
          } else {
            console.log('Member not found in the guild');
          }
        addToDB(userid,username,String(reason),interaction.user.username)
        await interaction.guild?.roles.fetch()
        const embed = new EmbedBuilder()
        .setColor("Green")
        .setDescription(Locale.blacklisted(target,reason))

        const DMEmbed = new EmbedBuilder()
        .setColor("Red")
        .setTitle('You have been blacklisted on '+Locale.serverName)
        .setDescription(`Hello, ${target?.displayName}. You are receiving this message because you have been blacklisted from our server.\n\n**Blacklist Reason**: ${reason}\n**Blacklisted by**: @${interaction.user.username}\n\nIf you'd like to appeal, you can create a ticket. Until then you have restricted access to the server. Please note that rejoining the server or joining with another account will not help you evade the blacklist.`)
        .setImage('https://media.discordapp.net/attachments/1124446695841865792/1132029387726925895/standard.gif')
        .setTimestamp()
        .setFooter({ text: 'WX Blacklist' });
        
        try {
            target?.send({ embeds: [DMEmbed] })
            .catch(error => console.error(`[WARNING] An error occured while trying to DM ${target.username}: ${error.message}`));
                  } catch(err) {
            void err
        }
        return await interaction.reply({
            embeds: [embed]
        });
    } else {

        const embed = new EmbedBuilder()
            .setColor("Red")
            .setDescription(Locale.alreadyBlacklisted(target,getBlacklistReason(userid),getBlacklistAdmin(userid))
        )
        return await interaction.reply({
            embeds: [embed]
        });

        
    }
}