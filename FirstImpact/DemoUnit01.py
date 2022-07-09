from src.Unit01 import Unit01


if __name__ == '__main__':
    unit01_instance = Unit01(model_dir='TrainedModel',
                             username='kerp',
                             bad_words=['<Captain of the Dishwasher>'])

    # place token here
    token = None
    if token is None:
        raise Exception('You have not provided a token yet. Please add a token to this script.')

    unit01_instance.run(token, bot=False)
