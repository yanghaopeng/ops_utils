#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/3 10:59
# @Author  : hyang
# @File    : ops_flow_manage.py
# @Software: PyCharm

import click
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)  # 加入环境变量
from core.data_flow import DataFlow

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


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


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('bankid', required=True)
@click.argument('filecode', required=True)
def brecheck(bankid, filecode):
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
def upstime():
    """
    修改证券公司装载时间
    使用 upstime
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


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('start', required=True)
@click.argument('end', required=True)
def initworkdt(start, end):
    """
        初始化工作日历 参数: 开始日期(如:20180102) 结束日期(如:20181202)
        使用 如initworkdt 20180102 20181202
        """
    click.echo(
        click.style(
            '工作日历初始化%s , %s, %s' %
            (start, end), fg='green', bold=True))
    d = DataFlow()
    d.initCal(start, end)


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.confirmation_option(help='Are you sure you want to 中登重新校验 ?')
def ccrc():
    """
        中登重新校验
    """
    click.echo(
        click.style(
            '中登重新校验', fg='green', bold=True))
    d = DataFlow()
    d.ccRC()


if __name__ == '__main__':
    cli()
