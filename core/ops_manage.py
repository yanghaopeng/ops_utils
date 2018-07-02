#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/26 10:52
# @Author  : hyang
# @File    : ops_manage.py
# @Software: PyCharm

import click
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)  # 加入环境变量
from core.disk_shell import DiskCmd
from core.ps_shell import PsCmd
from conf.shell_set import ps_shell as pshell
from core.data_flow import DataFlow

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


ps_str = '检查进程{}'.format(['all'] + [pshell[key]['name']
                                    for key in pshell.keys()])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='1.0.0')
def cli():
    """Repo is a command line tool that showcases how to build complex
        command line interfaces with Click.

        This tool is supposed to look like a distributed version control
        system to show how something like this can be structured.
    )"""
    pass


@cli.command()
@click.argument('name', default='all', required=True)
# @click.option('--greeting', default='Hello', help='word to use for the greeting')
# @click.option('--caps', is_flag=True, help='uppercase the output')
def hellocmd(name):
    click.echo(
        click.style(
            'I am colored %s and bold' %
            name,
            fg='green',
            bold=True))


@cli.command()
@click.option('-t', default='a', required=True,
              type=click.Choice(['a', 'h']), prompt=True, help='检查磁盘空间,a表示所有空间，h表示空间大于50%')
def dfcmd(t):
    click.echo(click.style('检查磁盘空间', fg='green', bold=True))
    d = DiskCmd()
    type_dict = {'a': 'all', 'h': 'half'}
    d.ops_disk_cmd(type_dict.get(t))


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.option('-t', default='all', required=True,
              type=click.Choice(['all'] + list(pshell.keys())), prompt=True, help=ps_str)
def catdp(t):
    click.echo(click.style('检查数据进程%s' % t, fg='green', bold=True))
    p = PsCmd()
    p.ops_ps_cmd(op_type='cat', ps_name=t)


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.option('-t', default='all', required=True,
              type=click.Choice(['all'] + list(pshell.keys())), prompt=True, help=ps_str)
def startdp(t):
    click.echo(click.style('启动数据进程%s' % t, fg='green', bold=True))
    p = PsCmd()
    p.ops_ps_cmd(op_type='start', ps_name=t)


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.option('-t', default='all', required=True,
              type=click.Choice(['all'] + list(pshell.keys())), prompt=True, help=ps_str)
def stopdp(t):
    click.echo(click.style('停止数据进程%s' % t, fg='green', bold=True))
    p = PsCmd()
    p.ops_ps_cmd(op_type='stop', ps_name=t)


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('bankid', required=True)
@click.argument('filecode', required=True)
def brec(bankid, filecode):
    """
    校验失败银行重新校验 参数: 银行代码(如:1051000)，文件代码(如:B05)
    使用 brec 1051000 B05
    """
    click.echo(
        click.style(
            '校验失败银行重新校验%s,%s' %
            (bankid, filecode), fg='green', bold=True))
    d = DataFlow()
    d.bankRC(bankid, filecode)


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('bankid', required=True)
def brerun(bankid):
    """
    银行重跑 参数: 银行代码(如:1051000)
    使用 brerun 1051000
    """
    click.echo(click.style('银行重跑%s' % bankid, fg='green', bold=True))
    d = DataFlow()
    d.bankRerun(bankid)


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('bankid', required=True)
def breload(bankid):
    """
    重新装载 参数: 银行代码(如:1051000)
    使用 breload 1051000
    """
    click.echo(click.style('银行重新装载%s' % bankid, fg='green', bold=True))
    d = DataFlow()
    d.bankRerun(bankid)


@cli.command(context_settings=CONTEXT_SETTINGS)
def upsctime():
    """
    修改证券公司装载时间
    使用 scuptime
    """
    click.echo(click.style('修改证券公司装载时间', fg='green', bold=True))
    d = DataFlow()
    d.upComLoadTime()


@cli.command(context_settings=CONTEXT_SETTINGS)
def initcom():
    """
    证券公司处理表初始化
    使用 initcom
    """
    click.echo(click.style('证券公司处理表初始化', fg='green', bold=True))
    d = DataFlow()
    d.initCom()


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('start', required=True)
@click.argument('end', required=True)
@click.argument('comid', required=True)
def initCComCal(start, end, comid):
    """
    中登拆分证券公司日历初始化 参数: 开始日期(如:20180102) 结束日期(如:20181202) 证券公司代码 com_id
    使用 initCComCal 20180102 20181202 10040000
    """
    click.echo(
        click.style(
            '中登拆分证券公司日历初始化%s , %s, %s' %
            (start, end, comid), fg='green', bold=True))
    d = DataFlow()
    d.initComCal(start, end, comid)


if __name__ == '__main__':
    cli()
