import { CommandInteraction, SlashCommandBuilder, EmbedBuilder, PermissionFlagsBits, ButtonBuilder, ButtonStyle } from "discord.js";
import {removeFromDB,isBlacklisted, getBlacklistReason} from '../utils/blacklistHandler'
import {Locale, BlacklistedRoleID} from '../bot_config'
export const data = new SlashCommandBuilder()
  .setName("unblacklist")
  .setDescription("Remove user from blacklist")
  .setDefaultMemberPermissions(PermissionFlagsBits.BanMembers)
  .setDMPermission(false)
  .addUserOption(option =>
    option.setName('user')
    .setRequired(true)
    .setDescription("User you want to remove. You can both mention the user or use User ID"))
    

export async function execute(interaction: CommandInteraction) {
    const target = interaction.options.getUser('user');
    const userid = String(target?.id)
    const blReason = getBlacklistReason(userid)
    if (!isBlacklisted(userid)) {
        const confirm = new ButtonBuilder()
        .setCustomId('confirm')
        .setLabel('Remove Blacklist')
        .setStyle(ButtonStyle.Danger);
        const embed = new EmbedBuilder()
        .setColor("Red")
        .setDescription(`${target} is not in blacklist.`)
        return await interaction.reply({
            embeds: [embed]
        });
    } else {
        removeFromDB(userid)
        if (!isBlacklisted(userid)) {
            const roleToRemove = interaction.guild?.roles.cache.get(BlacklistedRoleID);
            const member = interaction.guild?.members.cache.get(userid);
            if (member && roleToRemove) {
                await member.roles.remove(roleToRemove);
            }
            const embed = new EmbedBuilder()
            .setColor("Red")
            .setDescription(`${target} has been removed from the blacklist!`)
            const DMEmbed = new EmbedBuilder()
            .setColor("Green")
            .setTitle('Your blacklist on '+Locale.serverName+ ' has been removed')
            .setDescription(`Hello, ${target?.displayName}. You are receiving this message because your blacklist on our server has been removed.\n\n**Blacklist Reason**: ${blReason}\n**Removed by**: @${interaction.user.username}\n\nYou now have access back to the server.`)
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
            .setDescription(`${target} couldn't be removed from the blacklist!`)
        return await interaction.reply({
            embeds: [embed]
        });
        }
        
    }
}