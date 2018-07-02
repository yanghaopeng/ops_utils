# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# # @Time    : 2018/5/24 23:50
# # @Author  : hyang
# # @File    : hello.py
# # @Software: luffy_test
#
import click
# #
# # @click.command()
# # @click.option('--count', default=1, help='Number of greetings.')
# # @click.option('--name', prompt='Your name',
# #               help='The person to greet.')
# # def hello(count, name):
# #     """Simple program that greets NAME for a total of COUNT times."""
# #     for x in range(count):
# #         click.echo('Hello %s!' % name)
#
#
#
# # def print_version(ctx, param, value):
# #     if not value or ctx.resilient_parsing:
# #         return
# #     click.echo('Version 1.0')
# #     ctx.exit()
# #
# # @click.command()
# # @click.option('--version', is_flag=True, callback=print_version,
# #               expose_value=False, is_eager=True)
# # def hello():
# #     click.echo('Hello World!')
#
#
#
# # yes parameters
# import click
#
#
# def print_version(ctx, param, value):
#     if not value or ctx.resilient_parsing:
#         return
#     click.echo('Version 1.0')
#     ctx.exit()
#
#
# def abort_if_false(ctx, param, value):
#     if not value:
#         ctx.abort()
#     else:
#         grade = int(input('输入成绩: '))
#
#         if grade > 100:
#             print('成绩最多到100')
#         elif grade >= 90:
#             print('A')
#         elif grade >= 80:
#             print('B')
#         elif grade >= 60:
#             print('C')
#         elif grade >= 40:
#             print('D')
#         elif grade >= 0:
#             click.secho('E',fg='green')
#         else:
#             click.secho('成绩不能为负数',fg="red")
#
# @click.command()
# # @click.option('--version', is_flag=True, callback=print_version,
# #               expose_value=False, is_eager=True)
# @click.option('--name', default='Ethan', help='name')
# @click.option('--grade', is_flag=False, expose_value=False, is_eager=True,prompt='input grade', callback=abort_if_false)
# # is_flag=False 表示需要输入参数值
# # @click.option('--yes', is_flag=True, callback=abort_if_false,
# # expose_value=False,
# # prompt='Are you sure you want to drop the db?')
# def hello(name):
#     click.echo('Hello %s!' % name)
#
#
# if __name__ == '__main__':
#     hello()

#
#
# # @click.command()
# # @click.option('--name', help='The person to greet.')
# # def hello(name):
# #     click.secho('Hello %s!' % name, fg='red', underline=True)
# #     click.secho('Hello %s!' % name, fg='green', bg='black')
#
#
# # if __name__ == '__main__':
# #     print("hello")
# #     # dropdb()


import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def greeter(**kwargs):
    output = '{0}, {1}!'.format(kwargs['greeting'],
                                kwargs['name'])
    if kwargs['caps']:
        output = output.upper()
    print(output)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='1.0.0')
def greet():
    pass


@greet.command()
@click.argument('name')
@click.option('--greeting', default='Hello', help='word to use for the greeting')
@click.option('--caps', is_flag=True, help='uppercase the output')
def hello(**kwargs):
    greeter(**kwargs)


@greet.command()
@click.argument('name')
@click.option('--greeting', default='Goodbye', help='word to use for the greeting')
@click.option('--caps', is_flag=True, help='uppercase the output')
def goodbye(**kwargs):
    greeter(**kwargs)

@greet.command()
@click.option('--hash-type', type=click.Choice(['md5', 'sha1']))
def digest(hash_type):
    click.echo(hash_type)

if __name__ == '__main__':
    greet()


# !/home/xingming/pyvirt/bin/python
# -*- coding:utf-8 -*-

#############################################
# File Name: hello.py
# Author: xiaoh
# Mail: xiaoh@about.me
# Created Time: 2016-01-29 15:00:47
#############################################

import os, sys, click


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Version 1.0')
    ctx.exit()


@click.group()
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
def cli():
    pass


