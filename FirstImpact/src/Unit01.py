from src.Lilith import Lilith

import discord
import logging


class Unit01(discord.Client):
    def __init__(self,
                 model_dir,
                 username,
                 bad_words=[]):
        super().__init__()

        self.logger = logging.getLogger(__name__)
        self.lilith_instance = Lilith(model_dir=model_dir,
                                      username=username,
                                      bad_words=bad_words)

    async def on_ready(self):
        self.logger.info('Logged on as {0}'.format(self.user))

    async def on_message(self, message):
        if message.author == self.user:
            return

        async with message.channel.typing():
            # reformat message to match the data the model was trained on
            formatted_message = '<' + str(message.author).split('#')[0] + '> ' + message.content + '\n'

            self.lilith_instance.add_history(formatted_message)
            response = self.lilith_instance.generate_response()
            await message.channel.send(response)
