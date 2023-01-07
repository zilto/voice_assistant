# Voice assistant
Use your microphone to launch arbitrary Python functions

## Description
This project leverages the multilingual speech-to-text model *Whisper* from OpenAI. The model is loaded on a websocket server. The connected client sends an audio input stream and receives text transcriptions. If the predefined *keyword* is found, the following words are parsed to find a *registered command* using fuzzy matching. If there's a match, the command is executed on the client device.

A *command* is an arbitrary Python function. The name of function (separated by underscores `_`) is what needs to be uttered to trigger the command. Words spoken after the command name are parsed as function arguments. Additional commands can be written to Python modules (`.py`file) and multiple modules

## Design choices
- client-server architecture: allows a client with limited resources to leverage speech-to-text (smartphone, remote, dev board). Clients can share a server, and a client could potentially trigger commands on another client.
- structured commands: the opiniated structure removes the problem of natural language understanding, which allows for faster development of new commands
- modular commands: the modular organization of commands allows to ship a core app without bloating, and to make user-created commands easy to share
- few dependencies: thefuzz is a quality of life and could be reimplemented; the SpeechRecognition is a bit messy, but has nice features to ignore ambient noise