@click.command()
@click.option('--n', default=1)
def dots(n):
    click.echo('.' * n)


@click.command()
@click.option('--pos', nargs=2, type=float)
def findme(pos):
    click.echo('%s / %s' % pos)


@click.command()
@click.option('--item', type=(str, int))
def putitem(item):
    click.echo('name:%s, id=%s' % item)


@click.command()
@click.option('--message', '-m', multiple=True)
def commit(message):
    click.echo('\n'.join(message))


@click.command()
@click.option('-v', '--verbose', count=True)
def log(verbose):
    click.echo('Verbosity: %s' % verbose)


@click.command()
@click.option('--shout/--no-shout', default=False)
def info(shout):
    rv = sys.platform
    if shout:
        rv = rv.upper() + '!!!!111'
    click.echo(rv)


@click.command()
@click.option('--shout', is_flag=True)
def info1(shout):
    rv = sys.platform
    if shout:
        rv = rv.upper() + '!!!!111'
    click.echo(rv)


@click.command()
@click.option('/debug;/no-debug')
def info2(debug):
    click.echo('debug=%s' % debug)


@click.command()
@click.option('--upper', 'transformation', flag_value='upper',
              default=True)
@click.option('--lower', 'transformation', flag_value='lower')
def info3(transformation):
    click.echo(getattr(sys.platform, transformation)())


@click.command()
@click.option('--hash-type', type=click.Choice(['md5', 'sha1']))
def digest(hash_type):
    click.echo(hash_type)


@click.command()
@click.option('--name', prompt=True)
def hello(name):
    click.echo('Hello %s!' % name)


@click.command()
@click.option('--password', prompt=True, hide_input=True,
              confirmation_prompt=True)
def encrypt(password):
    click.echo('Encrypting password to %s' % password.encode('rot13'))


@click.command()
@click.password_option()
def encrypt1(password):
    click.echo('Encrypting password to %s' % password.encode('rot13'))


@click.command()
@click.option('--username', prompt=True,
              default=lambda: os.environ.get('USER', ''))
def hello1(username):
    print("Hello,", username)


@click.command()
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
def hello2():
    click.echo('Hello World!')


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


@click.command()
@click.option('--yes', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Are you sure you want to drop the db?')
def dropdb():
    click.echo('Dropped all tables!')


@click.command()
@click.argument('filename')
def touch(filename):
    click.echo(filename)


@click.command()
@click.argument('src', nargs=-1)
@click.argument('dst', nargs=1)
def copy(src, dst):
    for fn in src:
        click.echo('move %s to folder %s' % (fn, dst))


@click.command()
@click.argument('input', type=click.File('rb'))
@click.argument('output', type=click.File('wb'))
def inout(input, output):
    while True:
        chunk = input.read(1024)
        if not chunk:
            break
        output.write(chunk)


@click.command()
@click.argument('f', type=click.Path(exists=True))
def touch1(f):
    click.echo(click.format_filename(f))


@click.command()
@click.argument('src', envvar='SRC', type=click.File('r'))
def echo(src):
    click.echo(src.read())


@click.command()
@click.argument('files', nargs=-1, type=click.Path())
def touch2(files):
    for filename in files:
        click.echo(filename)


cli.add_command(touch2)
cli.add_command(echo)
cli.add_command(touch1)
cli.add_command(inout)
cli.add_command(copy)
cli.add_command(touch)
cli.add_command(dropdb)
cli.add_command(hello2)
cli.add_command(hello1)
cli.add_command(encrypt1)
cli.add_command(encrypt)
cli.add_command(dots)
cli.add_command(findme)
cli.add_command(putitem)
cli.add_command(commit)
cli.add_command(log)
cli.add_command(info)
cli.add_command(info1)
cli.add_command(info2)
cli.add_command(info3)
cli.add_command(digest)
cli.add_command(hello)

if __name__ == "__main__":
    cli()
    #>pip download -d C:\Users\china\pyenv -r requirements.txt