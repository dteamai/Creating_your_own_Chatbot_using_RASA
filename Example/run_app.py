from rasa_core.agent import Agent
from rasa_core.channels.channel import InputChannel
from rasa_core.channels.slack import SlackInput
from rasa_core.interpreter import RasaNLUHttpInterpreter
from rasa_core.utils import EndpointConfig
import yaml

# load your trained agent
MODEL_PATH = './models/dialogue'
action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
agent = Agent.load(MODEL_PATH, interpreter=RasaNLUHttpInterpreter('./models/nlu/default/weathernlu',action_endpoint),action_endpoint=action_endpoint)

input_channel = SlackInput("xoxb-510293626996-511519984071-kL4oH87tyMDYvyY0W04TmkuM"
                            ,True)
        # this is the `bot_user_o_auth_access_token`
        
        # the name of your channel to which the bot posts (optional)


# set serve_forever=True if you want to keep the server running
s = agent.handle_channels([input_channel], serve_forever=True)
