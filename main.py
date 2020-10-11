import pygame

# Define colours
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
brown = (139,69,19)
blue = (0,191,255)
yellow = (255,255,0)
darkBrown = (101, 67, 33)
darkGrey = (128,128,128)

class Wall(pygame.sprite.Sprite):
    """This class is for all visible and hidden walls in the game"""

    def __init__(self, x, y, width, height, color):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()

        # Create the dimensions of the character.
        self.image = pygame.Surface([width, height])

        # Handle colour parameter
        if color == None:
          pass
        else:
          self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()

        # Set the player's x and y values
        self.rect.y = y
        self.rect.x = x

class Player(pygame.sprite.Sprite):
    """ This class creates the player object"""

    # Set speed vector
    change_x = 0
    change_y = 0

    # Set the player's lives
    lives = 3

    # Set the player's coins
    coins = 0

    # Used in handling player damage when they hit a monster. It stores the length of the monster hit list before it is updated.
    original_len_monster_hit_list_x = 0
    original_len_monster_hit_list_y = 0

    # Used in determining when the switch is toggled. It stores the length of the switch hit list before it is updated.
    original_len_switch_hit_list_x = 0
    original_len_switch_hit_list_y = 0

    # Stores whether a monster has reached the lowest point in can travel on its predetermined path
    hit_bottom_of_path = False

    # Stores whether the switch has been flipped
    switchFLipped = False

    def __init__(self, x, y, width, height, colour):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()
        # Set height, width
        self.image = pygame.Surface([width, height])

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()

        # Set the player's x and y values.
        self.rect.y = y
        self.rect.x = x

        # Stores the direction that the monster is facing
        self.direction = 1

    def changespeed(self, x, y):
        """ Change the speed of the player."""
        self.change_x += x
        self.change_y += y

    # Will move the player and handle all colliding with other sprites (monsters, coins, walls, switches, ...)
    def move(self, walls, coins, hiddenCoins, monsters, switches, hiddenWalls):

        # Move left/right
        self.rect.x += self.change_x

        #If the player hits a coin, increment coin variable.
        coin_hit_list = pygame.sprite.spritecollide(self, coins, True)
        for coin in coin_hit_list:
          self.add_coins()
        hidden_coin_hit_list = pygame.sprite.spritecollide(self,hiddenCoins, True)
        for coin in hidden_coin_hit_list:
          self.add_coins()

        # Handle character placement when they hit the switch
        switches_hit_list = pygame.sprite.spritecollide(self,switches, False)
        len_switches_hit_list = len(switches_hit_list)
        for switch in switches_hit_list:
          if self.change_x > 0:
            self.rect.right = switch.rect.left
          else:
            # Otherwise if we are moving left, do the opposite.
            self.rect.left = switch.rect.right

          # Activate the switch only once if the player hits it.
          if len_switches_hit_list == 1:
            if self.original_len_switch_hit_list_x != len_switches_hit_list:
              switch.isSwapped = True
          self.original_len_switch_hit_list_x = len_switches_hit_list


        # Handle monsters
        if monsters != None:
          monster_hit_list = pygame.sprite.spritecollide(self,monsters,False)

          len_monster_hit_list = len(monster_hit_list)

          # Handle player positioning when they encounter a monster.
          for monster in monster_hit_list:
            if self.change_x > 0:
                self.rect.right = monster.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = monster.rect.right

          # Handle losing lives when the player hits the monster
          if len_monster_hit_list == 1:
            if self.original_len_monster_hit_list_x != len_monster_hit_list:
              self.lives = self.lose_life()
              # Play a sound when the player gets injured
             # injurySound = pygame.mixer.music.load("injurySound.mp3")
              #pygame.mixer.music.play()
          self.original_len_monster_hit_list_x = len_monster_hit_list

        # Handle collision with walls
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Handle collision with hidden walls
        hidden_block_hit_list = pygame.sprite.spritecollide(self, hiddenWalls, False)
        for block in hidden_block_hit_list:
            # If we are moving right, set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Handle collisions with monsters in the y direction
        if monsters != None:
          monster_hit_list = pygame.sprite.spritecollide(self,monsters,False)
          len_monster_hit_list = len(monster_hit_list)

          # Handle player positioning when they encounter a monster.
          for monster in monster_hit_list:
            if self.change_y > 0:
              self.rect.bottom = monster.rect.top
            else:
              self.rect.top = monster.rect.bottom

          # Handle losing lives when the player hits the monster
          if len_monster_hit_list == 1:
            if self.original_len_monster_hit_list_y != len_monster_hit_list:
              # Play a sound when the player gets injured
              #injurySound = pygame.mixer.music.load("injurySound.mp3")
              #pygame.mixer.music.play()
              self.lives = self.lose_life()
          self.original_len_monster_hit_list_y = len_monster_hit_list



        # Switches
        switches_hit_list = pygame.sprite.spritecollide(self,switches, False)
        len_switches_hit_list = len(switches_hit_list)

        # Handle character placement when they hit the switch
        for switch in switches_hit_list:
          if self.change_y > 0:
            self.rect.bottom = switch.rect.top
          else:
            self.rect.top = switch.rect.bottom

          # Activate the switch only once if the player hits it.
          if len_switches_hit_list == 1:
            if self.original_len_switch_hit_list_y != len_switches_hit_list:
              switch.isSwapped = True
          self.original_len_switch_hit_list_y = len_switches_hit_list


        block_hit_list = pygame.sprite.spritecollide(self, walls, False)

        # Handle collision with walls
        for block in block_hit_list:
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

        # Handle collision with hidden walls
        hidden_block_hit_list = pygame.sprite.spritecollide(self, hiddenWalls, False)
        for block in hidden_block_hit_list:
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

    # Add a life to the player (lambda function)
    add_life = lambda self : self.lives + 1

    # Remove a life from the player (lambda function)
    lose_life = lambda self : self.lives - 1

    # Increment the player's coin variable
    def add_coins(self):
      # If the player collects a coin play a sound
      #coinSound = pygame.mixer.music.load("coinSound.mp3")
      #pygame.mixer.music.play()
      self.coins += 1

