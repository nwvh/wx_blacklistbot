export const BotToken = "BOTTOKEN"; // Your Bot's token
export const ClientID = "CLIENTID"; // Your Bot's client ID
export const GuildID = "GUILDID"; // ID of the guild you want to use the bot in
  
export const BlacklistedRoleID = "ROLEID"; // ID of the blacklisted role that will be added to users in blacklist

// Locale settings
export const Locale = {
    serverName: "EXAMPLE SERVER",


    blacklistDesc: "Adds selected user to the blacklist",
    userDesc: "User that you want to blacklist",
    reasonDesc: "Reason for the blacklist",
    blacklisted: (user: any, reason: any) => `User ${user} has been blacklisted for: **${reason}**`,
    alreadyBlacklisted: (user: any, reason: any, admin: any) => `User ${user} has already been blacklisted for: **${reason}** (${admin})`,

    // more localization soon
}