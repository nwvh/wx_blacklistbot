import { CommandInteraction, SlashCommandBuilder, EmbedBuilder, PermissionFlagsBits, ButtonBuilder, ButtonStyle } from "discord.js";
import {removeFromDB,isBlacklisted, getBlacklistReason, getBlacklistAdmin, blacklistedUsers} from '../utils/blacklistHandler'
import {Locale} from '../bot_config'
export const data = new SlashCommandBuilder()
  .setName("blacklisted")
  .setDescription("Check how many users are blacklisted")
  .setDefaultMemberPermissions(PermissionFlagsBits.BanMembers)
  .setDMPermission(false)
    

export async function execute(interaction: CommandInteraction) {
        const users = blacklistedUsers()

        if (users == 1) {
            const embed = new EmbedBuilder()
            .setColor("Blue")
            .setDescription(`There is **1** user in blacklist.`)
            return await interaction.reply({
                embeds: [embed]
            });
        } else if (users > 1) {
            const embed = new EmbedBuilder()
            .setColor("Blue")
            .setDescription(`There are **${users}** user in blacklist.`)
            return await interaction.reply({
                embeds: [embed]
            });
        } else if (users == 0) {
            const embed = new EmbedBuilder()
            .setColor("Blue")
            .setDescription(`No one is blacklisted.`)
            return await interaction.reply({
                embeds: [embed]
            });
        }
        
}