# Creates the coin object
class Coin(pygame.sprite.Sprite):
  # Stores if the coin has been collected or not
  isCollected = False
  def __init__(self, x, y, width, height, color):
    """ Constructor function """

    # Call the parent's constructor
    super().__init__()

    # Handle colour parameter and set width, height of coin
    self.image = pygame.Surface([width, height])
    if color == None:
      pass
    else:
      self.image.fill(color)

    # Make our top-left corner the passed-in location.
    self.rect = self.image.get_rect()

    # Set the coin's x, y
    self.rect.y = y
    self.rect.x = x

  # Set's the coin's 'isCollected' var to True
  def collect(self):
    self.isCollected = True

# Create the switch object
class Switch(pygame.sprite.Sprite):

  # Stores whether the switch has been toggled or not
  isSwapped = False
  def __init__(self, x, y, width, height, color):
    """ Constructor function """

    # Call the parent's constructor
    super().__init__()

    # Handle the colour parameter. Set the switch's width and height
    self.image = pygame.Surface([width, height])
    if color == None:
      pass
    else:
      self.image.fill(color)

    # Make our top-left corner the passed-in location.
    self.rect = self.image.get_rect()

    # Set the switch's x, y
    self.rect.y = y
    self.rect.x = x

class Room(object):
    """ Base class for all rooms. """

    # Standard class variables for each room
    wall_list = None
    enemy_sprites = None
    coin_list = None
    hidden_coin_list = None
    monsters_list = None
    switch_list = None
    switch = None
    wallRemoved = None

    #Stores monster objects
    list_of_monsters = None

    #list of the y coordinate restrictions for the monsters
    y_monster_restrictions = None

    def __init__(self):
        """ Constructor, create our lists, sprite groups, and other variables """
        self.wall_list = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.coin_list = pygame.sprite.Group()
        self.hidden_coin_list = pygame.sprite.Group()
        self.monsters_list = pygame.sprite.Group()
        self.list_of_monsters = []
        self.y_monster_restrictions = []
        self.switch_list = pygame.sprite.Group()
        self.switch = None
        self.wallRemoved = False

