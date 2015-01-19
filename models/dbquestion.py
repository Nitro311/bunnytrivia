import logging
import random
import string
from google.appengine.ext import db

class DbQuestion(db.Model):
    def __init__(self, *args, **kwargs):
        key = str(kwargs['index'])
        kwargs['key'] = db.Key.from_path('DbQuestion', key)
        super(DbQuestion, self).__init__(*args, **kwargs)

    @staticmethod
    def get_by_index(index):
        key = str(index)
        return DbQuestion.get_by_key_name(key)

    @staticmethod
    def get_random():
        # Fetch the lowest index
        query = DbQuestion.all()
        query.order('index')
        lowest_index = list(query.run(limit=1))[0].index

        # Fetch the highest index
        query = DbQuestion.all()
        query.order('-index')
        highest_index = list(query.run(limit=1))[0].index

        # Keep trying random numbers until a question is found
        while True:
            index = random.randint(lowest_index, highest_index)
            logging.info("Lowest %d / Highest %d / Random %d" % (lowest_index, highest_index, index))
            result = DbQuestion.get_by_index(index)
            if result:
                return result

    @staticmethod
    def get_highest_index():
        # Fetch the highest index
        query = DbQuestion.all()
        query.order('-index')
        questions = list(query.run(limit=1))
        if questions:
            return questions[0].index
        return 0

    index = db.IntegerProperty(required=True, indexed=True)
    theme = db.StringProperty(required=True, indexed=True)
    question = db.StringProperty(required=True, indexed=False)
    answer = db.StringProperty(required=True, indexed=False)
    shows = db.IntegerProperty(indexed=False)
    likes = db.IntegerProperty(indexed=False)

    def get_just_answers(self):
        return [answer.text.upper() for answer in self.answers]

    def get_answers(self):
        return answers

    def to_python_code(self):
        q = '    q = DbQuestion(index=%d, theme="%s", question="%s", answer="%s", shows=%s, likes=%s); q.put();' % (self.index, self.theme, self.question.replace('"', '\\"'), self.answer, str(self.shows) if self.shows else "None", str(self.likes) if self.likes else "None")
        return q + string.join([' DbAnswer(question=q,text="%s",is_approved=True).put();' % answer.text for answer in self.answers if answer.text])

    def __str__(self):
        from pprint import PrettyPrinter
        return '<%s: %s>' % (self.__class__.__name__, PrettyPrinter().pformat(self.__dict__))

class DbAnswer(db.Model):
    question = db.Reference(DbQuestion, collection_name='answers')

    text = db.StringProperty(required=True, indexed=False)
    picks = db.IntegerProperty()
    likes = db.IntegerProperty()
    shows = db.IntegerProperty()
    is_approved = db.BooleanProperty()
    created = db.DateTimeProperty(auto_now_add=True)

def export_questions():
    query = DbQuestion.all()
    query.order('index')
    offset = 0
    while True:
        entries = query.fetch(limit=100, offset=offset)
        offset += 100
        if not entries:
            return
        for entry in entries:
            yield entry.to_python_code()

def import_questions_if_needed():
    if DbQuestion.all(keys_only=True).count(1) > 0:
        return
    logging.info("No questions found, importing them")
    _import_questions()
    logging.info("Question import complete")
    # Wait for eventual consistency
    while DbQuestion.all(keys_only=True).count(1) == 0:
        import time
        time.sleep(0.5)

def delete_all_questions():
    logging.info("Deleting all questions")
    query = DbQuestion.all(keys_only=True)
    while True:
        entries = query.fetch(1000)
        if not entries:
            break
        db.delete(entries)

