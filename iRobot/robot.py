from iBott import ChromeBrowser
from iBott.robot_activities import Robot, Robotmethod, get_all_Methods
from google_search import Keywords
from iRobot.exceptions import BusinessException, SystemException
import iRobot.settings as settings


class Main(Robot):
    def __init__(self, args):
        self.methods = get_all_Methods(self)
        if args is not None:
            self.robotId = args['RobotId']
            self.ExecutionId = args['ExecutionId']
            self.url = args['url']
            self.username = args['username']
            self.password = args['password']
            self.robotParameters = args['params']
            super().__init__(robotId=self.robotId, ExecutionId=self.ExecutionId, url=self.url,
                             username=self.username, password=self.password,
                             params=self.robotParameters)
        else:
            super().__init__()

    @Robotmethod
    def init(self):
        self.browser = ChromeBrowser(undetectable=True)
        self.browser.load_extension(
            "/Users/enriquecrespodebenito/Documents/telegram/extensions/Keyword-Surfer_v3.1.0.crx")
        self.browser.open()
        self.browser.maximize_window()
        self.keywords = ["agapornis", "ninfas", "loros", "papagayos"]
        self.keyword = Keywords(self)

    @Robotmethod
    def cleanup(self):
        """Clean system before executing the robot"""
        pass


    @Robotmethod
    def start(self):
        """Init variables, instance objects and start the applications you are going to work with"""
        pass

    @Robotmethod
    def process(self):
        """Run robot process"""
        if len(self.keywords) > 0:
            k = self.keywords[0]
            self.keyword.get_search_data(k)
            self.keyword.get_page_data()
            self.keyword.store_data()
            self.keywords.remove(k)
            print(self.keywords)
            self.Log.info("Processing : " + k)

        self.process()

    @Robotmethod
    def end(self):
        """Finish robot execution, cleanup environment, close applications and send reports"""
        self.browser.close()

