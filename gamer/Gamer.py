import logging

import aiohttp

from main import game


class Gamer:
    def __init__(self, loop, rand_sleep):
        self._api_url = 'http://localhost:8081'
        self._session = aiohttp.ClientSession()
        self._game = game
        self._players = {}
        self._rand_sleep = rand_sleep
        self._loop = loop

    async def _prepare_player(self, team_name):
        async with self._session.post(
                f'{self._api_url}/game',
                params={'team_name': team_name}
        ) as resp:
            res = (await resp.json())['data']
            player_num = 1 if res['color'] == 'RED' else 2
            self._players[player_num] = {
                'color': res['color'],
                'token': res['token']
            }

    async def _make_move(self, player, move):
        json = {'move': move}
        headers = {'Authorization': f'Token {self._players[player]["token"]}'}
        async with self._session.post(
                f'{self._api_url}/move',
                json=json,
                headers=headers
        ) as resp:
            resp = (await resp.json())['data']
            logging.info(f'Player {player} made move {move}, response: {resp}')

    def start(self):
        self._prepare_player('BOT NAME')

if __name__ == '__main__':
    Gamer
