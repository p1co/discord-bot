import logging
import re

from discord.game import Game

from bot.plugins.base import BasePlugin
from bot.plugins.commands import command

from .models import GameStatus


logger = logging.getLogger(__name__)


class Plugin(BasePlugin):

    has_blocking_io = True

    @command(pattern=re.compile(r'(?P<status>.+)', re.IGNORECASE))
    def add_status(self, command):
        status, created = GameStatus.objects.get_or_create(status=command.args.status.strip())
        if created:
            yield from command.reply('Status `{status}` added to the database.'.format(status=status))
        else:
            yield from command.reply('Status already existed, pk: {}'.format(status.pk))

    @command()
    def change_status(self, command):
        status = GameStatus.objects.order_by('?').first()
        game = Game(name=status.status)
        yield from self.client.change_status(game=game, idle=False)

    @command()
    def clear_status(self, command):
        yield from self.client.change_status(game=None, idle=False)

    @command()
    def list_status(self, command):
        statuses = GameStatus.objects.values('id', 'status').order_by('id')
        msg = '\n'.join(['{id} - {status}'.format(**status) for status in statuses])
        yield from command.reply(msg)

    @command(pattern=re.compile(r'(?P<id>\d+)'))
    def delete_status(self, command):
        id_ = command.args.id
        deleted, _ = GameStatus.objects.filter(id=id_).delete()
        if not deleted:
            yield from command.reply('Status {id} did not exist'.format(id=id_))
        else:
            yield from command.reply('Status deleted')
