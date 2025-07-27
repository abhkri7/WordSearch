import random
from copy import deepcopy
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
bold_alphabet = "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭"
class Grid:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.words_array = []
        self.word_count = 0
        self.words_choice = []
        self.used_spaces = []
        self.grid = []
    def _parse_mode(self,file_name):
        with open(file_name) as f:
            self.width, self.height, self.word_count = (int(f.readline()) for _ in range(3))
            for word in f:
                self.words_array.append(word.replace("\n","").replace(" ","").upper())
        print(f"In this mode, there are {len(self.words_array)} words possible.")
                
    def generateBlankGrid(self):
        for _ in range(self.height):
            self.grid.append([alphabet[random.randint(0, 25)] for _ in range(self.width)])
            
    def printGrid(self, answers = False):
        if not answers:
            height = len(self.grid)
            for i in range(height):
                print(" ".join(self.grid[i]))
        else:
            height = len(self.grid)
            width = len(self.grid[0])
            for i in range(height):
                for j in range(width):
                    if((j,i) in self.used_spaces):
                        self.grid[i][j] = bold_alphabet[alphabet.index(self.grid[i][j])]
                    print(self.grid[i][j], end=" ")
                print("")
                
    def initialize(self, mode_file):
        self._parse_mode(mode_file)
        while len(self.words_choice) < self.word_count:
            rand = random.randint(0, len(self.words_array) - 1)
            rand_word = self.words_array[rand]
            self.words_array.pop(rand)
            self.words_choice.append(rand_word)
        self.generateBlankGrid()
        working = self.place_words()
        while not working:
            self.generateBlankGrid()
            working = self.place_words()
        self.printGrid()
        print("Look For:")
        for word in self.words_choice:
            print(word)

    def find_preliminary_orientations(self, x, y, w_len, diagonals=True):
        """
        Determines the orientations the word can be placed from the first letter.
        It does not take into account any other words' placements
        """
        orients = []
        #Check if word can be placed horizontally or vertically
        if (y + 1 >= w_len):
            orients.append((0,-1))
        if (x + 1 >= w_len):
            orients.append((-1,0))  
        if (y <= self.height - w_len):
            orients.append((0,1)) 
        if (x <= self.width - w_len):
            orients.append((1, 0))
        if (diagonals):
            #Check if word can be placed diagonally 
            if (((0,1) in orients) and ((1,0) in orients)):
                orients.append((1,1))
            if (((1,0) in orients) and ((0,-1) in orients)):
                orients.append((1,-1))
            if (((0,-1) in orients) and ((-1, 0) in orients)):
                orients.append((-1,-1))
            if (((-1, 0) in orients) and ((0,1)in orients)):
                orients.append((-1,1))
        return orients
    def determine_filtered_placements(self, x, y, word, diagonals=True): 
        w_len = len(word)
        p_orient = self.find_preliminary_orientations(x, y, w_len, diagonals)
        cops_list = []
        for k, orient in enumerate(p_orient):
            conflict = False
            #print(f"******* Starting Orient {orient} *******")
            
            #Current Orient Positions
            cop = []
            
            dx = x
            dy = y
            for _ in range(w_len):
                cop.append((dx,dy))
                dx += orient[0]
                dy += orient[1]
            #print(f"C.O.P: {cop}")
            for item in cop:
                if item in self.used_spaces:
                    conflict = True
                    break
            if conflict:
                p_orient[k] = ""
            else:
                cops_list.append(cop)
        p_orient = list(filter(lambda t: t != "", p_orient))
        #print("Filtered orients: ", p_orient)
        return dict(zip(p_orient, cops_list))
    def place_words(self):
        #print("PLACING WORDS")
        WORD_PLACEMENTS = dict()
        for word in self.words_choice:
            success = 0
            invalid_spaces = deepcopy(self.used_spaces)
            while not success:
                placement = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
                if len(invalid_spaces) == self.width * self.height:
                    self.used_spaces = []
                    return 0
                while placement in invalid_spaces:
                    placement = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))    
                orients = self.determine_filtered_placements(placement[0], placement[1], word)
                
                try:
                    final_placement = random.choice(list(orients.items()))
                    success += 1
                except IndexError:
                    invalid_spaces.append(placement)
            self.used_spaces.extend(final_placement[1])
            WORD_PLACEMENTS[word] = final_placement[1]
        for word, indices in WORD_PLACEMENTS.items():
            for index, coord in enumerate(indices):
                self.grid[coord[1]][coord[0]] = word[index];
        return 1
