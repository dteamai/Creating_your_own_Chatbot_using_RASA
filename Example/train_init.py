import logging

from rasa_core.agent import Agent
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core import training
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.utils import EndpointConfig
import rasa_core
from rasa_core.run import serve_application
from rasa_core.policies.fallback import FallbackPolicy
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.embedding_policy import EmbeddingPolicy
def run_weather_bot(serve_forever=True):
	interpreter = RasaNLUInterpreter('./models/nlu/default/weathernlu')
	action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
	agent = Agent.load('./models/dialogue_element2', interpreter=interpreter, action_endpoint=action_endpoint)
	rasa_core.run.serve_application(agent ,channel='cmdline',port=5004)
		
	return agent
if __name__ == '__main__':
    logging.basicConfig(level='INFO')

    training_data_file = './data/stories.md'
    model_path = './models/dialogue_element2'
    
    fallback = FallbackPolicy(fallback_action_name="action_default_fallback",
                          core_threshold=0.5,
                          nlu_threshold=0.5)
    # agent = Agent('./weather_domain.yml', 
    #                 policies = [MemoizationPolicy(max_history = 2,), 
    #                 KerasPolicy(epochs =  100 ,#),fallback])
    #                 batch_size = 50,
    #                 validation_split = 0.2),fallback])
    # agent = Agent('./weather_domain.yml', 
    #                 policies = [MemoizationPolicy(max_history = 2,), 
    #                 KerasPolicy(epochs =  500,
    #                 batch_size = 50,
    #                 validation_split = 0.2),fallback])

    agent = Agent('./weather_domain.yml', 
                    policies = [MemoizationPolicy(max_history = 10,), 
                    KerasPolicy(epochs = 150,
                    batch_size = 50,rnn_size=500), fallback])

    data_ = agent.load_data(training_data_file,
                            augmentation_factor=50)

    agent.train(data_)

    agent.persist(model_path)
    run_weather_bot()