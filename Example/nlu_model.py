from rasa_nlu.training_data import load_data
from rasa_nlu import config
from rasa_nlu.model import Trainer
from rasa_nlu.model import Metadata, Interpreter
from rasa_nlu.config import RasaNLUModelConfig

def train_nlu(data, configuration, model_dir):
    training_data = load_data(data)
    trainer = Trainer(config.load(configuration))
    # trainer = Trainer(RasaNLUModelConfig(config))
    trainer.train(training_data)
    model_directory = trainer.persist(model_dir, fixed_model_name = 'weathernlu')
    # return model_directory

def run_nlu(model_directory):
  interpreter = Interpreter.load(model_directory)
  print(interpreter.parse(u"what's the weather in tamilnadu?"))
  print(interpreter.parse(u'yes i want to know the weather'))
  print(interpreter.parse(u"yes i want to know the weather in mumbai"))

if __name__ == '__main__':
    train_nlu('./data/data.json','config_spacy.yml','./models/nlu2')
    run_nlu('./models/nlu2/default/weathernlu')