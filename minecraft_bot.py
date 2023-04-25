from javascript import require, On
mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')

RANGE_GOAL = 1
BOT_USERNAME = 'python'

bot = mineflayer.createBot({
  'host': 'localhost',   # 127.0.0.1
  'port': 25565,
  'username': BOT_USERNAME,
  'hideErrors': False,
  'version': '1.18.2'
})

bot.loadPlugin(pathfinder.pathfinder)
print("Started mineflayer")

@On(bot, 'spawn')
def handle(*args):
  movements = pathfinder.Movements(bot)
  print("I spawned 👋")

  @On(bot, 'chat')
  def handleMsg(this, sender, message, *args):
    print("Got message", sender, message)
    if message[0] == '!':

      if 'come' in message:
        player = bot.players[sender]
        target = player.entity
        if not target:
          bot.chat("I don't see you !")
          return

        pos = target.position
        bot.pathfinder.setMovements(movements)
        bot.pathfinder.setGoal(pathfinder.goals.GoalNear(pos.x, pos.y, pos.z, RANGE_GOAL))

      if 'mine' in message:
        cobble_pos = bot.findBlock({ 'matching': 12, 'maxDistance': 3, 'count': 1})    # id 12 je cobblestone
        if cobble_pos:
          bot.chat("I found cobblestone at " + str(cobble_pos.position))
          while True:
            if bot.blockAt(cobble_pos.position).type == 12:
              bot.dig(bot.blockAt(cobble_pos.position), True)
        else:
          bot.chat("I don't see any cobblestone !")

      if 'inventory' in message:
        items = bot.inventory.items()
        items = list(map(lambda item: str(item.count) + ' ' + item.name, items))
        if items:
          bot.chat("I have " + str(items))
        else:
          bot.chat("I don't have anything")

      if 'go to' in message:
        pos = {
          'x': message.split(' ')[-3],
          'y': message.split(' ')[-2],
          'z': message.split(' ')[-1]
        }
        bot.pathfinder.setMovements(movements)
        bot.pathfinder.setGoal(pathfinder.goals.GoalNear(pos.get('x'), pos.get('y'), pos.get('z'), 0))