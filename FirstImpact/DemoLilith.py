from src.Lilith import Lilith

import logging


if __name__ == '__main__':
    # Uncomment if you'd like more logs
    # logging.basicConfig(level=logging.INFO)
    lilith_instance = Lilith(model_dir='TrainedModel',
                             username='Captain of the Dishwasher',
                             bad_words=['<kerp>'])
    lilith_instance.add_history('<kerp> hey i know this is random but would you go on a date with me?')
    print('Initial chat history:')
    print(lilith_instance.chat_history)
    print('Generating 3 sequential responses from Lilith...')
    for i in range(0, 3):
        response = lilith_instance.generate_response()
        print('    ' + response)
    print('Final chat history:')
    print(lilith_instance.chat_history)
