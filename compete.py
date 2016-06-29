from match import play_match
from test_bots.boilerbot import Bot

bot_a = Bot()
bot_b = Bot()

print(play_match(bot_a, bot_b, 1000))
