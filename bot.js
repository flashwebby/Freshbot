const Discord = require('discord.js');
const axios = require('axios');
const { token, geminiApiKey, geminiModel } = require('./config.json');
const maxTokens = 32768;

const client = new Discord.Client({ intents: ["GUILDS", "GUILD_MESSAGES"] });

client.once('ready', () => {
    console.log('Ready!');
});

client.on('messageCreate', async message => {
    if (!message.content.startsWith('/') || message.author.bot) return;

    const args = message.content.slice(1).trim().split(/ +/);
    const command = args.shift().toLowerCase();

    if (command === 'summarize') {
        try {
            const messages = await fetchMessages(message.channel, 3);
            const text = messages.join(" ");
            const summary = await summarizeText(text);
            message.channel.send(summary);
        } catch (error) {
            console.error(error);
            message.channel.send('An error occurred while trying to summarize the messages.');
        }
    }
});

async function fetchMessages(channel, durationHours) {
    const afterTime = new Date(Date.now() - durationHours * 60 * 60 * 1000);
    let messages = [];
    let lastID;

    while (true) {
        const fetchedMessages = await channel.messages.fetch({ limit: 100, before: lastID });
        messages = messages.concat(fetchedMessages.map(msg => msg.content));
        lastID = fetchedMessages.last().id;

        if (fetchedMessages.size != 100 || new Date(fetchedMessages.last().createdTimestamp) < afterTime) break;
    }

    return messages;
}

async function summarizeText(text) {
    if (!text.trim()) return "No relevant information found in the specified duration.";
    if (text.length > maxTokens) return `The input text exceeds the maximum token limit of ${maxTokens} tokens. Please try summarizing a shorter duration.`;

    const url = `https://generativelanguage.googleapis.com/v1beta/models/${geminiModel}:generateContent?key=${geminiApiKey}`;
    const headers = { "Content-Type": "application/json" };
    const payload = { contents: [{ parts: [{ text }] }] };

    try {
        const response = await axios.post(url, payload, { headers });
        const data = response.data;
        return data.candidates[0].content.parts[0].text;
    } catch (error) {
        console.error(error);
        return 'Failed to summarize the text.';
    }
}

client.login(token);
