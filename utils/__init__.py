from dbmodule import *


class Helper:
    def __init__(self, args="", commnad=""):
        self.args = args
        self.commnad = commnad

    # process the commnads
    def process(self):
        if self.commnad == "search":
            if not self.args:
                dbmodule.lastresults = dbmodule.searchAll()
                self.printlastResult()
            else:
                dbmodule.lastresults = dbmodule.searchByCriterial(
                    **self.__searchparams()
                )
                self.printlastResult()
        elif self.commnad == "addfav":
            dbmodule.createFavorite(**self.__addfavparams())
        elif self.commnad == "modfav":
            dbmodule.updateFavorite(**self.__modfavparams())
        elif self.commnad == "delfav":
            dbmodule.deleteFavorite(**self.__delfavparams())
        elif self.commnad == "showfav":
            if not self.args:
                dbmodule.lastresults = dbmodule.getFavorites()
                self.printlastResult(True)
            else:
                dbmodule.lastresults = dbmodule.getFavorites(**self.__showfavparams())
                self.printlastResult(True)
        else:
            print("Error")

    # Display the last results
    def printlastResult(self, fav=False):
        if fav:
            print("\033[1;32m*** {0:40} {1:40}\033[0m".format(*["Name", "Ranking"]))
            for key, value in dbmodule.lastresults.items():
                print(
                    "\033[1;32m[+] {0:40} {1:35}\033[0m".format(
                        *[value["name"], value["ranking"]]
                    )
                )
        else:
            print("\033[1;32m*** {0:40} {1:40}\033[0m".format(*["Name", "Author"]))
            for key, value in dbmodule.lastresults.items():
                print(
                    "\033[1;32m[+] {0:40} {1:35}\033[0m".format(
                        *[value["name"], value["author"]]
                    )
                )

    # Display the documentation per script
    def displayDoc(self):
        scriptFile = open(dbmodule.scriptsPath + self.args, "r")
        lines = scriptFile.read().splitlines()
        for line in lines:
            if line.startswith("license"):
                break
            print("\033[1;96m" + line + "\033[0m")
        scriptFile.close()

    # used for the autocomplete
    def resultitems(self):
        i = 0
        items = []
        for k, v in dbmodule.lastresults.items():
            items.insert(i, v["name"])
            i = i + 1
        return items

    # private function to set params for search command
    def __searchparams(self):
        if (
            self.args.find("name:") != -1
            or self.args.find("category:") != -1
            or self.args.find("author:") != -1
        ):
            return self.__setParams()

    # private funtion to set params for addfav command
    def __addfavparams(self):
        if self.args.find("name:") != -1 or self.args.find("ranking:") != -1:
            return self.__setParams()

    # private funtion to set params for delfav command
    def __delfavparams(self):
        if self.args.find("name:") != -1:
            return self.__setParams()

    # private function to set params for modfav command
    def __modfavparams(self):
        if (
            self.args.find("name:") != -1
            or self.args.find("newname:") != -1
            or self.args.find("newranking:") != -1
        ):
            return self.__setParams()

    # private function to set paramas for showfav command
    def __showfavparams(self):
        if self.args.find("name:") != -1 or self.args.find("ranking:") != -1:
            return self.__setParams()

    # Set Params validations
    def __setParams(self):
        argsdic = {}
        if len(self.args.split(":")) >= 4:
            argsdic.update(
                {
                    self.args.split(":")[0]: self.args.split(":")[1].split(" ")[0],
                    self.args.split(":")[1]
                    .split(" ")[1]: self.args.split(":")[2]
                    .split(" ")[0],
                    self.args.split(":")[2]
                    .split(" ")[1]: self.args.split(":")[3]
                    .split(" ")[0],
                }
            )
        elif len(self.args.split(":")) == 3:
            argsdic.update(
                {
                    self.args.split(":")[0]: self.args.split(":")[1].split(" ")[0],
                    self.args.split(":")[1]
                    .split(" ")[1]: self.args.split(":")[2]
                    .split(" ")[0],
                }
            )
        elif len(self.args.split(":")) == 2:
            argsdic.update(
                {self.args.split(":")[0]: self.args.split(":")[1].split(" ")[0]}
            )
        else:
            print("Plase enter a correct commands")
        return argsdic
