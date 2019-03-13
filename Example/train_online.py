from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from rasa_core.run import create_http_input_channels

import logging
from rasa_core.agent import Agent
from rasa_core.training import interactive
# from rasa_core.core.interpreter import  RegexInterpreter
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.utils import EndpointConfig
from rasa_core.policies.fallback import FallbackPolicy
from rasa_core.policies.keras_policy import KerasPolicy


logger = logging.getLogger(__name__)

def run_weather_online(interpreter,domain_file='weather_domain.yml',
                        training_data_file='data/stories.md'):
    action_endpoint = EndpointConfig(url="http://localhost:5000/webhook")
    fallback = FallbackPolicy(fallback_action_name="action_default_fallback",
                          core_threshold=0.8,
                          nlu_threshold=0.8)
    agent = Agent('./weather_domain.yml', 
                    policies = [MemoizationPolicy(max_history = 2,), 
                    KerasPolicy(epochs =  500,
                    batch_size = 50,
                    validation_split = 0.2),fallback],interpreter=interpreter,
                    action_endpoint=action_endpoint)
    data_ = agent.load_data(training_data_file,
                            augmentation_factor=50)

    agent.train(data_)
    interactive.run_interactive_learning(agent,training_data_file,skip_visualization=True)


    
	# agent.handle_channels(input_channel)
    return agent

if __name__ == '__main__':
    logging.basicConfig(level="INFO")
    nlu_interpreter = RasaNLUInterpreter('./models/nlu/default/weathernlu')
    run_weather_online(nlu_interpreter)
    