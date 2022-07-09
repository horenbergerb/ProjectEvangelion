from transformers import AutoTokenizer, GPT2LMHeadModel, set_seed

import logging


class Lilith:
    """
    Lilith uses torch to load a pretrained GPT-2 model
    and perform text generation in the format of Discord dialogue.

    Each call to generate_response will generate a single message from Lilith
    """
    def __init__(self,
                 model_dir,
                 username,
                 seed=42,
                 temperature=0.43,
                 max_length=128,
                 top_k=50,
                 top_p=.95,
                 repetition_penalty=1.15,
                 bad_words=[]):
        """
        :param model_dir: The directory from with the pretrained GPT-2 model is loaded
        :param username: The username which Lilith will be imitating
        :param seed: parameter for GPT-2 generation
        :param temperature: parameter for GPT-2 generation
        :param max_length: parameter for GPT-2 generation
        :param top_k: parameter for GPT-2 generation
        :param top_p: parameter for GPT-2 generation
        :param repetition_penalty: parameter for GPT-2 generation
        :param bad_words: Words which GPT-2 cannot generate. Typically include other conversation participants here so
        Lilith will not try to speak for them.
        """

        self.logger = logging.getLogger(__name__)

        # FriendSimulator trains such that <username> is converted to a special token, so we use that formatting here
        self.username = '<' + username + '>'

        self.logger.info('Initializing with username: {}...'.format(self.username))

        self.temperature = temperature
        self.max_length = max_length
        self.top_k = top_k
        self.top_p = top_p
        self.repetition_penalty = repetition_penalty
        self.bad_words = bad_words

        if self.bad_words is None:
            self.bad_words = []

        self.chat_history = ''

        set_seed(seed)

        self.logger.info('Loading GPT-2 model...')
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
            self.pt_model = GPT2LMHeadModel.from_pretrained(model_dir, pad_token_id=self.tokenizer.eos_token_id)
        except AttributeError as e:
            self.logger.error('Error loading GPT-2 model. Are you sure the model_dir directory is correct?')
            raise Exception(e)

        self.logger.info('Loading GPT-2 model completed')

        if self.bad_words:
            self.bad_words = self.tokenizer(self.bad_words, add_special_tokens=True, return_tensors='pt')['input_ids'].tolist()

        self.logger.info('Initialization completed')

    def add_history(self, new_text):
        """
        Appends to the chat history which will be input into GPT-2
        :param new_text: text to be added to history
        """
        self.chat_history += new_text

    def generate_response(self):
        """
        Feeds the chat history into GPT-2 and generates a response from Lilith.
        :return: The response from Lilith as a string, ex) "that's cool dude"
        """

        self.logger.info('Generating response...')
        # Append Lilith's username to the chat history so she knows it is her turn to speak
        self.chat_history += '\n' + self.username + ' '
        gpt2_input = self.chat_history
        encoded_gpt2_input = self.tokenizer.encode(gpt2_input, add_special_tokens=True, return_tensors='pt')
        if len(encoded_gpt2_input[0]) > self.max_length//2:
            encoded_gpt2_input = encoded_gpt2_input[..., len(encoded_gpt2_input)-(self.max_length//2):]
            gpt2_input = self.tokenizer.decode(encoded_gpt2_input[0], clean_up_tokenization_spaces=True)

        pt_text = self.pt_model.generate(
            encoded_gpt2_input,
            max_length=self.max_length,
            temperature=self.temperature,
            repetition_penalty=self.repetition_penalty,
            top_k=self.top_k,
            top_p=self.top_p,
            do_sample=True,
            num_return_sequences=1,
            bad_words_ids=self.bad_words
        )

        pt_text = pt_text.squeeze_()
        pt_text = self.tokenizer.decode(pt_text, clean_up_tokenization_spaces=True)
        # truncate output to keep only the first complete message from Lilith
        new_content = pt_text[len(gpt2_input):].split('\n')[0]
        self.chat_history += new_content

        self.logger.info('Generating response completed')
        return new_content
