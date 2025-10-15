/**
 * Appwrite SDK configuration
 */

import { Client, Storage } from 'appwrite';

const client = new Client();

const endpoint = import.meta.env.VITE_APPWRITE_ENDPOINT || 'https://fra.cloud.appwrite.io/v1';
const projectId = import.meta.env.VITE_APPWRITE_PROJECT_ID || '68eed0ee0033a7ceca80';

client
  .setEndpoint(endpoint)
  .setProject(projectId);

export const storage = new Storage(client);

export { client };
