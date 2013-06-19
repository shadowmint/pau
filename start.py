import bootstrap
import pau
import pau.webkit
import pau.less
import pau.views
from nark import *


@resolve(pau.scope)
class App(object):

  def __init__(self, config=pau.IConfig, db=pau.IDb, session=pau.ISession):
    
    self.config = config
    self.db = db
    self.session = session

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