# Third room in the game
class Room1(Room):
    def __init__(self, screen, background, player):
        super().__init__()
        self.background = background
        # Draw backgrouond
        screen.blit(background, (0, 0))

        # Set the player's coins to 0
        player.coins = 0

        # This is a list of walls. Each is in the form [x, y, width, height, colour]. The colour part is not drawn though. Only for testing
        walls = [
                 [665, 220, 10, 60, brown],

                 [20, 280,230, 10, brown],
                 [100,180,10, 50, brown],
                 [100, 90, 10, 40, brown],

                 [100, 90, 140, 10, brown],

                 [100, 220, 150, 10, brown],
                 [170, 90, 10, 80, brown],
                 [240, 180, 10, 40,brown],
                 [240, 90, 10, 40, brown],
                 [600, 420, 10, 60, brown],
                 [600, 350, 75, 10, brown],

                 [470, 420, 130, 10,brown],
                 [470, 360, 10, 60, brown],

                 [340, 360, 130, 10, brown],

                 [290, 280, 385, 10, brown],
                 [290, 280, 10, 130, brown],

                 [380, 420, 90, 10, brown],

                 [80, 340, 170, 10, brown],
                 [80, 340, 10, 70, brown],
                 [80, 410, 220, 10, brown],
                 [250, 220, 425, 10, brown]
                ]

        # Stors a list of the coins
        coins = [[200,110,20,20,black],
                 [630,60,20,20,black],
                 [110,370,20,20,black],
                 [440,385,20,20,black],
                 [640,315,20,20,black],
                 [165,55,20,20,black],
                 [530,350,20,20,black]
                ]

        # Stores a list of the hidden coind
        hiddenCoins = [[270,190,20,20,black]
                      ]

        # Stores a list of the monsters
        monsters = [[400,60,40,40,green],
                    [250,330,40,40,green]
                   ]

        # Stores the range at which each monster can move
        monsterRestrictions = [[150, 60],
                               [360, 230]
                              ]

        # Stores the switch
        switches = [[620, 400, 20, 20, green]
                   ]

        # Iterate through all the lists and add each to a sprite group, or a list
        for i in monsters:
          self.monster = Player(i[0],i[1],i[2],i[3],i[4])
          self.list_of_monsters.append(self.monster)
          self.monsters_list.add(self.monster)

        for i in monsterRestrictions:
          self.y_monster_restrictions.append(i)

        for i in hiddenCoins:
          coin = Coin(i[0], i[1], i[2], i[3], i[4])
          self.hidden_coin_list.add(coin)

        for i in switches:
            switch = Switch(i[0], i[1], i[2], i[3], i[4])
            self.switch = switch
            self.switch_list.add(switch)

        for i in coins:
          coin = Coin(i[0], i[1], i[2], i[3], i[4])
          self.coin_list.add(coin)

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

