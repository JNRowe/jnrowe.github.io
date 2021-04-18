#! /usr/bin/python3 -tt

import calendar
import colorsys
import datetime
import subprocess
import sys

import click


def pcnt_colour(percent):
    h = 1 / 3 - (1 / 3 * percent / 100)
    return '#' + ''.join(
        f'{min(int(n*256), 255):02x}' for n in colorsys.hls_to_rgb(h, 0.5, 1)
    )


def month_days(date):
    return calendar.monthrange(date.year, date.month)[1]


def days_in_year(date):
    if calendar.isleap(date.year):
        days = 366
    else:
        days = 365
    return days


def show_progress(title, percent, width):
    subprocess.run(
        ['gdbar', '-l', title, '-w', str(width), '-fg', pcnt_colour(percent)],
        input=str(percent).encode(),
    )


@click.command()
@click.option('-s', '--short/--no-short')
@click.option('-w', '--width', default=1000)
def main(short, width):
    now = datetime.datetime.now()

    midnight = datetime.datetime(now.year, now.month, now.day)
    day_pcnt = (now - midnight).total_seconds() / 86400 * 100

    month_pcnt = now.day / month_days(now) * 100

    year_pcnt = int(f'{now: %j}') / days_in_year(now) * 100

    print(
        'Progress: '
        f'D^fg({pcnt_colour(day_pcnt)}){day_pcnt:.0f}^fg()% '
        f'M^fg({pcnt_colour(month_pcnt)}){month_pcnt:.0f}^fg()% '
        f'Y^fg({pcnt_colour(year_pcnt)}){year_pcnt:.0f}^fg()%'
    )
    if not short:
        sys.stdout.flush()
        show_progress('day   ', day_pcnt, width)
        show_progress('month ', month_pcnt, width)
        show_progress('year  ', year_pcnt, width)


if __name__ == '__main__':
    main()
