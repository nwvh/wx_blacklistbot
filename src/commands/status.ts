import { CommandInteraction, SlashCommandBuilder, EmbedBuilder, PermissionFlagsBits, ButtonBuilder, ButtonStyle } from "discord.js";
import {removeFromDB,isBlacklisted, getBlacklistReason, getBlacklistAdmin} from '../utils/blacklistHandler'
import {Locale} from '../bot_config'
export const data = new SlashCommandBuilder()
  .setName("status")
  .setDescription("Check if user is blacklisted")
  .setDefaultMemberPermissions(PermissionFlagsBits.BanMembers)
  .setDMPermission(false)
  .addUserOption(option =>
    option.setName('user')
    .setRequired(true)
    .setDescription("User you want to check"))
    

export async function execute(interaction: CommandInteraction) {
    const target = interaction.options.getUser('user');
    const userid = String(target?.id)
    const blReason = getBlacklistReason(userid)
    if (!isBlacklisted(userid)) {
        const embed = new EmbedBuilder()
        .setColor("Red")
        .setDescription(`${target} is not blacklisted.`)
        return await interaction.reply({
            embeds: [embed]
        });
    } else {
        const embed = new EmbedBuilder()
        .setColor("Red")
        .setDescription(`${target} has been blacklisted by ${getBlacklistAdmin(userid)} for ${blReason}`)
        return await interaction.reply({
            embeds: [embed]
        });
        
    }
}