# Second room in the game
class Room2(Room):
    def __init__(self):
        super().__init__()

    def __init__(self, screen, background, player):
      super().__init__()
      self.background = background

      # Draw backgrouond
      screen.blit(background, (0, 0))

      # Set the player's coins to 0
      player.coins = 0

      # Reset the monster restrictions when the player goes onto the next map
      self.y_monster_restrictions = []

      # Create all of the visible walls (Same format as room 1)
      walls = [[315, 350, 15, 80, darkGrey],
               [380, 390, 15, 40, darkGrey],
               [120, 280, 400, 15, darkGrey],
               [175, 295, 15, 80, darkGrey],
               [120, 120, 15, 100, darkGrey],
               [120,120, 160, 15, darkGrey],
               [265, 80, 15, 50, darkGrey],
               [200, 205, 60, 15, darkGrey],
               [305, 80, 15, 200, darkGrey],
               [380, 80, 15, 140, darkGrey],
               [580, 280, 60, 15, darkGrey],
               [580, 295, 15, 90, darkGrey],
               [505, 295, 15, 80, darkGrey],
               [505, 140, 15, 140, darkGrey],
               [450, 80, 15, 140, darkGrey],

               [35, 225, 15, 50, darkGrey],
               [640, 225, 15, 50, darkGrey]
              ]

      # Stores all of the visible coins
      coins = [[225,85,20,20,blue],
                [255, 165, 20, 20,blue],
                [110,370,20,20,blue],
                [605,300,20,20,blue],
                [600,120,20,20,blue],
                [410,90,20,20,blue],
                [475,305,20,20,blue]
              ]

      # Stores all of the hidden coins
      hiddenCoins = [[600,230,20,20,blue]
                    ]

      # Stores all of the monsters
      monsters = [[450,295,40,40,green],
                  [150,135,40,40,green]
                  ]

      # Sets the range at which each monster can move
      monsterRestrictions = [[380, 295],
                               [230, 135]
                              ]

      # Iterate through all the lists and add each to a sprite group, or a list
      for item in walls:
          wall = Wall(item[0], item[1], item[2], item[3], item[4])
          self.wall_list.add(wall)
      for i in coins:
        coin = Coin(i[0], i[1], i[2], i[3], i[4])
        self.coin_list.add(coin)
      for i in hiddenCoins:
        coin = Coin(i[0], i[1], i[2], i[3], i[4])
        self.hidden_coin_list.add(coin)

      for i in monsters:
        self.monster = Player(i[0],i[1],i[2],i[3],i[4])
        self.list_of_monsters.append(self.monster)
        self.monsters_list.add(self.monster)

      for i in monsterRestrictions:
        self.y_monster_restrictions.append(i)

# First room in the game
class Room3(Room):
    def __init__(self):
        super().__init__()

    def __init__(self, screen, background, player):
      super().__init__()
      self.background = background
      # Draw backgrouond
      screen.blit(background, (0, 0))

      # Set the player's coins to 0
      player.coins = 0

      # Reset the monster restrictions when the player moves onto this map
      self.y_monster_restrictions = []

      # Create all of the visible walls (Same format as other rooms)
      walls = [[380, 360, 15, 70, darkBrown],
               [245,345, 150, 15, darkBrown],
               [135, 180, 15, 130, darkBrown],
               [250, 250, 220, 15, darkBrown],
               [300, 120, 15, 130, darkBrown],
               [470, 250, 15, 120, darkBrown],
               [470, 370, 70, 15, darkBrown],
               [525, 65, 15, 310, darkBrown],
               [580, 135, 15, 295, darkBrown],
               [375, 150, 100, 15, darkBrown],

               [325, 50, 50, 15, darkBrown],
               [35, 225, 15, 50, darkBrown]

              ]

      # Stores all of the coins
      coins = [[620, 70, 20, 20, blue],
               [495, 340, 20, 20, blue],
               [410, 100, 20, 20, blue],
               [75, 90, 20, 20, blue],
               [440, 280, 20, 20, blue],
               [135, 360, 20, 20, blue],
               [270, 220, 20, 20, blue]
              ]

      # Stores all of the hidden coins
      hiddenCoins = [[610, 390, 20, 20, blue]
                    ]

      # Stores all of the monsters
      monsters = [[165, 65, 40, 40, green]
                  ]

      # Stores the range at which the monsters can move on the map.
      monsterRestrictions = [[390,65]
                              ]

      # Iterate through all the lists and add each to a sprite group, or a list
      for item in walls:
          wall = Wall(item[0], item[1], item[2], item[3], item[4])
          self.wall_list.add(wall)
      for i in coins:
        coin = Coin(i[0], i[1], i[2], i[3], i[4])
        self.coin_list.add(coin)
      for i in hiddenCoins:
        coin = Coin(i[0], i[1], i[2], i[3], i[4])
        self.hidden_coin_list.add(coin)

      for i in monsters:
        self.monster = Player(i[0],i[1],i[2],i[3],i[4])
        self.list_of_monsters.append(self.monster)
        self.monsters_list.add(self.monster)

      for i in monsterRestrictions:
        self.y_monster_restrictions.append(i)

