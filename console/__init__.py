## console.py

import os, cmd, readline, i18n
from utils import Helper


banner = (
    "\033[0;36m"
    + """
  ================================================
    _   _  _____  _____                     _
   | \ | |/  ___||  ___|                   | |
   |  \| |\ `--. | |__    __ _  _ __   ___ | |__
   | . ` | `--. \|  __|  / _` || '__| / __|| '_  |
   | |\  |/\__/ /| |___ | (_| || |   | (__ | | | |
   \_| \_/\____/ \____/  \__,_||_|    \___||_| |_|
  ================================================
   Version 0.4  http://goo.gl/8mFHE5  @jjtibaquira
   Email: jko@dragonjar.org  |   www.dragonjar.org
  ================================================
"""
    + "\033[0m"
)


class Console(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "nsearch> "
        self.intro = banner
        self.doc_header = i18n.t("help.doc_header")
        self.misc_header = i18n.t("help.misc_header")
        self.undoc_header = i18n.t("help.undoc_header")
        self.ruler = "="

    ## autocomplete definition list
    serachCommands = ["name", "category", "help", "author"]
    showfavOptions = ["name", "ranking", "help"]

    ## Command definitions ##
    def do_history(self, args):
        """Print a list of commands that have been entered"""
        print(self._history)

    def do_exit(self, args):
        """Exits from the console"""
        return -1

    def do_help(self, args):
        """Get help on commands
        'help' or '?' with no arguments prints a list of commands for which help is available
        'help <command>' or '? <command>' gives help on <command>
        """
        ## The only reason to define this method is for the help text in the doc string
        cmd.Cmd.do_help(self, args)

    ## Override methods in Cmd object ##
    def preloop(self):
        """Initialization before prompting user for commands.
        Despite the claims in the Cmd documentaion, Cmd.preloop() is not a stub.
        """
        cmd.Cmd.preloop(self)  ## sets up command completion
        self._history = ""  ## No historyory yet
        self._locals = {}  ## Initialize execution namespace for user
        self._globals = {}
        old_delims = readline.get_completer_delims()
        readline.set_completer_delims(old_delims.replace("-", ""))

    def postloop(self):
        """Take care of any unfinished business.
        Despite the claims in the Cmd documentaion, Cmd.postloop() is not a stub.
        """
        cmd.Cmd.postloop(self)  ## Clean up command completion
        print("\033[0;36m Exiting ... :D\033[0m")

    def precmd(self, line):
        """This method is called after the line has been input but before
        it has been interpreted. If you want to modifdy the input line
        before execution (for example, variable substitution) do it here.
        """
        self._history += line.strip() + "\n"
        return line

    def postcmd(self, stop, line):
        """If you want to stop the console, return something that evaluates to true.
        If you want to do some post command processing, do it here.
        """
        return stop

    def emptyline(self):
        """Do nothing on empty input line"""
        pass

    def do_clear(self, args):
        """ Clear the shell """
        os.system("clear")
        print(self.intro)

    def do_search(self, args):
        """ Search """
        search = Helper(args, "search")
        search.process()

    def complete_search(self, text, line, begidx, endidx):
        if not text:
            commands = self.serachCommands[:]
        else:
            commands = [f for f in self.serachCommands if f.startswith(text)]
        return commands

    def help_search(self):
        print(
            "\n".join(
                [
                    "\n\tname     : " + i18n.t("help.help_search_name") + "",
                    "\tcategory : " + i18n.t("help.help_search_category") + "",
                    "\tauthor   : " + i18n.t("help.help_search_author") + "",
                    "\t" + i18n.t("help.help_usage") + ":",
                    "\t\tsearch name:http",
                    "\t\tsearch category:exploit",
                    "\t\tsearch author:fyodor",
                    "\t\tsearch name:http category:exploit author:fyodor",
                ]
            )
        )

    def do_doc(self, args):
        """ Display Script Documentaion"""
        doc = Helper(args)
        doc.displayDoc()

    def help_doc(self):
        print("\t" + i18n.t("help.help_doc"))
        print("\t" + i18n.t("help.help_usage"))
        print("\t\t" + i18n.t("help.help_doc_exmp"))

    def complete_doc(self, text, line, begidx, endidx):
        """ Autocomplete over the last result """
        resultitems = Helper()
        return [i for i in resultitems.resultitems() if i.startswith(text)]

    def do_last(self, args):
        """ last help"""
        search = Helper()
        search.printlastResult()

    def help_last(self):
        print(i18n.t("help.help_last"))

    # handler fav actions
    def do_addfav(self, args):
        search = Helper(args, "addfav")
        search.process()

    def help_addfav(self):
        print(
            "\n".join(
                [
                    "\t" + i18n.t("help.help_addfav") + "",
                    "\tname     : " + i18n.t("help.help_fav_name") + "",
                    "\tranking : " + i18n.t("help.help_fav_ranking") + "",
                    "\t" + i18n.t("help.help_usage") + ":",
                    "\t\taddfav name:http ranking:great",
                ]
            )
        )

    def complete_addfav(self, text, line, begidx, endidx):
        """ Autocomplete over the last result """
        resultitems = Helper()
        return [i for i in resultitems.resultitems() if i.startswith(text)]

    def do_delfav(self, args):
        search = Helper(args, "delfav")
        search.process()

    def help_delfav(self):
        print(
            "\n".join(
                [
                    "\t" + i18n.t("help.help_delfav") + "",
                    "\tname     : " + i18n.t("help.help_fav_name") + "",
                    "\t" + i18n.t("help.help_usage") + ":",
                    "\t\tdelfav name:http",
                ]
            )
        )

    def complete_delfav(self, text, line, begidx, endidx):
        """ Autocomplete over the last result """
        resultitems = Helper()
        return [i for i in resultitems.resultitems() if i.startswith(text)]

    def do_modfav(self, args):
        search = Helper(args, "modfav")
        search.process()

    def help_modfav(self):
        print(
            "\n".join(
                [
                    "\t" + i18n.t("help.help_modfav") + "",
                    "\tname     : " + i18n.t("help.help_search_name") + "",
                    "\tnewname : " + i18n.t("help.help_fav_name") + "",
                    "\tnewranking   : " + i18n.t("help.help_fav_ranking") + "",
                    "\t" + i18n.t("help.help_usage") + ":",
                    "\t\tmodfav name:http newname:http-new-script newranking:super-great",
                ]
            )
        )

    def complete_modfav(self, text, line, begidx, endidx):
        """ Autocomplete over the last result """
        resultitems = Helper()
        return [i for i in resultitems.resultitems() if i.startswith(text)]

    def do_showfav(self, args):
        search = Helper(args, "showfav")
        search.process()

    def help_showfav(self):
        print(
            "\n".join(
                [
                    "\t" + i18n.t("help.help_showfav") + "",
                    "\tname     : " + i18n.t("help.help_fav_name") + "",
                    "\tranking : " + i18n.t("help.help_fav_ranking") + "",
                    "\t" + i18n.t("help.help_usage") + ":",
                    "\t\tshowfav name:http",
                    "\t\tshowfav ranking:great",
                    "\t\tshowfav name:http ranking:great",
                ]
            )
        )

    def complete_showfav(self, text, line, begidx, endidx):
        if not text:
            commands = self.showfavOptions[:]
        else:
            commands = [f for f in self.showfavOptions if f.startswith(text)]
        return commands

    # default action cmd class
    def default(self, line):
        """Called on an input line when the command prefix is not recognized.
        In that case we execute the line as Python code.
        """
        try:
            exec(line) in self._locals, self._globals
        except Exception as e:
            print(e.__class__, ":", e)
