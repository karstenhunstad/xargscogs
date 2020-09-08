from datetime import datetime, tzinfo
from typing import TYPE_CHECKING

from apscheduler.triggers.cron import CronTrigger
from dateutil import parser, tz
from discord.ext.commands import BadArgument, Converter

from fifo.timezones import assemble_timezones

if TYPE_CHECKING:
    DatetimeConverter = datetime
    CronConverter = str
else:
    class TimezoneConverter(Converter):
        async def convert(self, ctx, argument) -> tzinfo:
            tzinfos = assemble_timezones()
            if argument.upper() in tzinfos:
                return tzinfos[argument.upper()]

            timez = tz.gettz(argument)

            if timez is not None:
                return timez
            raise BadArgument()

    class DatetimeConverter(Converter):
        async def convert(self, ctx, argument) -> datetime:
            dt = parser.parse(argument, fuzzy=True, tzinfos=assemble_timezones())
            if dt is not None:
                return dt
            raise BadArgument()

    class CronConverter(Converter):
        async def convert(self, ctx, argument) -> str:
            try:
                CronTrigger.from_crontab(argument)
            except ValueError:
                raise BadArgument()

            return argument
