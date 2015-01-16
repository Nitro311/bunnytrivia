class question(object):

    def __init__(self, theme, question, answer, answers):
        self.theme = theme
        self.question = question
        self.answer = answer
        self.answers = answers



questions = [
    question(theme = "Religion/Mythology", question = "What is the only domesticated animal not mentioned in the Bible?", answer = "Cat", answers = []),
    question(theme = "Religion/Mythology", question = "What word appears exactly 773,692 times in the King James Bible?", answer = "Amen", answers = []),
    question(theme = "Religion/Mythology", question = "What follows mass as the most popular activity in U.S. Catholic churches?", answer = "Bingo", answers = []),
    question(theme = "Religion/Mythology", question = "What Arab nation has the highest percentage of Christians?", answer = "Lebanon", answers = []),
    question(theme = "Religion/Mythology", question = "What symbol did St. Patrick use to explain his theory of the Holy Trinity?", answer = "Shamrock", answers = []),
    question(theme = "Religion/Mythology", question = "What political movement got its name from the hill in Jerusalem boasting the Temple of Solomon?", answer = "Zionism", answers = []),
    question(theme = "Religion/Mythology", question = "What country boasts the largest number of Catholics?", answer = "Brazil", answers = []),
    question(theme = "Religion/Mythology", question = "What name has been shared by the most popes?", answer = "John", answers = []),
    question(theme = "Religion/Mythology", question = "Which two wicked cities were destroyed by God in Genesis?", answer = "Sodom and Gomorrah", answers = []),
    question(theme = "Religion/Mythology", question = "What two countries claim two-thirds of the world's 2,000-plus registered saints?", answer = "Italy and France", answers = []),
    question(theme = "Religion/Mythology", question = "What fruit is depicted in Leonardo's Last Supper, even though it did not arrive in the Holy Land until long after Jesus' death?", answer = "Orange", answers = []),
    question(theme = "Religion/Mythology", question = "What is there more of in the world- nonreligious people, Hindus or Muslims?", answer = "Nonreligious people", answers = []),
    question(theme = "Religion/Mythology", question = "What former church lady got $75,000 to let ""A Current Affair"" televise her wedding in 1993?", answer = "Tammy Faye Bakker", answers = []),
    question(theme = "Religion/Mythology", question = "What religious movement began with Martin Luther's attack on the sale of indulgences?", answer = "Reformation", answers = []),
    question(theme = "Religion/Mythology", question = "What Saudi Arabian city was the birthplace of the prophet Muhammad?", answer = "Mecca", answers = []),
    question(theme = "Religion/Mythology", question = "What storied city on the Euphrates River was 55 miles south of Baghdad?", answer = "Babylon", answers = []),
    question(theme = "Religion/Mythology", question = "What biblical place name means ""pleasure""?", answer = "Eden", answers = []),
    question(theme = "Religion/Mythology", question = "What city did Napoleon occupy in 1798, sending Pope Pius VI to the south of France?", answer = "Rome", answers = []),
    question(theme = "Religion/Mythology", question = "What church raised millions selling members ""electropsychometer"" lie detectors?", answer = "Church of Scientology", answers = []),
    question(theme = "Religion/Mythology", question = "What nation has 1,000 permanent inhabitants and produces no export goods?", answer = "Vatican City", answers = []),
    question(theme = "Religion/Mythology", question = "What was the world's principal Christian city before it fell to the Ottoman Turks in 1453?", answer = "Constantinople", answers = []),
    question(theme = "Religion/Mythology", question = "What nation's Catholics saw the Pope make a triumphant homecoming visit in 1980?", answer = "Poland", answers = []),
    question(theme = "Religion/Mythology", question = "What animal is mentioned most frequently in both the New and Old Testaments?", answer = "Sheep", answers = []),
    question(theme = "Religion/Mythology", question = "What's the only 100 percent Christian nation on Earth?", answer = "Vatican City", answers = []),
    question(theme = "Religion/Mythology", question = "What biblical epic was the top-grossing movie of the 1950's?", answer = "Ten Commandments", answers = []),
    question(theme = "Religion/Mythology", question = "Who was the first pope?", answer = "St. Peter", answers = []),
    question(theme = "Religion/Mythology", question = "What does an ecclesiophobic evangelist fear?", answer = "Churches", answers = []),
    question(theme = "Religion/Mythology", question = "What book did Christians often place on their foreheads to cure insomnia in medieval times?", answer = "Bible", answers = []),
    question(theme = "Religion/Mythology", question = "How much time did Jonah spend in the belly of the whale?", answer = "Three days and three nights", answers = []),
    question(theme = "Religion/Mythology", question = "According to the Bible, what substance was used to caulk Noah's ark and to seal the basket in which the infant Moses was set adrift on the Nile?", answer = "Pitch or natural asphalt", answers = []),
    question(theme = "Religion/Mythology", question = "What language is Jesus believed to have spoken?", answer = "Aramaic", answers = []),
    question(theme = "Religion/Mythology", question = "According to the Bible, what weapons was the Philistine giant Goliath carrying when he was slain by David?", answer = "A sword and a spear", answers = []),
    question(theme = "Religion/Mythology", question = "According to the Bible, how many pearly gates are there?", answer = "12", answers = []),
    question(theme = "Religion/Mythology", question = "What were the names of the three wise men?", answer = "Balthazar, Caspar and Melchior", answers = []),
    question(theme = "Religion/Mythology", question = "Who were the parents of King Solomon?", answer = "David and Bathsheba", answers = []),
    question(theme = "Religion/Mythology", question = "Name the two books of the Bible named after women.", answer = "Ruth and Esther", answers = []),
    question(theme = "Religion/Mythology", question = "In the Old Testament, who was Jezebel's husband?", answer = "Ahab, King of Israel", answers = []),
    question(theme = "Food", question = "What milk product did the U.S. Agriculture Department propose as a substitute for meat in school lunches, in 1996?", answer = "Yogurt", answers = []),
    question(theme = "Food", question = "What breakfast cereal was Sonny the Cuckoo Bird \"cuckoo for\"?", answer = "Cocoa Puffs", answers = []),
    question(theme = "Food", question = "On what vegetable did an ancient Egyptian place his right hand when taking an oath?", answer = "onion", answers = []),
    question(theme = "Food", question = "How many flowers are in the design stamped on each side of an Oreo cookie?", answer = "Twelve", answers = []),
    question(theme = "Food", question = "Black-eyed peas are not peas. What are they?", answer = "Beans", answers = []),
    question(theme = "Food", question = "Under what name did the Domino's Pizza chain get its start?", answer = "DomNick's", answers = []),
    question(theme = "Food", question = "What was margarine called when it was first marketed in England?", answer = "Butterine", answers = []),
    question(theme = "Food", question = "What are the two top selling spices in the world?", answer = "Pepper and mustard", answers = []),
    question(theme = "Food", question = "What was the name of Cheerios when it was first marketed 50 years ago?", answer = "Cheerioats", answers = []),
    question(theme = "Food", question = "What flavor of ice cream did Baskin-Robbins introduce to commemorate America's landing on the moon on July 20, 1969?", answer = "Lunar Cheesecake", answers = []),
    question(theme = "Food", question = "What is the most widely eaten fish in the world?", answer = "Herring", answers = []),
    question(theme = "Food", question = "What is the name of the evergreen shrub from which we get capers?", answer = "caper bush", answers = []),
    question(theme = "Food", question = "What animals milk is used to make authentic Italian mozzarella cheese?", answer = "water buffalo's", answers = []),
    question(theme = "Food", question = "What nation produces two thirds of the world's vanilla?", answer = "Madagascar", answers = []),
    question(theme = "Food", question = "What was the drink we know as the Bloody Mary originally called?", answer = "Red Snapper", answers = []),
    question(theme = "Food", question = "What was the first commercially manufactured breakfast cereal?", answer = "Shredded Wheat", answers = []),
    question(theme = "Food", question = "When Birdseye introduced the first frozen food in 1930, what did the company call it?", answer = "Frosted Food", answers = []),
    question(theme = "Food", question = "What American city produces most of the egg rolls sold in grocery stores in the United States?", answer = "Houston, Texas", answers = []),
    question(theme = "Food", question = "What was the first of H.J. Heinz' \"57 varieties\"?", answer = "Horseradish", answers = []),
    question(theme = "Food", question = "What is the literal meaning of the Italian word linguine?", answer = "Little tongues", answers = []),
    question(theme = "Food", question = "Where did the pineapple plant originate?", answer = "South America", answers = []),
    question(theme = "Food", question = "What recipe, first published 50 years ago, has been requested most frequently through the years by the readers of \"Better Homes and Garden\"?", answer = "Hamburger Pie", answers = []),
    question(theme = "Food", question = "What is the only essential vitamin not found in the white potato?", answer = "Vitamin A", answers = []),
    question(theme = "Food", question = "What food is the leading source of salmonella poisoning?", answer = "Chicken", answers = []),
    question(theme = "Food", question = "What company first condensed soup in 1898?", answer = "Campbell's", answers = []),
    question(theme = "Food", question = "What nutty legume accounts for one sixth of the world's vegetable oil production?", answer = "peanut", answers = []),
    question(theme = "Food", question = "What country saw the cultivation of the first potato, in 200 A.D.?", answer = "South America", answers = []),
    question(theme = "Food", question = "What type of lettuce was called Crisphead until the 1920s?", answer = "Iceberg lettuce", answers = []),
    question(theme = "Food", question = "What tree gives us prunes?", answer = "plum tree", answers = []),
    question(theme = "Food", question = "What type of chocolate was first developed for public consumption in Vevey, Switzerland in 1875?", answer = "Milk Chocolate", answers = []),
    question(theme = "Food", question = "What added ingredient keeps confectioners' sugar from clumping?", answer = "Corn starch", answers = []),
    question(theme = "Food", question = "What edible comes in crimmini, morel, oyster and wood ear varieties?", answer = "Mushrooms", answers = []),
    question(theme = "Food", question = "What newly-imported substance caused the first major outbreak of tooth decay in Europe, in the1500's?", answer = "Sugar", answers = []),
    question(theme = "Food", question = "What ingredient in fresh milk is eventually devoured by bacteria, causing the sour taste?", answer = "Lactose", answers = []),
    question(theme = "Food", question = "What uncooked meat is a trichina worm most likely to make a home in?", answer = "Pork", answers = []),
    question(theme = "Food", question = "What baking ingredient, sprayed at high pressure, did the U.S. Air Force replace its toxic paint stripper with?", answer = "Baking soda", answers = []),
    question(theme = "Food", question = "What staple is laced with up to 16 additives including plaster of paris, to stay fresh?", answer = "Bread", answers = []),
    question(theme = "Food", question = "What falling fruit supposedly inspired Isaac Newton to write the laws of gravity?", answer = "An Apple", answers = []),
    question(theme = "Food", question = "What method of preserving food did the Incas first use, on potatoes?", answer = "Freeze-drying", answers = []),
    question(theme = "Food", question = "What drupaceous fruit were Hawaiian women once forbidden by law to eat?", answer = "coconut", answers = []),
    question(theme = "Food", question = "What hit the market alongside spinach as the first frozen veggies?", answer = "Peas", answers = []),
    question(theme = "Food", question = "How many sizes of chicken eggs does the USDA recognize, including peewee?", answer = "Six", answers = []),
    question(theme = "Food", question = "What are de-headed, de-veined an sorted by size in a laitram machine?", answer = "Shrimp", answers = []),
    question(theme = "Food", question = "What's the only fish that produces real caviar, according to the FDA?", answer = "Sturgeon", answers = []),
    question(theme = "Food", question = "What type of egg will yield 11 and one-half average-size omelettes?", answer = "An Ostrich egg", answers = []),
    question(theme = "Food", question = "What's the groundnut better known as?", answer = "peanut", answers = []),
    question(theme = "Food", question = "What crystalline salt is frequently used to enhance the flavor to TV dinners?", answer = "Monosodium glutamate", answers = []),
    question(theme = "Food", question = "What sticky sweetener was traditionally used as an antiseptic ointment for cuts and burns?", answer = "Honey", answers = []),
    question(theme = "Food", question = "What should your diet be high in to lessen the chance of colon cancer, according to a 1990 study?", answer = "Fiber", answers = []),
    question(theme = "Food", question = "What nut do two-thirds of its U. S. producers sell through Blue Diamond?", answer = "Almond", answers = []),
    question(theme = "Food", question = "What type of oven will not brown foods?", answer = "Microwave oven", answers = []),
    question(theme = "Food", question = "What type of food did Linda McCartney launch?", answer = "Vegetarian food", answers = []),
    question(theme = "Food", question = "What type of tree leaves are the only food that a koala bear will eat?", answer = "Eucalyptus", answers = []),
    question(theme = "Food", question = "Which country in Europe consumes more spicy Mexican food than any other?", answer = "Norway", answers = []),
    question(theme = "Food", question = "The FDA approved what fat substitute for use in snack foods even though there were reports of side affects like cramps and diarrhea?", answer = "Olestra", answers = []),
    question(theme = "Food", question = "Federal labeling regulations require how much caffeine be removed from coffee for it to be called decaffeinated?", answer = "Ninety seven percent", answers = []),
    question(theme = "Food", question = "What famous Greek once advised = \"Let your food be your medicine, and your medicine be your food\"?", answer = "Hippocrates", answers = []),
    question(theme = "Food", question = "Chicken is the leading cause of what food born illness?", answer = "Salmonella poisoning", answers = []),
    question(theme = "Food", question = "Who invented Margarine in 1868?", answer = "Hyppolyte Merge-mouries", answers = []),
    question(theme = "Food", question = "What group of people were the first to use freeze-drying on potatoes?", answer = "Incas", answers = []),
    question(theme = "Food", question = "What was the Teenage Mutant Ninja Turtles favorite food?", answer = "Pizza", answers = []),
    question(theme = "Food", question = "What food was considered the food of the Gods, and was said to bring eternal life to anyone who ate it?", answer = "Ambrosia", answers = []),
    question(theme = "Food", question = "What was the convenience food that Joel Cheek developed?", answer = "Instant Coffee", answers = []),
    question(theme = "Food", question = "The song, Food, Glorious Food, was featured in which musical?", answer = "Oliver", answers = []),
    question(theme = "Food", question = "Of the Worlds food crops, what percentage is pollinated by insects?", answer = "80 percent", answers = []),
    question(theme = "Food", question = "The Giant panda's favorite food is what?", answer = "Bamboo shoots", answers = []),
    question(theme = "Food", question = "Which entertainer on Conan O'Brien's show, choose NBC cafeteria chicken over his own brand in a blind taste test?", answer = "Kenny Rogers", answers = []),
    question(theme = "Food", question = "What drink was sold as Diastoid when first introduced?", answer = "Malted milk", answers = []),
    question(theme = "Food", question = "What type of micro organism makes up the base of marine and freshwater food chains?", answer = "Plankton", answers = []),
    question(theme = "Food", question = "What type of creature builds a lodge in which to store food, rear its young, and pass the winter?", answer = "Beaver", answers = []),
    question(theme = "Food", question = "What fruit or vegetable was dubbed the FlavrSavr and was the first genetically engineered food sold in the United States?", answer = "tomato", answers = []),
    question(theme = "Food", question = "What fitness guru appeared as a dancing meatball in an Italian TV commercial as an art student?", answer = "Richard Simmons", answers = []),
    question(theme = "Food", question = "What Olympic athlete could not run the 200-meter final in the 92 Olympics because of food poisoning?", answer = "Michael Johnson", answers = []),
    question(theme = "Food", question = "What morning food has a name derived from the German word for stirrup?", answer = "Bagel", answers = []),
    question(theme = "Food", question = "In 1904, what food product was renamed Post Toasties cereal because the clergy objected to the original name?", answer = "Elijah's Manna", answers = []),
    question(theme = "Food", question = "Which country does Rioja Wine come from?", answer = "Spain", answers = []),
    question(theme = "Food", question = "The juice of which fruit will you find in a bloody mary?", answer = "Tomato", answers = []),
    question(theme = "Food", question = "Homer Simpson drinks Which brand of beer regularly?", answer = "Duff", answers = []),
    question(theme = "Food", question = "What is the main ingredient of paella?", answer = "Rice", answers = []),
    question(theme = "Food", question = "What would you call a segment of garlic?", answer = "Clove", answers = []),
    question(theme = "Food", question = "A canteloupe is what kind of fruit?", answer = "Melon", answers = []),
    question(theme = "Food", question = "Sticky and sweet this food is produced in a hive?", answer = "Honey", answers = []),
    question(theme = "Food", question = "This dairy product tastes good on crackers and sandwiches or on its own?", answer = "Cheese", answers = []),
    question(theme = "Food", question = "In the dish of Beef Wellington, in what is the beef wrapped?", answer = "Pastry", answers = []),
    question(theme = "Food", question = "What is The Teenage Mutant Ninja Turtles favourite food?", answer = "Pizza", answers = []),
    question(theme = "Food", question = "What is the main vegetable ingredient in the dish Borsht?", answer = "Beetroot", answers = []),
    question(theme = "Food", question = "Sauerkraut is pickled what?", answer = "Cabbage", answers = []),
    question(theme = "Food", question = "What vegetable is also known as zucchini in the USA?", answer = "Courgette", answers = []),
    question(theme = "Food", question = "This fruit goes into the liqueur Kirsch?", answer = "Cherry", answers = []),
    question(theme = "Food", question = "A bloomer is what type of food?", answer = "Bread", answers = []),
    question(theme = "Food", question = "Which is the fruit that contains the most calories?", answer = "Avocado pear", answers = []),
    question(theme = "Food", question = "What is lava bread?", answer = "Seaweed", answers = []),
    question(theme = "Food", question = "What fruit grows on the blackthorn tree?", answer = "Sloe", answers = []),
    question(theme = "Food", question = "Which food has a name which means on a skewer?", answer = "Kebab", answers = []),
    question(theme = "Food", question = "In a Mcdonald's Big Mac how many pieces of bun are there?", answer = "Three", answers = []),
    question(theme = "Food", question = "Oyster, Chestnut, or Shitaki are types of which vegetable?", answer = "Mushrooms", answers = []),
    question(theme = "Food", question = "A Calzone Is A Folded Stuffed What?", answer = "Pizza", answers = []),
    question(theme = "Food", question = "Which country invented the Marmite alternative - Veggie mite?", answer = "Australia", answers = []),
    question(theme = "Food", question = "Which country does the dish Mousakka come from?", answer = "Greece", answers = []),
    question(theme = "Food", question = "Which fruit served with cream is eaten during the summer tennis tournament Wimbledon?", answer = "Strawberries", answers = []),
    question(theme = "Food", question = "Apart from potato What is the other main ingredient of Bubble and Squeak?", answer = "Cabbage", answers = []),
    question(theme = "Food", question = "Which food was popular with Popeye the Sailor?", answer = "Spinach", answers = []),
    question(theme = "Food", question = "What is Scooby Doo`s favourite food?", answer = "Scooby Snacks", answers = []),
    question(theme = "Food", question = "What is the only fruit that grows its seeds on the outside?", answer = "Strawberry", answers = []),
    question(theme = "Food", question = "What other names are sardines known by?", answer = "Pilchards", answers = []),
    question(theme = "Food", question = "Which city gave its name to a three-coloured Neapolitan ice-cream?", answer = "Naples", answers = []),
    question(theme = "Food", question = "What would you be drinking if you were drinking Earl Grey?", answer = "Tea", answers = []),
    question(theme = "Food", question = "What are Pontefract cakes made from?", answer = "Liquorice", answers = []),
    question(theme = "Food", question = "What is another name for almond paste?", answer = "Marzipan", answers = []),
    question(theme = "Food", question = "What name can be a lettuce or a mass of floating frozen water?", answer = "Iceberg", answers = []),
    question(theme = "Food", question = "What's Sauerkraut's main ingredient?", answer = "Cabbage", answers = []),
    question(theme = "Food", question = "What's the only rock edible to man?", answer = "Salt", answers = []),
    question(theme = "Food", question = "What type of salad do you need apple, celery, walnuts, raisins and mayonnaise mixed together?", answer = "Waldorf Salad", answers = []),
    question(theme = "Food", question = "Which fruit also shares its name with Gwyneth Paltrow's daughter?", answer = "Apple", answers = []),
    question(theme = "Food", question = "From which animal does haggis come?", answer = "Sheep", answers = []),
    question(theme = "Food", question = "In cockney rhyming slang what is \"Ruby Murray\"?", answer = "Curry", answers = []),
    question(theme = "Food", question = "What cake do you keep a layer of to eat at the christening of your first child?", answer = "Wedding Cake", answers = []),
    question(theme = "Food", question = "Which brand of frozen ice cream cone was advertised to the tune of Italian song \"O Sole Mio\"?", answer = "Cornetto", answers = []),
    question(theme = "Food", question = "If I take two apples out of a basket containing six apples how many apples do I have ?", answer = "Two", answers = []),
    question(theme = "Food", question = "Which fruit does one of Bob Geldofs' daughter share a name with?", answer = "Peaches", answers = []),
    question(theme = "Food", question = "In Eggs Florentine which vegetable is a main ingredient?", answer = "Spinach", answers = []),
    question(theme = "Food", question = "In a French restaurant what would you be eating if you chose escargots?", answer = "Snails", answers = []),
    question(theme = "Food", question = "Which meat is usally in a Shish Kebab?", answer = "Lamb", answers = []),
    question(theme = "Food", question = "What flavour is Ouzo?", answer = "Aniseed", answers = []),
    question(theme = "Food", question = "A crapulous person is full of what?", answer = "Alcohol", answers = []),
    question(theme = "Food", question = "What Italian Cheese usually tops a pizza?", answer = "Mozzarella", answers = []),
    question(theme = "Food", question = "Port Salut is what?", answer = "Cheese", answers = []),
    question(theme = "Food", question = "Who talked of eating human liver washed down with Chianti?", answer = "Hannibal Lecter", answers = []),
    question(theme = "Food", question = "Who, according to the TV commercial, \'makes exceedingly good cakes ""?", answer = "Mr Kipling", answers = []),
    question(theme = "Food", question = "What vegetable is sold mainly before 30th October?", answer = "Pumpkin", answers = []),
    question(theme = "Food", question = "Whats the english translation for the french word crepe?", answer = "Pancake", answers = []),
    question(theme = "Food", question = "What is a macadamia?", answer = "Nut", answers = []),
    question(theme = "Food", question = "In ancient Egypt what was liquorice used for?", answer = "Medicine", answers = []),
    question(theme = "Food", question = "What type of thin pancake is eaten in Mexico?", answer = "Tortilla", answers = []),
    question(theme = "Food", question = "If steak was blue how would it be cooked?", answer = "Very Rare", answers = []),
    question(theme = "Food", question = "Baked beans are made from which beans?", answer = "Haricot", answers = []),
    question(theme = "Food", question = "What are small cubes of toasted or fried bread?", answer = "Croutons", answers = []),
    question(theme = "Food", question = "What would you call a cluster of bananas?", answer = "A hand", answers = []),
    question(theme = "Food", question = "What nuts are used to flavour amaretto?", answer = "Almonds", answers = []),
    question(theme = "Food", question = "If you had frijoles refritos in a Mexican restaurant it would be refried what?", answer = "beans", answers = []),
    question(theme = "Food", question = "This city is famous for its oranges?", answer = "Seville", answers = []),
    question(theme = "Food", question = "Which celebrity chef was nicknamed 'The Naked Chef'?", answer = "Jamie Oliver", answers = []),
    question(theme = "Food", question = "What daily vegetable do typical boxer's ears look like?", answer = "Cauliflower", answers = []),
    question(theme = "Food", question = "What's a small pickled cucumber?", answer = "Gherkin", answers = []),
    question(theme = "Food", question = "What's cockney rhyming slang for eyes?", answer = "Mince Pies", answers = []),
    question(theme = "Food", question = "What name's given to a small, deep fried chinese dumpling with a savoury filing?", answer = "Won ton", answers = []),
    question(theme = "Food", question = "Which brand of beer features a kangaroo on the packaging?", answer = "Fosters", answers = []),
    question(theme = "Food", question = "A mint with a hole?", answer = "Polo", answers = []),
    question(theme = "Food", question = "What is advertised on TV with the slogan \"You either Love it or Hate it\"?", answer = "Marmite", answers = []),
    question(theme = "Food", question = "In Ancient China what variety of meat was reserved exclusively for the emperor?", answer = "Pork", answers = []),
    question(theme = "Food", question = "Which song mentions saveloy, mustard, jelly, custard and sausages in the lyrics?", answer = "Food Glorious Food", answers = []),
    question(theme = "Food", question = "Jasmine and long grain are both types of what?", answer = "Rice", answers = []),
    question(theme = "Food", question = "What might you be eating at Wimbledon if you had a Cambridge Rival in your mouth?", answer = "Strawberry", answers = []),
    question(theme = "Food", question = "What fruit was originally called a Chinese gooseberry", answer = "Kiwi Fruit", answers = []),
    question(theme = "Food", question = "What sort of pastry is used to make profiteroles?", answer = "Choux", answers = []),
    question(theme = "Food", question = "What is the national dish of Hungary?", answer = "Goulash", answers = []),
    question(theme = "Food", question = "Which nut is used to flavour traditional Bakewell Tart?", answer = "Almond", answers = []),
    question(theme = "Food", question = "In the dish of Beef Wellington, in what is the beef wrapped?", answer = "Pastry", answers = []),
    question(theme = "Food", question = "What is the main vegetable used to make Borsch?", answer = "Beetroot", answers = []),
    question(theme = "Food", question = "What is Bombay Duck?", answer = "Fish", answers = []),
    question(theme = "Food", question = "Which fruit is used in the making of a Black Forest Gateau?", answer = "Black Cherries", answers = []),
    question(theme = "Food", question = "What is included in a BLT sandwich?", answer = "Bacon, lettuce and tomato", answers = []),
    question(theme = "Food", question = "The name of what food, when translated, means twice-cooked?", answer = "Biscuit", answers = []),
    question(theme = "Food", question = "How many calories are there in a stick of celery?", answer = "None", answers = []),
    question(theme = "Food", question = "Which country consumes the most pasta per person per year?", answer = "Italy", answers = []),
    question(theme = "Food", question = "What was the favourite food of Paddington Bear?", answer = "Marmalade", answers = []),
    question(theme = "Food", question = "Which family of vegatables are Chives from?", answer = "Onions", answers = []),
    question(theme = "Food", question = "In the Hansel and Gretel tale what was the wicked witch's house made of?", answer = "Gingerbread", answers = []),
    question(theme = "Food", question = "What take-away is traditional in England at the seaside?", answer = "Fish and chips", answers = []),
    question(theme = "Food", question = "What meat is Coq au vin made with ?", answer = "Chicken", answers = []),
    question(theme = "Food", question = "Which cheese is made in reverse?", answer = "Edam", answers = []),
    question(theme = "Food", question = "What variety of banana shares its name with the title of a Bond movie?", answer = "Goldfinger", answers = []),
    question(theme = "Food", question = "Conference, Bartlett and Kaiser are all varieties of which fruit?", answer = "Pear", answers = []),
    question(theme = "Food", question = "Which product is advertised on TV with the slogan, ""Once you pop you can't stop""?", answer = "Pringles", answers = []),
    question(theme = "Food", question = "What is the official national cheese of Greece?", answer = "Feta", answers = []),
    question(theme = "Food", question = "Which variety of orange was named after a Japanese province?", answer = "Satsuma", answers = []),
    question(theme = "Food", question = "Marzipan is made from which nuts?", answer = "Almonds", answers = []),
    question(theme = "Food", question = "During brewing what is converted into alcohol?", answer = "Sugar", answers = []),
    question(theme = "Food", question = "This chick pea puree is flavoured with tahini and served as a dip?", answer = "Hummus", answers = []),
    question(theme = "Food", question = "Grolsch lager is from which country?", answer = "Holland", answers = []),
    question(theme = "Food", question = "This carbohydrate fruit is high in potassium?", answer = "Banana", answers = []),
    question(theme = "Food", question = "What overtook coca-cola as the most well known brand name (in the world) in 1996?", answer = "McDonalds", answers = []),
    question(theme = "Food", question = "The 'M' in the McDonalds logo is what colour?", answer = "Yellow", answers = []),
    question(theme = "Food", question = "Bacardi Rum's logo features which creature?", answer = "Bat", answers = []),
    question(theme = "Food", question = "An egg plant is also known as which vegetable?", answer = "Aubergine", answers = []),
    question(theme = "Food", question = "What is a light round bun usually served hot?", answer = "Muffin", answers = []),
    question(theme = "Food", question = "What is the plant that wards off vampires?", answer = "Garlic", answers = []),
    question(theme = "Food", question = "The Teenage Mutant Ninja Turtles favourite food is?", answer = "Pizza", answers = []),
    question(theme = "Food", question = "The main vegetable ingredient in the dish Borsht is what?", answer = "Beetroot", answers = []),
    question(theme = "Food", question = "Sauerkraut is pickled what?", answer = "Cabbage", answers = []),
    question(theme = "Food", question = "Chicory was a war time substitute for what drink?", answer = "Coffee", answers = []),
    question(theme = "Food", question = "What vegetable is also known as zucchini in the USA?", answer = "Courgette", answers = []),
    question(theme = "Food", question = "This fruit goes into the liqueur Kirsch?", answer = "Cherry", answers = []),
    question(theme = "Food", question = "A bloomer is What type of food?", answer = "Bread", answers = []),
    question(theme = "Food", question = "This type of milk is a basic ingredient in Thai cookery?", answer = "Coconut milk", answers = []),
    question(theme = "Food", question = "What soft drink uses this slogan, \"What's the worst that could happen\"?", answer = "Dr Pepper", answers = []),
    question(theme = "Food", question = "Which is the fruit that contains the most calories?", answer = "Avocado pear", answers = []),
    question(theme = "Food", question = "What are dried prunes?", answer = "Plums", answers = []),
    question(theme = "Food", question = "The main cereal ingredient of flapkacks (Hudson Bars in USA)?", answer = "Oats", answers = []),
    question(theme = "Food", question = "What is the correct spelling of a Cadbury Creame/Creem/Creme/Cream Egg?", answer = "Creme", answers = []),
    question(theme = "Food", question = "What is Uganda's staple crop, which each adult consumes over 3 times bodyweight annually?", answer = "Bananas", answers = []),
    question(theme = "Food", question = "What's lava bread?", answer = "Seaweed", answers = []),
    question(theme = "Food", question = "What fruit grows on the blackthorn tree?", answer = "Sloe", answers = []),
    question(theme = "Food", question = "Which two fruits are anagrams of each other?", answer = "Lemon & Melon", answers = []),
    question(theme = "Food", question = "Homer Simpson drinks what brand of beer?", answer = "Duff", answers = []),
    question(theme = "Food", question = "A crapulous person is full of what?", answer = "Acohol", answers = []),
    question(theme = "Food", question = "What spanish drink consists of sweet red wine, lemonade or soda water and decorated with fruit?", answer = "Sangria", answers = []),
    question(theme = "Food", question = "This spirit is the base for a Black Russian cocktail?", answer = "Vodka", answers = []),
    question(theme = "Food", question = "What country is home to Grolsch lager?", answer = "Holland", answers = []),
    question(theme = "Food", question = "A crapulous person is full of what?", answer = "Alcohol", answers = []),
    question(theme = "Food", question = "What is the name of this hot red chilli pepper it is often dried and ground?", answer = "Cayenne Pepper", answers = []),
    question(theme = "Food", question = "What's colour of the inside of a pistachio nut?", answer = "Green", answers = []),
    question(theme = "Food", question = "This is converted into alcohol during brewing?", answer = "Sugar", answers = []),
    question(theme = "Food", question = "This herb is used to make a Pesto sauce?", answer = "Basil", answers = []),
    question(theme = "Food", question = "When a wine is described as 'brut' what does it mean about the taste?", answer = "Very Dry", answers = []),
    question(theme = "Food", question = "The usual main meat ingredient of a Shish Kebab is?", answer = "Lamb", answers = []),
    question(theme = "Food", question = "What do the brits call a Weenie?", answer = "A hot dog", answers = []),
    question(theme = "Food", question = "The \"D\" where milk is processed?", answer = "Dairy", answers = []),
    question(theme = "Food", question = "What spice gives piccalilli and curries its yellow colour?", answer = "Turmeric", answers = []),
    question(theme = "Food", question = "Hash Browns are normally made from which vegetables?", answer = "Potatoes", answers = []),
    question(theme = "Food", question = "Prunes stuffed with almonds are wrapped in what to make Devils on horseback?", answer = "Bacon", answers = []),
    question(theme = "Food", question = "The main ingredient of a Paella is what?", answer = "Rice", answers = []),
    question(theme = "Food", question = "The main ingredient of Sauerkraut is what?", answer = "Cabbage", answers = []),
    question(theme = "Food", question = "This food has a name which means on a skewer?", answer = "Kebab", answers = []),
    question(theme = "Food", question = "In a Mcdonald's Big Mac how many pieces of bun are there?", answer = "Three", answers = []),
    question(theme = "Food", question = "Oyster, Chestnut, or Shitaki are types of which vegetable?", answer = "Mushrooms", answers = []),
    question(theme = "Food", question = "What is the only fruit named for its colour?", answer = "Orange", answers = []),
    question(theme = "Food", question = "Traditionally at a fair ground what fruit would be covered with toffee?", answer = "Apple", answers = []),
    question(theme = "Food", question = "This herb is used to flavour Pernod?", answer = "Aniseed", answers = []),
    question(theme = "Food", question = "This milk is a basic ingredient in Thai cookery?", answer = "Coconut milk", answers = [])
]
