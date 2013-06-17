import bootstrap
import pau
import pau.webkit
import pau.less
import pau.views
from nark import *


class App(object):

  def __init__(self):
    
    self.config = pau.IConfig
    self.db = pau.IDb
    self.session = pau.ISession

    pau.resolve(self)

    # Setup database
    self.db.init()

    # Setup webkit
    a = self.session.assets
    base = a.base() + "/"
    path = a.resolve("index.html")
    self.webkit = pau.webkit.Webkit(base, path)
    self.session.webkit = self.webkit

    # Attach views
    controller = pau.Controller(self.webkit)
    controller.load(pau.views)

    # Rebuild assets
    runner = pau.less.Less()
    runner.execute(a.resolve("css"))

  def run(self):
    """ Launch the UI """
    self.webkit.run()


if __name__ == "__main__":
    app = App()
    app.run()
