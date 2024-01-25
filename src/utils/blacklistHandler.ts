import * as fs from 'fs';

interface BlacklistEntry {
  userid: string;
  username: string;
  reason: string;
  admin: string;
}

interface Database {
  blacklist: BlacklistEntry[];
}

export function writeToDB(blacklist: BlacklistEntry, filename: string = './db/blacklists.json'): void {
  const fileData: Database = JSON.parse(fs.readFileSync(filename, 'utf-8'));
  fileData.blacklist.push(blacklist);
  fs.writeFileSync(filename, JSON.stringify(fileData, null, 4));
}

export function addToDB(userid: string, username: string, reason: string, admin: string): boolean {
  if (!isBlacklisted(userid)) {
    const blacklist: BlacklistEntry = {
      userid: `${userid}`,
      username: `${username}`,
      reason: `${reason}`,
      admin: `${admin}`,
    };
    writeToDB(blacklist);
    return true;
  } else {
    return false;
  }
}

export function removeFromDB(userid: string): void {
  const fileData: Database = JSON.parse(fs.readFileSync('./db/blacklists.json', 'utf-8'));
  const toSearch = [`${userid}`] || [userid];
  fileData.blacklist = fileData.blacklist.filter((element) => !toSearch.includes(element.userid));

  fs.writeFileSync('./db/blacklists.json', JSON.stringify(fileData, null, 4));
}

export function clearDB(): boolean {
  const usersCount = blacklistedUsers();
  if (usersCount >= 1) {
    const fileData: Database = JSON.parse(fs.readFileSync('./db/blacklists.json', 'utf-8'));
    const backupFilename = `backups/database-BACKUP-${Math.floor(Math.random() * 8888) + 1111}.json`;

    fs.writeFileSync(backupFilename, JSON.stringify(fileData, null, 4));

    fs.writeFileSync('./db/blacklists.json', JSON.stringify({ blacklist: [] }, null, 4));
    log('success', 'Database has been cleared!');
    return true;
  } else {
    return false;
  }
}

export function blacklistedUsers(): number {
  const fileData: Database = JSON.parse(fs.readFileSync('./db/blacklists.json', 'utf-8'));
  return fileData.blacklist.length;
}

export function isBlacklisted(userid: string): boolean {
  const fileData: Database = JSON.parse(fs.readFileSync('./db/blacklists.json', 'utf-8'));
  const toSearch = [`${userid}`] || [userid];
  return fileData.blacklist.some((element) => toSearch.includes(element.userid));
}

export function getBlacklistReason(userid: string): string | undefined {
  const fileData: Database = JSON.parse(fs.readFileSync('./db/blacklists.json', 'utf-8'));
  const toSearch = [`${userid}`] || [userid];
  const entry = fileData.blacklist.find((element) => toSearch.includes(element.userid));
  return entry ? entry.reason : undefined;
}

export function getBlacklistAdmin(userid: string): string | undefined {
  const fileData: Database = JSON.parse(fs.readFileSync('./db/blacklists.json', 'utf-8'));
  const toSearch = [`${userid}`] || [userid];
  const entry = fileData.blacklist.find((element) => toSearch.includes(element.userid));
  return entry ? entry.admin : undefined;
}
export function log(level: string, message: string): void {
    console.log(`[${level.toUpperCase()}] ${message}`);
  }