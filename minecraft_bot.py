from javascript import require, On
mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')

RANGE_GOAL = 1
BOT_USERNAME = 'soifr'

bot = mineflayer.createBot({
  'host': 'klobasnicek.aternos.me',   # 127.0.0.1
  'port': 36985,
  'username': BOT_USERNAME
})

bot.loadPlugin(pathfinder.pathfinder)
print("Started mineflayer")

@On(bot, 'spawn')
def handle(*args):
  print("I spawned 👋")
  movements = pathfinder.Movements(bot)

  @On(bot, 'chat')
  def handleMsg(this, sender, message, *args):
    print("Got message", sender, message)
    if message[0] == '!':

      if 'come' in message:
        player = bot.players[sender]
        print("Target", player)
        target = player.entity
        if not target:
          bot.chat("I don't see you !")
          return

        pos = target.position
        bot.pathfinder.setMovements(movements)
        bot.pathfinder.setGoal(pathfinder.goals.GoalNear(pos.x, pos.y, pos.z, RANGE_GOAL))

      if 'mine' in message:
        pos = bot.entity.position
        print(bot.findBlock(pos, "cobblestone", 3, 3))
        bot.dig(bot.blockAt(bot.entity.position.offset(0, -1, 0)), True)

      if 'go to' in message:
        pos = {
          'x': message.split(' ')[-3],
          'y': message.split(' ')[-2],
          'z': message.split(' ')[-1]
        }
        bot.pathfinder.setMovements(movements)
        bot.pathfinder.setGoal(pathfinder.goals.GoalNear(pos.get('x'), pos.get('y'), pos.get('z'), 0))
        
@On(bot, "end")
def handle(*args):
  print("Bot ended!", args)