from plumbum import cli
from plumbum import colors
import os
import logging

# class MyApp(cli.Application):
#     verbose = cli.Flag(["v", "verbose"], help="If given, I will be very talkative")
#
#     def main(self, filename):
#         print("I will now read {0}".format(filename))
#         if self.verbose:
#             print("Yadda " * 200)
#
# class MyApp(cli.Application):
#     _allow_root = False  # provide a default
#
#     @cli.switch("--log-to-file", str)
#     def log_to_file(self, filename):
#         """Sets the file into which logs will be emitted"""
#         print('--record-log-to-file ')
#
#     @cli.switch(["-r", "--root"])
#     def allow_as_root(self):
#         """If given, allow running as root"""
#         self._allow_root = True
#
#     def main(self):
#         if self._allow_root:
#             print('allow-root')
try:
    import colorama
    colorama.init(autoreset = False)
except ImportError:
    pass
# class MyApp(cli.Application):
#     _port = 8080
#     _mode = "TCP"
#
#     @cli.switch("-p", cli.Range(1024, 65535),mandatory = True)
#     def server_port(self, port):
#         self._port = port
#
#     @cli.switch("-m", cli.Set("TCP", "UDP", case_sensitive=False),mandatory = True)
#     def server_mode(self, mode):
#         self._mode = mode

    # def main(self):
    #     print(self._port, self._mode)

from plumbum import cli, colors


class Geet(cli.Application):
    SUBCOMMAND_HELPMSG = False
    DESCRIPTION = colors.yellow | """The l33t version control"""
    PROGNAME = colors.green
    VERSION = colors.blue | "1.7.2"
    COLOR_USAGE = colors.magenta
    COLOR_GROUPS = {"Meta-switches": colors.bold, "Switches": colors.skyblue1, "Subcommands": colors.yellow}

    verbosity = cli.SwitchAttr("--verbosity", cli.Set("low", "high", "some-very-long-name", "to-test-wrap-around"),
                               help=colors.cyan | "sets the verbosity level of the geet tool. doesn't really do anything except for testing line-wrapping "
                                                  "in help " * 3)
    verbositie = cli.SwitchAttr("--verbositie",
                                cli.Set("low", "high", "some-very-long-name", "to-test-wrap-around"),
                                help=colors.hotpink | "sets the verbosity level of the geet tool. doesn't really do anything except for testing line-wrapping "
                                                      "in help " * 3)


@Geet.subcommand(colors.red | "commit")
class GeetCommit(cli.Application):
    """creates a new commit in the current branch"""

    auto_add = cli.Flag("-a", help="automatically add changed files")
    message = cli.SwitchAttr("-m", str, mandatory=True, help="sets the commit message")

    def main(self):
        print("committing...")


GeetCommit.unbind_switches("-v", "--version")


@Geet.subcommand("push")
class GeetPush(cli.Application):
    """pushes the current local branch to the remote one"""

    tags = cli.Flag("--tags", help="whether to push tags (default is False)")

    def main(self, remote, branch="master"):
        print("pushing to %s/%s..." % (remote, branch))


if __name__ == "__main__":
    Geet.run()
