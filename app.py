import os
import time
from slackclient import SlackClient
from source import exchange
from util import parse_slack_output,handle_error

# Constant variables
EXAMPLE_COMMAND = "환율"
BOT_NAME = "parrot-bot"

sc = SlackClient(os.environ["SLACK_API_TOKEN"])

def exchange_model(command):
    if command and command.startswith("환율"):
        return "exchange"
    return None
        
models = [ exchange_model ]
parrots = [ exchange.ExchangeParrot(sc) ] 
parrot_cage = {}
for parrot in parrots:
    parrot_cage[parrot.NAME] = parrot.generate_actor()

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if sc.rtm_connect():
        print("Parrot-Bot connected and running!")
        while True:
            command, channel = parse_slack_output(sc.rtm_read())
            success = 0 # if all model failed, command is not valid
            for model in models:
                if model(command):
                    parrot_cage[model(command)](command,channel)
                    success += 1
            if command and success == 0: # if command is '', handle_error wouldn't be executed
                handle_error(sc)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID")