# Final room in the game (When you win or lose)
class Room4(Room):
    def __init__(self):
        super().__init__()

    def __init__(self, screen, background, player):
      super().__init__()
      self.background = background
      # Draw backgrouond
      screen.blit(background, (0, 0))

      # Set the player's coins to 0
      player.coins = 0

# Main function
def main():
  pygame.init()
  #pygame.mixer.init()

  # Create player object
  player = Player(330, 390, 40, 40, white)

  # Initialize the moving sprites sprite group and add the player to it
  movingsprites = pygame.sprite.Group()
  movingsprites.add(player)

  # Set the width and height of the screen
  size = (700, 500)
  screen = pygame.display.set_mode(size)

  # Set the window title
  pygame.display.set_caption("Escape the Labrynth")

  # Loop until the user clicks the close button.
  done = False

  # Load in the background images and scale them
  background1 = pygame.image.load('lightImage.png')
  background1 = pygame.transform.scale(background1, (700, 500))

  background2 = pygame.image.load('mistRoomCutFinal.png')
  background2 = pygame.transform.scale(background2, (700, 500))

  background3 = pygame.image.load('woodBackgroundCut.png')
  background3 = pygame.transform.scale(background3, (700, 500))

  background4 = pygame.image.load('lightImage.png')
  background4 = pygame.transform.scale(background4, (700, 500))

  # Save all character animations into a dictionary
  characterAnimations = {"characterDown":pygame.image.load('charDown.png'), "characterUp": pygame.image.load('charUp.png'), "characterRight":pygame.image.load('charRight.png'),
                         "characterLeft":pygame.image.load('charLeft.png'), "monsterUp":pygame.image.load('monsterUp.png'), "monsterDown":pygame.image.load('monsterDown.png')}

  # Initialize all lever images and scale them down
  leverStraight = pygame.image.load('leverStraight.png')
  leverStraight = pygame.transform.scale(leverStraight, (240, 107))
  leverToggled = pygame.image.load('leverToggled.png')
  leverToggled = pygame.transform.scale(leverToggled, (240, 107))

  # Set the font for the instruction and main page
  titleFont = pygame.font.Font(None, 75)
  headerFont = pygame.font.Font(None, 55)
  font = pygame.font.Font(None,36)

  # Says whether the player is still on the instruction screens and set the instruction page.
  display_instructions = True
  instruction_page = 1

  # Used to manage how fast the screen updates
  clock = pygame.time.Clock()

  # -------- Instruction Page Loop -----------
  # Handle the changing of the instructions page
  while not done and display_instructions:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        done = True
      if event.type == pygame.MOUSEBUTTONDOWN:
        instruction_page += 1
        if instruction_page ==4:
          display_instructions = False
    # Set the screen background
    screen.fill(black)

    # Set the background page for the instructions part and blit it
    background = pygame.image.load('lightImage.png')
    background = pygame.transform.scale(background1, (700, 500))
    screen.blit(background, (0, 0))

    # Instructions sequence
    if instruction_page == 1:
      #Draw instructions
      text = titleFont.render("Escape the Labrynth",True, white)
      screen.blit(text,[100,10])

      text = font.render("Click to continue",True, white)
      screen.blit(text,[10,70])

    if instruction_page == 2:
      #Draw instructions
      text = titleFont.render("Objective",True, white)
      screen.blit(text,[200,10])

      # Save each line of instructions to a dictionary
      content = {"1": "You have been captured by monsters and taken into their", "2": "labrynth. Your objective is to escape the labrynth while", "3":"only encountering the monsters up to 3 times. However, by", "4":"collecting 3 hidden coins around the map, you can gain", "5":"an extra encounter with the monster."}

      # Set the first y position of the first part of text
      y = 70

      # Iterate throught the dictionary and blit the text
      for key, val in content.items():
        screen.blit(font.render(val, True, white),[10,y])
        # Increment the y value for the text
        y += 30

    if instruction_page == 3:
      # Draw instructions
      text = titleFont.render("How to Play", True, white)
      screen.blit(text,[200,10])

      # Save each line of instructions to a dictionary
      content = {"1": "1.) Use the arrow keys to move around on the first map.", "2":"Click and hold directly right, left, up, or down of your", "3":"character to move around on the second map. ",
                 "4":"Keyboard controls are inverted on the third map", "5":"2.) Avoid monsters by not walking over them or you will", "6":"lose live(s). If you hit a monster in the same direction",
                 "7":"it's moving, you lose 2 lives. Sometimes the monsters", "8":"will push you away from them on contact.", "9":"3.) Walk over visible and hidden coins to collect them. If",
                 "10":"you collect 8 coins you gain an extra life", "11":"4.) Make it through the maps and have fun!"}

      # Set the first y position of the first part of text
      y = 70

      # Iterate throught the dictionary and blit the text
      for key, val in content.items():
        # If the line of text starts a new point, set the x position a bit back
        if key == "1" or key == "5" or key == "9" or key == "11":
            screen.blit(font.render(val, True, white),[10,y])
        else:
            screen.blit(font.render(val, True, white),[45,y])
        # Increment the y value for the text
        y += 30

    #Limit to 60 frames per second
    clock.tick(60)

    #Update the screen
    pygame.display.flip()

  # Store all of the room objects to a dictionary
  rooms = {"Room1":Room3(screen, background3, player), "Room2":Room2(screen, background2, player), "Room3":Room1(screen, background1, player), "Room4":Room4(screen, background4, player)}
  current_room = rooms["Room1"]

  # Set the current room number
  current_room_no = 0


  # ------- Main Program Loop --------
  while not done:

    # Main event loop
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        done = True
        # If user clicks close, it will end the main loop.

      # If it is room 1 or 3, use regular controls with the keyboard
      print(current_room_no)
      if current_room_no == 0 or current_room_no == 3:
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_LEFT:
            player.changespeed(-5, 0)
          if event.key == pygame.K_RIGHT:
            player.changespeed(5, 0)
          if event.key == pygame.K_UP:
            player.changespeed(0, -5)
          if event.key == pygame.K_DOWN:
            player.changespeed(0, 5)

        if event.type == pygame.KEYUP:
          if event.key == pygame.K_LEFT:
            player.changespeed(5, 0)
          if event.key == pygame.K_RIGHT:
            player.changespeed(-5, 0)
          if event.key == pygame.K_UP:
            player.changespeed(0, 5)
          if event.key == pygame.K_DOWN:
            player.changespeed(0, -5)

      # If it is the second room, use mouse controlls
      elif current_room_no == 1:
        print("True")
        if event.type == pygame.MOUSEBUTTONDOWN:
          x, y = event.pos
          if player.rect.x < x and player.rect.y <= y <=player.rect.y + 30:
            player.changespeed(5,0)
          elif player.rect.x > x and player.rect.y <= y <=player.rect.y + 30:
            player.changespeed(-5,0)
          if player.rect.y < y and player.rect.x <= x <= player.rect.x + 30:
            player.changespeed(0,5)
          elif player.rect.y > y and player.rect.x <= x <= player.rect.x + 30:
            player.changespeed(0,-5)
        if event.type == pygame.MOUSEBUTTONUP:
          player.change_x = 0
          player.change_y = 0

      # If it is the third room, use inverted controlls
      elif current_room_no == 2:
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_LEFT:
            player.changespeed(5, 0)
          if event.key == pygame.K_RIGHT:
            player.changespeed(-5, 0)
          if event.key == pygame.K_UP:
            player.changespeed(0, 5)
          if event.key == pygame.K_DOWN:
            player.changespeed(0, -5)

        if event.type == pygame.KEYUP:
          if event.key == pygame.K_LEFT:
            player.changespeed(-5, 0)
          if event.key == pygame.K_RIGHT:
            player.changespeed(5, 0)
          if event.key == pygame.K_UP:
            player.changespeed(0, -5)
          if event.key == pygame.K_DOWN:
            player.changespeed(0, 5)



    # Create the list for and initialize the hidden border walls for each room
    hiddenWallsSprite = pygame.sprite.Group()
    if current_room_no == 2:
      hiddenWalls = [[0, 0, 20, 500, white],
                    [0, 0, 700, 35, white],
                    [0, 465, 700, 35, white],
                    [680, 0, 20, 230, white],
                    [680, 280, 20, 300, white]]
    elif current_room_no == 1:
      hiddenWalls = [[30, 60, 20, 500, white],
                    [30, 60, 290, 20, white],
                    [380, 60, 400, 20, white],
                    [30, 430, 290, 35, white],
                    [390, 430, 400, 35, white],
                    [640, 0, 60, 700, white]
                    ]
    elif current_room_no == 0:
      hiddenWalls = [[30, 45, 20, 500, white],
                    [30, 45, 290, 20, white],
                    [380, 45, 400, 20, white],
                    [30, 430, 700, 35, white],
                    [640, 0, 60, 230, white],
                    [640, 270, 60, 500, white]
                    ]
    elif current_room_no == 3:
      hiddenWalls = [[0, 0, 20, 500, white],
                    [0, 0, 700, 35, white],
                    [0, 465, 700, 35, white],
                    [680, 0, 20, 700, white]
      ]

    # Add the hidden walls to the hidden walls sprite group
    for i in hiddenWalls:
      wall = Wall(i[0], i[1], i[2], i[3], i[4])
      hiddenWallsSprite.add(wall)

    # Move the player (call the move function)
    player.move(current_room.wall_list, current_room.coin_list, current_room.hidden_coin_list, current_room.monsters_list, current_room.switch_list, hiddenWallsSprite)

    # Handle movement between rooms
    if current_room_no == 2 and player.rect.x > 700:
      current_room_no = 3
      current_room = rooms["Room4"]
      player.change_x = 0
      player.change_y = 0
      player.rect.x = 330
      player.rect.y = 380
    elif current_room_no == 1 and player.rect.y < 40:
      current_room_no = 2
      current_room = rooms["Room3"]
      player.change_x = 0
      player.change_y = 0
      player.rect.x = 50
      player.rect.y = 220
    elif current_room_no == 0 and player.rect.x >= 640:
      current_room_no = 1
      current_room = rooms["Room2"]
      player.change_x = 0
      player.change_y = 0
      player.rect.x = 330
      player.rect.y = 380
    elif player.lives <= 0:
      player.change_x = 0
      player.change_y = 0
      current_room_no = 3
      current_room = rooms["Room4"]
    elif current_room_no == 1 and player.rect.y >=430:
      current_room_no = 0
      current_room = rooms["Room1"]
      player.change_x = 0
      player.change_y = 0
      player.rect.x = 560
      player.rect.y = 220

    # If the player gets 8 coins, add a life and reset the coin var
    if player.coins == 8:
      player.coins = 0
      player.lives += 1

    # If the player is on the second room, handle the switch
    if current_room_no == 2:
      # Will remove the exit wall if the switch is flipped
      if current_room.wallRemoved == False:
        if current_room.switch.isSwapped == True:
          current_room.wall_list.remove(current_room.wall_list.sprites()[0])
          current_room.wallRemoved = True

    # Set the monster's mouvement and the conditions if the player hits it.
    for i in range(0, len(current_room.list_of_monsters)):
      if current_room.list_of_monsters[i].hit_bottom_of_path == False:
        # If the monster hits the player, lose a life and play a sound
        if current_room.list_of_monsters[i].rect.y+30 == player.rect.y and current_room.list_of_monsters[i].rect.x-40 < player.rect.x < current_room.list_of_monsters[i].rect.x + 40:
          player.lose_life()
          #injurySound = pygame.mixer.music.load("injurySound.mp3")
          #pygame.mixer.music.play()
          current_room.list_of_monsters[i].hit_bottom_of_path = True
        # if the monster hits the player from below, change the monster's direction
        elif current_room.list_of_monsters[i].rect.y <= current_room.y_monster_restrictions[i][0]:
          current_room.list_of_monsters[i].rect.y += 1
          current_room.list_of_monsters[i].direction = 1
        else:
          current_room.list_of_monsters[i].hit_bottom_of_path = True
      if current_room.list_of_monsters[i].hit_bottom_of_path == True:
         # If the monster hits the player, lose a life and play a sound
        if current_room.list_of_monsters[i].rect.y == player.rect.y+40 and current_room.list_of_monsters[i].rect.x-40 < player.rect.x < current_room.list_of_monsters[i].rect.x + 40:
          player.lose_life()
          #injurySound = pygame.mixer.music.load("injurySound.mp3")
         # pygame.mixer.music.play()
          current_room.list_of_monsters[i].hit_bottom_of_path = False
        # if the monster hits the player from below, change the monster's direction
        elif current_room.list_of_monsters[i].rect.y >= current_room.y_monster_restrictions[i][1]:
          current_room.list_of_monsters[i].rect.y -= 1
          current_room.list_of_monsters[i].direction= -1
        else:
          current_room.list_of_monsters[i].hit_bottom_of_path = False

    # Draw all sprites on the screen
    current_room.wall_list.draw(screen)
    current_room.hidden_coin_list.draw(screen)
    current_room.monsters_list.draw(screen)
    current_room.switch_list.draw(screen)
    hiddenWallsSprite.draw(screen)
    movingsprites.draw(screen)

    # Blit the background for the level
    screen.blit(current_room.background, (0,0))

    # Only make walls the visible sprite on the map. Everything else is added through images and not the pygame shapes.
    current_room.wall_list.draw(screen)

    # Display the player's current lives
    colour = white
    lives = font.render(str(player.lives) + " Lives", True, colour)
    screen.blit(lives, [600,0])

    # Display the player's current coins
    coins = font.render(str(player.coins) + " Coins", True, colour)
    screen.blit(coins, [400,0])

    # Handle the player going to the end map when they win or lose
    if current_room_no == 3:
      if player.lives > 0:
        endMessage = titleFont.render("You Win!", True, white)
        screen.blit(endMessage, [250,200])
      else:
        endMessage = titleFont.render("You Lose!", True, white)
        screen.blit(endMessage, [250,200])

    #Handle the character animations, if they are moving left display the left animation on top of the character square, if they are moving right display the right animation on top of the character square, ...
    if player.change_x <0:
      screen.blit(characterAnimations["characterLeft"],[player.rect.x-380,player.rect.y-880])
    elif player.change_x >0:
      screen.blit(characterAnimations["characterRight"],[player.rect.x-380,player.rect.y-820])
    elif player.change_y <0:
      screen.blit(characterAnimations["characterUp"],[player.rect.x-380,player.rect.y-940])
    elif player.change_y >0:
      screen.blit(characterAnimations["characterDown"],[player.rect.x-270,player.rect.y-760])
    elif player.change_x == 0 and player.change_y == 0:
      screen.blit(characterAnimations["characterDown"],[player.rect.x-270,player.rect.y-760])

    # Handle the monster animations, if they are moving up, display the up animation. If they are moving down, display the down animation.
    for i in current_room.list_of_monsters:
      if i.direction == -1:
        screen.blit(characterAnimations["monsterUp"],[i.rect.x-230,i.rect.y-1160])
      elif i.direction == 1:
        screen.blit(characterAnimations["monsterDown"],[i.rect.x-230,i.rect.y-950])

    # Draw yellow circles on top of each coin rectangle
    for i in current_room.coin_list:
      pygame.draw.ellipse(screen, yellow, [i.rect.x, i.rect.y, 20, 20])

    # If the lever is swapped on the last map, remove the wall blocking the exit
    if current_room_no == 2:
        if current_room.wallRemoved == True:
            screen.blit(leverToggled, [500, 325])
        else:
            screen.blit(leverStraight,[530,325])

    pygame.display.flip()

    clock.tick(60)

  # Close the window and quit
  pygame.quit()

if __name__ == "__main__":
  main()