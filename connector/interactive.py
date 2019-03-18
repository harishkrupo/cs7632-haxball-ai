import aiohttp
import functools, operator

import replay

class Interactive:
  def __init__(self):
    self.input = 0
    self._sent_input = None
    self._player_id = None
    self.game = None
    self.player = None

  def onUpdate(self):
    pass

  def setInput(self, *inputs):
    self.input = functools.reduce(operator.or_, (x.value for x in inputs), 0)

  async def play(self):
    async with aiohttp.ClientSession() as s:
      async with s.ws_connect('ws://localhost:80/user') as ws:
        async for msg in ws:
          if msg.type == aiohttp.WSMsgType.BINARY:
            self._player_id = msg.data[0]
            self.game, _ = replay.Game(msg.data, 1)
            self.player = self.game.players and next((x for x in self.game.players if x.id == self._player_id), None)
            self.onUpdate()
            if self.input != self._sent_input:
              await ws.send_str('%d' % self.input)
              self._sent_input = self.input
          else:
            break