def _import_questions():
    q = DbQuestion(index=1, theme="Seahawks", question="What is the last name of number 89 on the Seahawks 2014 football team?", answer="Baldwin", shows=None, likes=None); q.put(); DbAnswer(question=q,text="Tate",is_approved=True).put(); DbAnswer(question=q,text="Willson",is_approved=True).put(); DbAnswer(question=q,text="Simon",is_approved=True).put(); DbAnswer(question=q,text="Chancellor",is_approved=True).put(); DbAnswer(question=q,text="Lynch",is_approved=True).put();
    q = DbQuestion(index=2, theme="Seahawks", question="What is the name of the Seahawks drum line?  Blue ________", answer="Thunder", shows=None, likes=None); q.put(); DbAnswer(question=q,text="Lightning",is_approved=True).put(); DbAnswer(question=q,text="Rumble",is_approved=True).put(); DbAnswer(question=q,text="Quake",is_approved=True).put();
    q = DbQuestion(index=3, theme="Seahawks", question="Before a name-the-team contest led to the selection of 'Seahawks', what were they originally to be called?", answer="Kings", shows=None, likes=None); q.put(); DbAnswer(question=q,text="Sounders",is_approved=True).put(); DbAnswer(question=q,text="Surge",is_approved=True).put(); DbAnswer(question=q,text="Storm",is_approved=True).put(); DbAnswer(question=q,text="Flight",is_approved=True).put();
    q = DbQuestion(index=4, theme="Seahawks", question="What year did the Seahawks enter the NFL?", answer="1976", shows=None, likes=None); q.put(); DbAnswer(question=q,text="1974",is_approved=True).put(); DbAnswer(question=q,text="1977",is_approved=True).put(); DbAnswer(question=q,text="1978",is_approved=True).put(); DbAnswer(question=q,text="1980",is_approved=True).put();
    q = DbQuestion(index=5, theme="Seahawks", question="What is the name given to the Seahawk's Marshawn Lynch's 67-yard run against the New Orleans Saints?", answer="Beastquake", shows=None, likes=None); q.put(); DbAnswer(question=q,text="Beastmode",is_approved=True).put(); DbAnswer(question=q,text="Earthquake",is_approved=True).put(); DbAnswer(question=q,text="Beast",is_approved=True).put();
    q = DbQuestion(index=6, theme="Religion/Mythology", question="What is the only domesticated animal not mentioned in the Bible?", answer="Cat", shows=None, likes=None); q.put(); DbAnswer(question=q,text="Dog",is_approved=True).put(); DbAnswer(question=q,text="Horse",is_approved=True).put(); DbAnswer(question=q,text="Goat",is_approved=True).put(); DbAnswer(question=q,text="Sheep",is_approved=True).put();
    q = DbQuestion(index=7, theme="Religion/Mythology", question="What word appears exactly 773,692 times in the King James Bible?", answer="Amen", shows=None, likes=None); q.put(); DbAnswer(question=q,text="Lord",is_approved=True).put(); DbAnswer(question=q,text="Jesus",is_approved=True).put(); DbAnswer(question=q,text="Israel",is_approved=True).put(); DbAnswer(question=q,text="Water",is_approved=True).put();
    q = DbQuestion(index=8, theme="Religion/Mythology", question="What follows mass as the most popular activity in U.S. Catholic churches?", answer="Bingo", shows=None, likes=None); q.put(); DbAnswer(question=q,text="Brunch",is_approved=True).put(); DbAnswer(question=q,text="Youth Group",is_approved=True).put();
    q = DbQuestion(index=9, theme="Religion/Mythology", question="What Arab nation has the highest percentage of Christians?", answer="Lebanon", shows=None, likes=None); q.put(); DbAnswer(question=q,text="Syria",is_approved=True).put(); DbAnswer(question=q,text="Saudi Arabia",is_approved=True).put();
    q = DbQuestion(index=10, theme="Religion/Mythology", question="What symbol did St. Patrick use to explain his theory of the Holy Trinity?", answer="Shamrock", shows=None, likes=None); q.put(); DbAnswer(question=q,text="Cross",is_approved=True).put(); DbAnswer(question=q,text="Fish",is_approved=True).put();
    q = DbQuestion(index=11, theme="Religion/Mythology", question="What country boasts the largest number of Catholics?", answer="Brazil", shows=None, likes=None); q.put(); DbAnswer(question=q,text="United States",is_approved=True).put(); DbAnswer(question=q,text="Italy",is_approved=True).put();
    q = DbQuestion(index=12, theme="Religion/Mythology", question="What name has been shared by the most popes?", answer="John", shows=None, likes=None); q.put(); DbAnswer(question=q,text="Francis",is_approved=True).put(); DbAnswer(question=q,text="Henry",is_approved=True).put();
    q = DbQuestion(index=13, theme="Religion/Mythology", question="Which other wicked city besides Gomorrah was destroyed by God in Genesis?", answer="Sodom", shows=None, likes=None); q.put(); DbAnswer(question=q,text="Jeruselum",is_approved=True).put(); DbAnswer(question=q,text="Corinth",is_approved=True).put();
    q = DbQuestion(index=14, theme="Religion/Mythology", question="What two European countries claim two-thirds of the world's 2,000-plus registered saints?", answer="Italy and France", shows=None, likes=None); q.put(); DbAnswer(question=q,text="England and France",is_approved=True).put();
    q = DbQuestion(index=15, theme="Religion/Mythology", question="What fruit is depicted in Leonardo's Last Supper, even though it did not arrive in the Holy Land until long after Jesus' death?", answer="Orange", shows=None, likes=None); q.put(); DbAnswer(question=q,text="Fig",is_approved=True).put(); DbAnswer(question=q,text="Lemon",is_approved=True).put(); DbAnswer(question=q,text="Lime",is_approved=True).put();
    q = DbQuestion(index=16, theme="Religion/Mythology", question="What religious movement began with Martin Luther's attack on the sale of indulgences?", answer="Reformation", shows=None, likes=None); q.put(); DbAnswer(question=q,text="Protestation",is_approved=True).put(); DbAnswer(question=q,text="Enlightenment",is_approved=True).put();
    q = DbQuestion(index=17, theme="Religion/Mythology", question="What Saudi Arabian city was the birthplace of the prophet Muhammad?", answer="Mecca", shows=None, likes=None); q.put(); DbAnswer(question=q,text="Baghdad",is_approved=True).put(); DbAnswer(question=q,text="Babylon",is_approved=True).put();
    q = DbQuestion(index=18, theme="Religion/Mythology", question="What storied city on the Euphrates River was 55 miles south of Baghdad?", answer="Babylon", shows=None, likes=None); q.put(); DbAnswer(question=q,text="Mecca",is_approved=True).put(); DbAnswer(question=q,text="Jeruselum",is_approved=True).put();
    q = DbQuestion(index=19, theme="Religion/Mythology", question="What biblical place name means \"pleasure\"?", answer="Eden", shows=None, likes=None); q.put(); DbAnswer(question=q,text="Solomon's temple",is_approved=True).put(); DbAnswer(question=q,text="Babylon",is_approved=True).put();
    q = DbQuestion(index=20, theme="Religion/Mythology", question="What city did Napoleon occupy in 1798, sending Pope Pius VI to the south of France?", answer="Rome", shows=None, likes=None); q.put(); DbAnswer(question=q,text="Tripoli",is_approved=True).put(); DbAnswer(question=q,text="Venice",is_approved=True).put();
    q = DbQuestion(index=21, theme="Religion/Mythology", question="What was the world's principal Christian city before it fell to the Ottoman Turks in 1453?", answer="Constantinople", shows=None, likes=None); q.put(); DbAnswer(question=q,text="Rome",is_approved=True).put();
    q = DbQuestion(index=22, theme="Religion/Mythology", question="What nation's Catholics saw the Pope make a triumphant homecoming visit in 1980?", answer="Poland", shows=None, likes=None); q.put(); DbAnswer(question=q,text="Hungary",is_approved=True).put(); DbAnswer(question=q,text="Romania",is_approved=True).put();
    q = DbQuestion(index=23, theme="Religion/Mythology", question="What animal is mentioned most frequently in both the New and Old Testaments?", answer="Sheep", shows=None, likes=None); q.put(); DbAnswer(question=q,text="Donkey",is_approved=True).put(); DbAnswer(question=q,text="Colt",is_approved=True).put(); DbAnswer(question=q,text="Goat",is_approved=True).put();
    q = DbQuestion(index=24, theme="Religion/Mythology", question="What biblical epic was the top-grossing movie of the 1950's?", answer="Ten Commandments", shows=None, likes=None); q.put(); DbAnswer(question=q,text="Ben Hur",is_approved=True).put();
    q = DbQuestion(index=25, theme="Religion/Mythology", question="Who was the first pope? St. ______", answer="Peter", shows=None, likes=None); q.put(); DbAnswer(question=q,text="James",is_approved=True).put(); DbAnswer(question=q,text="Patrick",is_approved=True).put();
    q = DbQuestion(index=26, theme="Religion/Mythology", question="How many 'days and nights' did Jonah spend in the belly of the whale?", answer="Three", shows=None, likes=None); q.put(); DbAnswer(question=q,text="Five",is_approved=True).put(); DbAnswer(question=q,text="Seven",is_approved=True).put();
    q = DbQuestion(index=27, theme="Religion/Mythology", question="According to the Bible, what substance was used to caulk Noah's ark and to seal the basket in which the infant Moses was set adrift on the Nile?", answer="Pitch or natural asphalt", shows=None, likes=None); q.put();
    q = DbQuestion(index=28, theme="Religion/Mythology", question="What language is Jesus believed to have spoken?", answer="Aramaic", shows=None, likes=None); q.put(); DbAnswer(question=q,text="Hebrew",is_approved=True).put(); DbAnswer(question=q,text="Greek",is_approved=True).put();
    q = DbQuestion(index=29, theme="Religion/Mythology", question="According to the Bible, what weapons was the Philistine giant Goliath carrying when he was slain by David?", answer="A sword and a spear", shows=None, likes=None); q.put();
    q = DbQuestion(index=30, theme="Religion/Mythology", question="According to the Bible, how many pearly gates are there?", answer="12", shows=None, likes=None); q.put();
    q = DbQuestion(index=31, theme="Religion/Mythology", question="What were the names of the three wise men?", answer="Balthazar, Caspar and Melchior", shows=None, likes=None); q.put();
    q = DbQuestion(index=32, theme="Religion/Mythology", question="Who were the parents of King Solomon?", answer="David and Bathsheba", shows=None, likes=None); q.put();
    q = DbQuestion(index=33, theme="Religion/Mythology", question="Name the two books of the Bible named after women.", answer="Ruth and Esther", shows=None, likes=None); q.put();
    q = DbQuestion(index=34, theme="Religion/Mythology", question="In the Old Testament, who was Jezebel's husband?", answer="Ahab, King of Israel", shows=None, likes=None); q.put();
    q = DbQuestion(index=35, theme="Food", question="What milk product did the U.S. Agriculture Department propose as a substitute for meat in school lunches, in 1996?", answer="Yogurt", shows=None, likes=None); q.put();
    q = DbQuestion(index=36, theme="Food", question="What breakfast cereal was Sonny the Cuckoo Bird \"cuckoo for\"?", answer="Cocoa Puffs", shows=None, likes=None); q.put();
    q = DbQuestion(index=37, theme="Food", question="On what vegetable did an ancient Egyptian place his right hand when taking an oath?", answer="onion", shows=None, likes=None); q.put();
    q = DbQuestion(index=38, theme="Food", question="How many flowers are in the design stamped on each side of an Oreo cookie?", answer="Twelve", shows=None, likes=None); q.put();
    q = DbQuestion(index=39, theme="Food", question="Black-eyed peas are not peas. What are they?", answer="Beans", shows=None, likes=None); q.put();
    q = DbQuestion(index=40, theme="Food", question="Under what name did the Domino's Pizza chain get its start?", answer="DomNick's", shows=None, likes=None); q.put();
    q = DbQuestion(index=41, theme="Food", question="What was margarine called when it was first marketed in England?", answer="Butterine", shows=None, likes=None); q.put();
    q = DbQuestion(index=42, theme="Food", question="What are the two top selling spices in the world?", answer="Pepper and mustard", shows=None, likes=None); q.put();
    q = DbQuestion(index=43, theme="Food", question="What was the name of Cheerios when it was first marketed 50 years ago?", answer="Cheerioats", shows=None, likes=None); q.put();
    q = DbQuestion(index=44, theme="Food", question="What flavor of ice cream did Baskin-Robbins introduce to commemorate America's landing on the moon on July 20, 1969?", answer="Lunar Cheesecake", shows=None, likes=None); q.put();
    q = DbQuestion(index=45, theme="Food", question="What is the most widely eaten fish in the world?", answer="Herring", shows=None, likes=None); q.put();
    q = DbQuestion(index=46, theme="Food", question="What is the name of the evergreen shrub from which we get capers?", answer="caper bush", shows=None, likes=None); q.put();
    q = DbQuestion(index=47, theme="Food", question="What animals milk is used to make authentic Italian mozzarella cheese?", answer="water buffalo's", shows=None, likes=None); q.put();
    q = DbQuestion(index=48, theme="Food", question="What nation produces two thirds of the world's vanilla?", answer="Madagascar", shows=None, likes=None); q.put();
    q = DbQuestion(index=49, theme="Food", question="What was the drink we know as the Bloody Mary originally called?", answer="Red Snapper", shows=None, likes=None); q.put();
    q = DbQuestion(index=50, theme="Food", question="What was the first commercially manufactured breakfast cereal?", answer="Shredded Wheat", shows=None, likes=None); q.put();
    q = DbQuestion(index=51, theme="Food", question="When Birdseye introduced the first frozen food in 1930, what did the company call it?", answer="Frosted Food", shows=None, likes=None); q.put();
    q = DbQuestion(index=52, theme="Food", question="What American city produces most of the egg rolls sold in grocery stores in the United States?", answer="Houston, Texas", shows=None, likes=None); q.put();
    q = DbQuestion(index=53, theme="Food", question="What was the first of H.J. Heinz' \"57 varieties\"?", answer="Horseradish", shows=None, likes=None); q.put();
    q = DbQuestion(index=54, theme="Food", question="What is the literal meaning of the Italian word linguine?", answer="Little tongues", shows=None, likes=None); q.put();
    q = DbQuestion(index=55, theme="Food", question="Where did the pineapple plant originate?", answer="South America", shows=None, likes=None); q.put();
    q = DbQuestion(index=56, theme="Food", question="What recipe, first published 50 years ago, has been requested most frequently through the years by the readers of \"Better Homes and Garden\"?", answer="Hamburger Pie", shows=None, likes=None); q.put();
    q = DbQuestion(index=57, theme="Food", question="What is the only essential vitamin not found in the white potato?", answer="Vitamin A", shows=None, likes=None); q.put();
    q = DbQuestion(index=58, theme="Food", question="What food is the leading source of salmonella poisoning?", answer="Chicken", shows=None, likes=None); q.put();
    q = DbQuestion(index=59, theme="Food", question="What company first condensed soup in 1898?", answer="Campbell's", shows=None, likes=None); q.put();
    q = DbQuestion(index=60, theme="Food", question="What nutty legume accounts for one sixth of the world's vegetable oil production?", answer="peanut", shows=None, likes=None); q.put();
    q = DbQuestion(index=61, theme="Food", question="What country saw the cultivation of the first potato, in 200 A.D.?", answer="South America", shows=None, likes=None); q.put();
    q = DbQuestion(index=62, theme="Food", question="What type of lettuce was called Crisphead until the 1920s?", answer="Iceberg lettuce", shows=None, likes=None); q.put();
    q = DbQuestion(index=63, theme="Food", question="What tree gives us prunes?", answer="plum tree", shows=None, likes=None); q.put();
    q = DbQuestion(index=64, theme="Food", question="What type of chocolate was first developed for public consumption in Vevey, Switzerland in 1875?", answer="Milk Chocolate", shows=None, likes=None); q.put();
    q = DbQuestion(index=65, theme="Food", question="What added ingredient keeps confectioners' sugar from clumping?", answer="Corn starch", shows=None, likes=None); q.put();
    q = DbQuestion(index=66, theme="Food", question="What edible comes in crimmini, morel, oyster and wood ear varieties?", answer="Mushrooms", shows=None, likes=None); q.put();
    q = DbQuestion(index=67, theme="Food", question="What newly-imported substance caused the first major outbreak of tooth decay in Europe, in the1500's?", answer="Sugar", shows=None, likes=None); q.put();
    q = DbQuestion(index=68, theme="Food", question="What ingredient in fresh milk is eventually devoured by bacteria, causing the sour taste?", answer="Lactose", shows=None, likes=None); q.put();
    q = DbQuestion(index=69, theme="Food", question="What uncooked meat is a trichina worm most likely to make a home in?", answer="Pork", shows=None, likes=None); q.put();
    q = DbQuestion(index=70, theme="Food", question="What baking ingredient, sprayed at high pressure, did the U.S. Air Force replace its toxic paint stripper with?", answer="Baking soda", shows=None, likes=None); q.put();
    q = DbQuestion(index=71, theme="Food", question="What staple is laced with up to 16 additives including plaster of paris, to stay fresh?", answer="Bread", shows=None, likes=None); q.put();
    q = DbQuestion(index=72, theme="Food", question="What falling fruit supposedly inspired Isaac Newton to write the laws of gravity?", answer="An Apple", shows=None, likes=None); q.put();
    q = DbQuestion(index=73, theme="Food", question="What method of preserving food did the Incas first use, on potatoes?", answer="Freeze-drying", shows=None, likes=None); q.put();
    q = DbQuestion(index=74, theme="Food", question="What drupaceous fruit were Hawaiian women once forbidden by law to eat?", answer="coconut", shows=None, likes=None); q.put();
    q = DbQuestion(index=75, theme="Food", question="What hit the market alongside spinach as the first frozen veggies?", answer="Peas", shows=None, likes=None); q.put();
    q = DbQuestion(index=76, theme="Food", question="How many sizes of chicken eggs does the USDA recognize, including peewee?", answer="Six", shows=None, likes=None); q.put();
    q = DbQuestion(index=77, theme="Food", question="What are de-headed, de-veined an sorted by size in a laitram machine?", answer="Shrimp", shows=None, likes=None); q.put();
    q = DbQuestion(index=78, theme="Food", question="What's the only fish that produces real caviar, according to the FDA?", answer="Sturgeon", shows=None, likes=None); q.put();
    q = DbQuestion(index=79, theme="Food", question="What type of egg will yield 11 and one-half average-size omelettes?", answer="An Ostrich egg", shows=None, likes=None); q.put();
    q = DbQuestion(index=80, theme="Food", question="What's the groundnut better known as?", answer="peanut", shows=None, likes=None); q.put();
    q = DbQuestion(index=81, theme="Food", question="What crystalline salt is frequently used to enhance the flavor to TV dinners?", answer="Monosodium glutamate", shows=None, likes=None); q.put();
    q = DbQuestion(index=82, theme="Food", question="What sticky sweetener was traditionally used as an antiseptic ointment for cuts and burns?", answer="Honey", shows=None, likes=None); q.put();
    q = DbQuestion(index=83, theme="Food", question="What should your diet be high in to lessen the chance of colon cancer, according to a 1990 study?", answer="Fiber", shows=None, likes=None); q.put();
    q = DbQuestion(index=84, theme="Food", question="What nut do two-thirds of its U. S. producers sell through Blue Diamond?", answer="Almond", shows=None, likes=None); q.put();
    q = DbQuestion(index=85, theme="Food", question="What type of oven will not brown foods?", answer="Microwave oven", shows=None, likes=None); q.put();
    q = DbQuestion(index=86, theme="Food", question="What type of food did Linda McCartney launch?", answer="Vegetarian food", shows=None, likes=None); q.put();
    q = DbQuestion(index=87, theme="Food", question="What type of tree leaves are the only food that a koala bear will eat?", answer="Eucalyptus", shows=None, likes=None); q.put();
    q = DbQuestion(index=88, theme="Food", question="Which country in Europe consumes more spicy Mexican food than any other?", answer="Norway", shows=None, likes=None); q.put();
    q = DbQuestion(index=89, theme="Food", question="The FDA approved what fat substitute for use in snack foods even though there were reports of side affects like cramps and diarrhea?", answer="Olestra", shows=None, likes=None); q.put();
    q = DbQuestion(index=90, theme="Food", question="Federal labeling regulations require how much caffeine be removed from coffee for it to be called decaffeinated?", answer="Ninety seven percent", shows=None, likes=None); q.put();
    q = DbQuestion(index=91, theme="Food", question="What famous Greek once advised = \"Let your food be your medicine, and your medicine be your food\"?", answer="Hippocrates", shows=None, likes=None); q.put();
    q = DbQuestion(index=92, theme="Food", question="Chicken is the leading cause of what food born illness?", answer="Salmonella poisoning", shows=None, likes=None); q.put();
    q = DbQuestion(index=93, theme="Food", question="Who invented Margarine in 1868?", answer="Hyppolyte Merge-mouries", shows=None, likes=None); q.put();
    q = DbQuestion(index=94, theme="Food", question="What group of people were the first to use freeze-drying on potatoes?", answer="Incas", shows=None, likes=None); q.put();
    q = DbQuestion(index=95, theme="Food", question="What was the Teenage Mutant Ninja Turtles favorite food?", answer="Pizza", shows=None, likes=None); q.put();
    q = DbQuestion(index=96, theme="Food", question="What food was considered the food of the Gods, and was said to bring eternal life to anyone who ate it?", answer="Ambrosia", shows=None, likes=None); q.put();
    q = DbQuestion(index=97, theme="Food", question="What was the convenience food that Joel Cheek developed?", answer="Instant Coffee", shows=None, likes=None); q.put();
    q = DbQuestion(index=98, theme="Food", question="The song, Food, Glorious Food, was featured in which musical?", answer="Oliver", shows=None, likes=None); q.put();
    q = DbQuestion(index=99, theme="Food", question="Of the Worlds food crops, what percentage is pollinated by insects?", answer="80 percent", shows=None, likes=None); q.put();
    q = DbQuestion(index=100, theme="Food", question="The Giant panda's favorite food is what?", answer="Bamboo shoots", shows=None, likes=None); q.put();
    q = DbQuestion(index=101, theme="Food", question="Which entertainer on Conan O'Brien's show, choose NBC cafeteria chicken over his own brand in a blind taste test?", answer="Kenny Rogers", shows=None, likes=None); q.put();
    q = DbQuestion(index=102, theme="Food", question="What drink was sold as Diastoid when first introduced?", answer="Malted milk", shows=None, likes=None); q.put();
    q = DbQuestion(index=103, theme="Food", question="What type of micro organism makes up the base of marine and freshwater food chains?", answer="Plankton", shows=None, likes=None); q.put();
    q = DbQuestion(index=104, theme="Food", question="What type of creature builds a lodge in which to store food, rear its young, and pass the winter?", answer="Beaver", shows=None, likes=None); q.put();
    q = DbQuestion(index=105, theme="Food", question="What fruit or vegetable was dubbed the FlavrSavr and was the first genetically engineered food sold in the United States?", answer="tomato", shows=None, likes=None); q.put();
    q = DbQuestion(index=106, theme="Food", question="What fitness guru appeared as a dancing meatball in an Italian TV commercial as an art student?", answer="Richard Simmons", shows=None, likes=None); q.put();
    q = DbQuestion(index=107, theme="Food", question="What Olympic athlete could not run the 200-meter final in the 92 Olympics because of food poisoning?", answer="Michael Johnson", shows=None, likes=None); q.put();
    q = DbQuestion(index=108, theme="Food", question="What morning food has a name derived from the German word for stirrup?", answer="Bagel", shows=None, likes=None); q.put();
    q = DbQuestion(index=109, theme="Food", question="In 1904, what food product was renamed Post Toasties cereal because the clergy objected to the original name?", answer="Elijah's Manna", shows=None, likes=None); q.put();
    q = DbQuestion(index=110, theme="Food", question="Which country does Rioja Wine come from?", answer="Spain", shows=None, likes=None); q.put();
    q = DbQuestion(index=111, theme="Food", question="The juice of which fruit will you find in a bloody mary?", answer="Tomato", shows=None, likes=None); q.put();
    q = DbQuestion(index=112, theme="Food", question="Homer Simpson drinks Which brand of beer regularly?", answer="Duff", shows=None, likes=None); q.put();
    q = DbQuestion(index=113, theme="Food", question="What is the main ingredient of paella?", answer="Rice", shows=None, likes=None); q.put();
    q = DbQuestion(index=114, theme="Food", question="What would you call a segment of garlic?", answer="Clove", shows=None, likes=None); q.put();
    q = DbQuestion(index=115, theme="Food", question="A canteloupe is what kind of fruit?", answer="Melon", shows=None, likes=None); q.put();
    q = DbQuestion(index=116, theme="Food", question="Sticky and sweet this food is produced in a hive?", answer="Honey", shows=None, likes=None); q.put();
    q = DbQuestion(index=117, theme="Food", question="This dairy product tastes good on crackers and sandwiches or on its own?", answer="Cheese", shows=None, likes=None); q.put();
    q = DbQuestion(index=118, theme="Food", question="In the dish of Beef Wellington, in what is the beef wrapped?", answer="Pastry", shows=None, likes=None); q.put();
    q = DbQuestion(index=119, theme="Food", question="What is The Teenage Mutant Ninja Turtles favourite food?", answer="Pizza", shows=None, likes=None); q.put();
    q = DbQuestion(index=120, theme="Food", question="What is the main vegetable ingredient in the dish Borsht?", answer="Beetroot", shows=None, likes=None); q.put();
    q = DbQuestion(index=121, theme="Food", question="Sauerkraut is pickled what?", answer="Cabbage", shows=None, likes=None); q.put();
    q = DbQuestion(index=122, theme="Food", question="What vegetable is also known as zucchini in the USA?", answer="Courgette", shows=None, likes=None); q.put();
    q = DbQuestion(index=123, theme="Food", question="This fruit goes into the liqueur Kirsch?", answer="Cherry", shows=None, likes=None); q.put();
    q = DbQuestion(index=124, theme="Food", question="A bloomer is what type of food?", answer="Bread", shows=None, likes=None); q.put();
    q = DbQuestion(index=125, theme="Food", question="Which is the fruit that contains the most calories?", answer="Avocado pear", shows=None, likes=None); q.put();
    q = DbQuestion(index=126, theme="Food", question="What is lava bread?", answer="Seaweed", shows=None, likes=None); q.put();
    q = DbQuestion(index=127, theme="Food", question="What fruit grows on the blackthorn tree?", answer="Sloe", shows=None, likes=None); q.put();
    q = DbQuestion(index=128, theme="Food", question="Which food has a name which means on a skewer?", answer="Kebab", shows=None, likes=None); q.put();
    q = DbQuestion(index=129, theme="Food", question="In a Mcdonald's Big Mac how many pieces of bun are there?", answer="Three", shows=None, likes=None); q.put();
    q = DbQuestion(index=130, theme="Food", question="Oyster, Chestnut, or Shitaki are types of which vegetable?", answer="Mushrooms", shows=None, likes=None); q.put();
    q = DbQuestion(index=131, theme="Food", question="A Calzone Is A Folded Stuffed What?", answer="Pizza", shows=None, likes=None); q.put();
    q = DbQuestion(index=132, theme="Food", question="Which country invented the Marmite alternative - Veggie mite?", answer="Australia", shows=None, likes=None); q.put();
    q = DbQuestion(index=133, theme="Food", question="Which country does the dish Mousakka come from?", answer="Greece", shows=None, likes=None); q.put();
    q = DbQuestion(index=134, theme="Food", question="Which fruit served with cream is eaten during the summer tennis tournament Wimbledon?", answer="Strawberries", shows=None, likes=None); q.put();
    q = DbQuestion(index=135, theme="Food", question="Apart from potato What is the other main ingredient of Bubble and Squeak?", answer="Cabbage", shows=None, likes=None); q.put();
    q = DbQuestion(index=136, theme="Food", question="Which food was popular with Popeye the Sailor?", answer="Spinach", shows=None, likes=None); q.put();
    q = DbQuestion(index=137, theme="Food", question="What is Scooby Doo`s favourite food?", answer="Scooby Snacks", shows=None, likes=None); q.put();
    q = DbQuestion(index=138, theme="Food", question="What is the only fruit that grows its seeds on the outside?", answer="Strawberry", shows=None, likes=None); q.put();
    q = DbQuestion(index=139, theme="Food", question="What other names are sardines known by?", answer="Pilchards", shows=None, likes=None); q.put();
    q = DbQuestion(index=140, theme="Food", question="Which city gave its name to a three-coloured Neapolitan ice-cream?", answer="Naples", shows=None, likes=None); q.put();
    q = DbQuestion(index=141, theme="Food", question="What would you be drinking if you were drinking Earl Grey?", answer="Tea", shows=None, likes=None); q.put();
    q = DbQuestion(index=142, theme="Food", question="What are Pontefract cakes made from?", answer="Liquorice", shows=None, likes=None); q.put();
    q = DbQuestion(index=143, theme="Food", question="What is another name for almond paste?", answer="Marzipan", shows=None, likes=None); q.put();
    q = DbQuestion(index=144, theme="Food", question="What name can be a lettuce or a mass of floating frozen water?", answer="Iceberg", shows=None, likes=None); q.put();
    q = DbQuestion(index=145, theme="Food", question="What's Sauerkraut's main ingredient?", answer="Cabbage", shows=None, likes=None); q.put();
    q = DbQuestion(index=146, theme="Food", question="What's the only rock edible to man?", answer="Salt", shows=None, likes=None); q.put();
    q = DbQuestion(index=147, theme="Food", question="What type of salad do you need apple, celery, walnuts, raisins and mayonnaise mixed together?", answer="Waldorf Salad", shows=None, likes=None); q.put();
    q = DbQuestion(index=148, theme="Food", question="Which fruit also shares its name with Gwyneth Paltrow's daughter?", answer="Apple", shows=None, likes=None); q.put();
    q = DbQuestion(index=149, theme="Food", question="From which animal does haggis come?", answer="Sheep", shows=None, likes=None); q.put();
    q = DbQuestion(index=150, theme="Food", question="In cockney rhyming slang what is \"Ruby Murray\"?", answer="Curry", shows=None, likes=None); q.put();
    q = DbQuestion(index=151, theme="Food", question="What cake do you keep a layer of to eat at the christening of your first child?", answer="Wedding Cake", shows=None, likes=None); q.put();
    q = DbQuestion(index=152, theme="Food", question="Which brand of frozen ice cream cone was advertised to the tune of Italian song \"O Sole Mio\"?", answer="Cornetto", shows=None, likes=None); q.put();
    q = DbQuestion(index=153, theme="Food", question="If I take two apples out of a basket containing six apples how many apples do I have ?", answer="Two", shows=None, likes=None); q.put();
    q = DbQuestion(index=154, theme="Food", question="Which fruit does one of Bob Geldofs' daughter share a name with?", answer="Peaches", shows=None, likes=None); q.put();
    q = DbQuestion(index=155, theme="Food", question="In Eggs Florentine which vegetable is a main ingredient?", answer="Spinach", shows=None, likes=None); q.put();
    q = DbQuestion(index=156, theme="Food", question="In a French restaurant what would you be eating if you chose escargots?", answer="Snails", shows=None, likes=None); q.put();
    q = DbQuestion(index=157, theme="Food", question="Which meat is usally in a Shish Kebab?", answer="Lamb", shows=None, likes=None); q.put();
    q = DbQuestion(index=158, theme="Food", question="What flavour is Ouzo?", answer="Aniseed", shows=None, likes=None); q.put();
    q = DbQuestion(index=159, theme="Food", question="A crapulous person is full of what?", answer="Alcohol", shows=None, likes=None); q.put();
    q = DbQuestion(index=160, theme="Food", question="What Italian Cheese usually tops a pizza?", answer="Mozzarella", shows=None, likes=None); q.put();
    q = DbQuestion(index=161, theme="Food", question="Port Salut is what?", answer="Cheese", shows=None, likes=None); q.put();
    q = DbQuestion(index=162, theme="Food", question="Who talked of eating human liver washed down with Chianti?", answer="Hannibal Lecter", shows=None, likes=None); q.put();
    q = DbQuestion(index=163, theme="Food", question="Who, according to the TV commercial, \"makes exceedingly good cakes\"?", answer="Mr Kipling", shows=None, likes=None); q.put();
    q = DbQuestion(index=164, theme="Food", question="What vegetable is sold mainly before 30th October?", answer="Pumpkin", shows=None, likes=None); q.put();
    q = DbQuestion(index=165, theme="Food", question="Whats the english translation for the french word crepe?", answer="Pancake", shows=None, likes=None); q.put();
    q = DbQuestion(index=166, theme="Food", question="What is a macadamia?", answer="Nut", shows=None, likes=None); q.put();
    q = DbQuestion(index=167, theme="Food", question="In ancient Egypt what was liquorice used for?", answer="Medicine", shows=None, likes=None); q.put();
    q = DbQuestion(index=168, theme="Food", question="What type of thin pancake is eaten in Mexico?", answer="Tortilla", shows=None, likes=None); q.put();
    q = DbQuestion(index=169, theme="Food", question="If steak was blue how would it be cooked?", answer="Very Rare", shows=None, likes=None); q.put();
    q = DbQuestion(index=170, theme="Food", question="Baked beans are made from which beans?", answer="Haricot", shows=None, likes=None); q.put();
    q = DbQuestion(index=171, theme="Food", question="What are small cubes of toasted or fried bread?", answer="Croutons", shows=None, likes=None); q.put();
    q = DbQuestion(index=172, theme="Food", question="What would you call a cluster of bananas?", answer="A hand", shows=None, likes=None); q.put();
    q = DbQuestion(index=173, theme="Food", question="What nuts are used to flavour amaretto?", answer="Almonds", shows=None, likes=None); q.put();
    q = DbQuestion(index=174, theme="Food", question="If you had frijoles refritos in a Mexican restaurant it would be refried what?", answer="beans", shows=None, likes=None); q.put();
    q = DbQuestion(index=175, theme="Food", question="This city is famous for its oranges?", answer="Seville", shows=None, likes=None); q.put();
    q = DbQuestion(index=176, theme="Food", question="Which celebrity chef was nicknamed 'The Naked Chef'?", answer="Jamie Oliver", shows=None, likes=None); q.put();
    q = DbQuestion(index=177, theme="Food", question="What daily vegetable do typical boxer's ears look like?", answer="Cauliflower", shows=None, likes=None); q.put();
    q = DbQuestion(index=178, theme="Food", question="What's a small pickled cucumber?", answer="Gherkin", shows=None, likes=None); q.put();
    q = DbQuestion(index=179, theme="Food", question="What's cockney rhyming slang for eyes?", answer="Mince Pies", shows=None, likes=None); q.put();
    q = DbQuestion(index=180, theme="Food", question="What name's given to a small, deep fried chinese dumpling with a savoury filing?", answer="Won ton", shows=None, likes=None); q.put();
    q = DbQuestion(index=181, theme="Food", question="Which brand of beer features a kangaroo on the packaging?", answer="Fosters", shows=None, likes=None); q.put();
    q = DbQuestion(index=182, theme="Food", question="A mint with a hole?", answer="Polo", shows=None, likes=None); q.put();
    q = DbQuestion(index=183, theme="Food", question="What is advertised on TV with the slogan \"You either Love it or Hate it\"?", answer="Marmite", shows=None, likes=None); q.put();
    q = DbQuestion(index=184, theme="Food", question="In Ancient China what variety of meat was reserved exclusively for the emperor?", answer="Pork", shows=None, likes=None); q.put();
    q = DbQuestion(index=185, theme="Food", question="Which song mentions saveloy, mustard, jelly, custard and sausages in the lyrics?", answer="Food Glorious Food", shows=None, likes=None); q.put();
    q = DbQuestion(index=186, theme="Food", question="Jasmine and long grain are both types of what?", answer="Rice", shows=None, likes=None); q.put();
    q = DbQuestion(index=187, theme="Food", question="What might you be eating at Wimbledon if you had a Cambridge Rival in your mouth?", answer="Strawberry", shows=None, likes=None); q.put();
    q = DbQuestion(index=188, theme="Food", question="What fruit was originally called a Chinese gooseberry", answer="Kiwi Fruit", shows=None, likes=None); q.put();
    q = DbQuestion(index=189, theme="Food", question="What sort of pastry is used to make profiteroles?", answer="Choux", shows=None, likes=None); q.put();
    q = DbQuestion(index=190, theme="Food", question="What is the national dish of Hungary?", answer="Goulash", shows=None, likes=None); q.put();
    q = DbQuestion(index=191, theme="Food", question="Which nut is used to flavour traditional Bakewell Tart?", answer="Almond", shows=None, likes=None); q.put();
    q = DbQuestion(index=192, theme="Food", question="In the dish of Beef Wellington, in what is the beef wrapped?", answer="Pastry", shows=None, likes=None); q.put();
    q = DbQuestion(index=193, theme="Food", question="What is the main vegetable used to make Borsch?", answer="Beetroot", shows=None, likes=None); q.put();
    q = DbQuestion(index=194, theme="Food", question="What is Bombay Duck?", answer="Fish", shows=None, likes=None); q.put();
    q = DbQuestion(index=195, theme="Food", question="Which fruit is used in the making of a Black Forest Gateau?", answer="Black Cherries", shows=None, likes=None); q.put();
    q = DbQuestion(index=196, theme="Food", question="What is included in a BLT sandwich?", answer="Bacon, lettuce and tomato", shows=None, likes=None); q.put();
    q = DbQuestion(index=197, theme="Food", question="The name of what food, when translated, means twice-cooked?", answer="Biscuit", shows=None, likes=None); q.put();
    q = DbQuestion(index=198, theme="Food", question="How many calories are there in a stick of celery?", answer="None", shows=None, likes=None); q.put();
    q = DbQuestion(index=199, theme="Food", question="Which country consumes the most pasta per person per year?", answer="Italy", shows=None, likes=None); q.put();
    q = DbQuestion(index=200, theme="Food", question="What was the favourite food of Paddington Bear?", answer="Marmalade", shows=None, likes=None); q.put();
    q = DbQuestion(index=201, theme="Food", question="Which family of vegatables are Chives from?", answer="Onions", shows=None, likes=None); q.put();
    q = DbQuestion(index=202, theme="Food", question="In the Hansel and Gretel tale what was the wicked witch's house made of?", answer="Gingerbread", shows=None, likes=None); q.put();
    q = DbQuestion(index=203, theme="Food", question="What take-away is traditional in England at the seaside?", answer="Fish and chips", shows=None, likes=None); q.put();
    q = DbQuestion(index=204, theme="Food", question="What meat is Coq au vin made with ?", answer="Chicken", shows=None, likes=None); q.put();
    q = DbQuestion(index=205, theme="Food", question="Which cheese is made in reverse?", answer="Edam", shows=None, likes=None); q.put();
    q = DbQuestion(index=206, theme="Food", question="What variety of banana shares its name with the title of a Bond movie?", answer="Goldfinger", shows=None, likes=None); q.put();
    q = DbQuestion(index=207, theme="Food", question="Conference, Bartlett and Kaiser are all varieties of which fruit?", answer="Pear", shows=None, likes=None); q.put();
    q = DbQuestion(index=208, theme="Food", question="Which product is advertised on TV with the slogan, \"Once you pop you can't stop\"?", answer="Pringles", shows=None, likes=None); q.put();
    q = DbQuestion(index=209, theme="Food", question="What is the official national cheese of Greece?", answer="Feta", shows=None, likes=None); q.put();
    q = DbQuestion(index=210, theme="Food", question="Which variety of orange was named after a Japanese province?", answer="Satsuma", shows=None, likes=None); q.put();
    q = DbQuestion(index=211, theme="Food", question="Marzipan is made from which nuts?", answer="Almonds", shows=None, likes=None); q.put();
    q = DbQuestion(index=212, theme="Food", question="During brewing what is converted into alcohol?", answer="Sugar", shows=None, likes=None); q.put();
    q = DbQuestion(index=213, theme="Food", question="This chick pea puree is flavoured with tahini and served as a dip?", answer="Hummus", shows=None, likes=None); q.put();
    q = DbQuestion(index=214, theme="Food", question="Grolsch lager is from which country?", answer="Holland", shows=None, likes=None); q.put();
    q = DbQuestion(index=215, theme="Food", question="This carbohydrate fruit is high in potassium?", answer="Banana", shows=None, likes=None); q.put();
    q = DbQuestion(index=216, theme="Food", question="What overtook coca-cola as the most well known brand name (in the world) in 1996?", answer="McDonalds", shows=None, likes=None); q.put();
    q = DbQuestion(index=217, theme="Food", question="The 'M' in the McDonalds logo is what colour?", answer="Yellow", shows=None, likes=None); q.put();
    q = DbQuestion(index=218, theme="Food", question="Bacardi Rum's logo features which creature?", answer="Bat", shows=None, likes=None); q.put();
    q = DbQuestion(index=219, theme="Food", question="An egg plant is also known as which vegetable?", answer="Aubergine", shows=None, likes=None); q.put();
    q = DbQuestion(index=220, theme="Food", question="What is a light round bun usually served hot?", answer="Muffin", shows=None, likes=None); q.put();
    q = DbQuestion(index=221, theme="Food", question="What is the plant that wards off vampires?", answer="Garlic", shows=None, likes=None); q.put();
    q = DbQuestion(index=222, theme="Food", question="The Teenage Mutant Ninja Turtles favourite food is?", answer="Pizza", shows=None, likes=None); q.put();
    q = DbQuestion(index=223, theme="Food", question="The main vegetable ingredient in the dish Borsht is what?", answer="Beetroot", shows=None, likes=None); q.put();
    q = DbQuestion(index=224, theme="Food", question="Sauerkraut is pickled what?", answer="Cabbage", shows=None, likes=None); q.put();
    q = DbQuestion(index=225, theme="Food", question="Chicory was a war time substitute for what drink?", answer="Coffee", shows=None, likes=None); q.put();
    q = DbQuestion(index=226, theme="Food", question="What vegetable is also known as zucchini in the USA?", answer="Courgette", shows=None, likes=None); q.put();
    q = DbQuestion(index=227, theme="Food", question="This fruit goes into the liqueur Kirsch?", answer="Cherry", shows=None, likes=None); q.put();
    q = DbQuestion(index=228, theme="Food", question="A bloomer is What type of food?", answer="Bread", shows=None, likes=None); q.put();
    q = DbQuestion(index=229, theme="Food", question="This type of milk is a basic ingredient in Thai cookery?", answer="Coconut milk", shows=None, likes=None); q.put();
    q = DbQuestion(index=230, theme="Food", question="What soft drink uses this slogan, \"What's the worst that could happen\"?", answer="Dr Pepper", shows=None, likes=None); q.put();
    q = DbQuestion(index=231, theme="Food", question="Which is the fruit that contains the most calories?", answer="Avocado pear", shows=None, likes=None); q.put();
    q = DbQuestion(index=232, theme="Food", question="What are dried prunes?", answer="Plums", shows=None, likes=None); q.put();
    q = DbQuestion(index=233, theme="Food", question="The main cereal ingredient of flapkacks (Hudson Bars in USA)?", answer="Oats", shows=None, likes=None); q.put();
    q = DbQuestion(index=234, theme="Food", question="What is the correct spelling of a Cadbury Creame/Creem/Creme/Cream Egg?", answer="Creme", shows=None, likes=None); q.put();
    q = DbQuestion(index=235, theme="Food", question="What is Uganda's staple crop, which each adult consumes over 3 times bodyweight annually?", answer="Bananas", shows=None, likes=None); q.put();
    q = DbQuestion(index=236, theme="Food", question="What's lava bread?", answer="Seaweed", shows=None, likes=None); q.put();
    q = DbQuestion(index=237, theme="Food", question="What fruit grows on the blackthorn tree?", answer="Sloe", shows=None, likes=None); q.put();
    q = DbQuestion(index=238, theme="Food", question="Which two fruits are anagrams of each other?", answer="Lemon & Melon", shows=None, likes=None); q.put();
    q = DbQuestion(index=239, theme="Food", question="Homer Simpson drinks what brand of beer?", answer="Duff", shows=None, likes=None); q.put();
    q = DbQuestion(index=240, theme="Food", question="A crapulous person is full of what?", answer="Acohol", shows=None, likes=None); q.put();
    q = DbQuestion(index=241, theme="Food", question="What spanish drink consists of sweet red wine, lemonade or soda water and decorated with fruit?", answer="Sangria", shows=None, likes=None); q.put();
    q = DbQuestion(index=242, theme="Food", question="This spirit is the base for a Black Russian cocktail?", answer="Vodka", shows=None, likes=None); q.put();
    q = DbQuestion(index=243, theme="Food", question="What country is home to Grolsch lager?", answer="Holland", shows=None, likes=None); q.put();
    q = DbQuestion(index=244, theme="Food", question="A crapulous person is full of what?", answer="Alcohol", shows=None, likes=None); q.put();
    q = DbQuestion(index=245, theme="Food", question="What is the name of this hot red chilli pepper it is often dried and ground?", answer="Cayenne Pepper", shows=None, likes=None); q.put();
    q = DbQuestion(index=246, theme="Food", question="What's colour of the inside of a pistachio nut?", answer="Green", shows=None, likes=None); q.put();
    q = DbQuestion(index=247, theme="Food", question="This is converted into alcohol during brewing?", answer="Sugar", shows=None, likes=None); q.put();
    q = DbQuestion(index=248, theme="Food", question="This herb is used to make a Pesto sauce?", answer="Basil", shows=None, likes=None); q.put();
    q = DbQuestion(index=249, theme="Food", question="When a wine is described as 'brut' what does it mean about the taste?", answer="Very Dry", shows=None, likes=None); q.put();
    q = DbQuestion(index=250, theme="Food", question="The usual main meat ingredient of a Shish Kebab is?", answer="Lamb", shows=None, likes=None); q.put();
    q = DbQuestion(index=251, theme="Food", question="What do the brits call a Weenie?", answer="A hot dog", shows=None, likes=None); q.put();
    q = DbQuestion(index=252, theme="Food", question="The \"D\" where milk is processed?", answer="Dairy", shows=None, likes=None); q.put();
    q = DbQuestion(index=253, theme="Food", question="What spice gives piccalilli and curries its yellow colour?", answer="Turmeric", shows=None, likes=None); q.put();
    q = DbQuestion(index=254, theme="Food", question="Hash Browns are normally made from which vegetables?", answer="Potatoes", shows=None, likes=None); q.put();
    q = DbQuestion(index=255, theme="Food", question="Prunes stuffed with almonds are wrapped in what to make Devils on horseback?", answer="Bacon", shows=None, likes=None); q.put();
    q = DbQuestion(index=256, theme="Food", question="The main ingredient of a Paella is what?", answer="Rice", shows=None, likes=None); q.put();
    q = DbQuestion(index=257, theme="Food", question="The main ingredient of Sauerkraut is what?", answer="Cabbage", shows=None, likes=None); q.put();
    q = DbQuestion(index=258, theme="Food", question="This food has a name which means on a skewer?", answer="Kebab", shows=None, likes=None); q.put();
    q = DbQuestion(index=259, theme="Food", question="In a Mcdonald's Big Mac how many pieces of bun are there?", answer="Three", shows=None, likes=None); q.put();
    q = DbQuestion(index=260, theme="Food", question="Oyster, Chestnut, or Shitaki are types of which vegetable?", answer="Mushrooms", shows=None, likes=None); q.put();
    q = DbQuestion(index=261, theme="Food", question="What is the only fruit named for its colour?", answer="Orange", shows=None, likes=None); q.put();
    q = DbQuestion(index=262, theme="Food", question="Traditionally at a fair ground what fruit would be covered with toffee?", answer="Apple", shows=None, likes=None); q.put();
    q = DbQuestion(index=263, theme="Food", question="This herb is used to flavour Pernod?", answer="Aniseed", shows=None, likes=None); q.put();
    q = DbQuestion(index=264, theme="Food", question="This milk is a basic ingredient in Thai cookery?", answer="Coconut milk", shows=None, likes=None); q.put();
