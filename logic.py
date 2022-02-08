try:
    import numpy as np
except:
    import _numpypy as np

RIGHT = 0
DOWN = 1

wds_w_fr = True
wds_w_fr_sm = True

import time, random

words = set()
with open( "words.txt" if not wds_w_fr else "wwf_words.txt", "r" ) as words_file:
    for word in words_file:
        words.add(word.strip().upper())

blank_cache = {}

def is_word2( word, letter_options, is_main_word, blank_index ):
    if len( word ) < 2: return False
    if "_" in word:            
        num_blanks = word.count("_")
        if is_main_word:
            letter_options.clear()
            if word in blank_cache:
                letter_options.extend( blank_cache[word] )
                return len( letter_options ) > 0

            def recursive_add( sub_string ):
                if len( sub_string ) < num_blanks:
                    for new_letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                        recursive_add( sub_string + new_letter )
                else:
                    letter_options.append( sub_string )
            recursive_add( "" )

        i = 0
        while i < len(letter_options):
            test_word = word
            if is_main_word:
                for test_letter in letter_options[i]:
                    test_word = test_word.replace( "_", test_letter, 1 )
            else:
                test_letter = letter_options[i][blank_index]
                test_word = test_word.replace( "_", test_letter, 1 )

            if test_word.upper() in words:
                i += 1
            else:
                del letter_options[i]

        #only the main word is cached because it doesn't depend on a main
        #word's sub selection of letters.
        if is_main_word:
            blank_cache[word] = letter_options

        return len( letter_options ) > 0 
    else:
        return  word.upper() in words


        
        

# def is_word( word, letter_options, blank_index=0 ):
#     if "_" in word:
#         if blank_index >= len( letter_options ):
#             letter_options.append( "ABCDEFGHIJKLMNOPQRSTUVWXYZ" )
#         if letter_options[blank_index] == "": return False
#         working_letters = ""
#         for test_letter in letter_options[blank_index]:
#             test_word = word.replace( "_", test_letter, 1 )
#             if is_word( test_word, letter_options, blank_index+1 ):
#                 working_letters += test_letter
#         letter_options[blank_index] = working_letters
#         if len( working_letters ) > 0:
#             return True
#         else:
#             return False
#     else:
#         return  word.upper() in words

class Board:
    size = 15 if not wds_w_fr_sm else 11

    special_squares = [\
      ["tw",""  ,""  ,"dl",""  ,""  ,""  ,"tw",""  ,""  ,""  ,"dl",""  ,""  ,"tw"],
      [""  ,"dw",""  ,""  ,""  ,"tl",""  ,""  ,""  ,"tl",""  ,""  ,""  ,"dw",""  ],
      [""  ,""  ,"dw",""  ,""  ,""  ,"dl",""  ,"dl",""  ,""  ,""  ,"dw",""  ,""  ],
      ["dl",""  ,""  ,"dw",""  ,""  ,""  ,"dl",""  ,""  ,""  ,"dw",""  ,""  ,"dl"],
      [""  ,""  ,""  ,""  ,"dw",""  ,""  ,""  ,""  ,""  ,"dw",""  ,""  ,""  ,""  ],
      [""  ,"tl",""  ,""  ,""  ,"tl",""  ,""  ,""  ,"tl",""  ,""  ,""  ,"tl",""  ],
      [""  ,""  ,"dl",""  ,""  ,""  ,"dl",""  ,"dl",""  ,""  ,""  ,"dl",""  ,""  ],
      ["tw",""  ,""  ,"dl",""  ,""  ,""  ,"s" ,""  ,""  ,""  ,"dl",""  ,""  ,"tw"],
      [""  ,""  ,"dl",""  ,""  ,""  ,"dl",""  ,"dl",""  ,""  ,""  ,"dl",""  ,""  ],
      [""  ,"tl",""  ,""  ,""  ,"tl",""  ,""  ,""  ,"tl",""  ,""  ,""  ,"tl",""  ],
      [""  ,""  ,""  ,""  ,"dw",""  ,""  ,""  ,""  ,""  ,"dw",""  ,""  ,""  ,""  ],
      ["dl",""  ,""  ,"dw",""  ,""  ,""  ,"dl",""  ,""  ,""  ,"dw",""  ,""  ,"dl"],
      [""  ,""  ,"dw",""  ,""  ,""  ,"dl",""  ,"dl",""  ,""  ,""  ,"dw",""  ,""  ],
      [""  ,"dw",""  ,""  ,""  ,"tl",""  ,""  ,""  ,"tl",""  ,""  ,""  ,"dw",""  ],
      ["tw",""  ,""  ,"dl",""  ,""  ,""  ,"tw",""  ,""  ,""  ,"dl",""  ,""  ,"tw"] ] \
        if not wds_w_fr else \
      ([\
      [""  ,""  ,""  ,"tw",""  ,""  ,"tl",""  ,"tl",""  ,""  ,"tw",""  ,""  ,""  ],
      [""  ,""  ,"dl",""  ,""  ,"dw",""  ,""  ,""  ,"dw",""  ,""  ,"dl",""  ,""  ],
      [""  ,"dl",""  ,""  ,"dl",""  ,""  ,""  ,""  ,""  ,"dl",""  ,""  ,"dl",""  ],
      ["tw",""  ,""  ,"tw",""  ,""  ,""  ,"dw",""  ,""  ,""  ,"tw",""  ,""  ,"tw"],
      [""  ,""  ,"dl",""  ,""  ,""  ,"dl",""  ,"dl",""  ,""  ,""  ,"dl",""  ,""  ],
      [""  ,"dw",""  ,""  ,""  ,"tw",""  ,""  ,""  ,"tw",""  ,""  ,""  ,"dw",""  ],
      [""  ,""  ,""  ,""  ,"dl",""  ,""  ,""  ,""  ,""  ,"dl",""  ,""  ,""  ,"tl"],
      [""  ,""  ,""  ,"dw",""  ,""  ,""  ,"s" ,""  ,""  ,""  ,"dw",""  ,""  ,""  ],
      ["tl",""  ,""  ,""  ,"dl",""  ,""  ,""  ,""  ,""  ,"dl",""  ,""  ,""  ,"tl"],
      [""  ,"dw",""  ,""  ,""  ,"tw",""  ,""  ,""  ,"tw",""  ,""  ,""  ,"dw",""  ],
      [""  ,""  ,"dl",""  ,""  ,""  ,"dl",""  ,"dl",""  ,""  ,""  ,"dl",""  ,""  ],
      ["tw",""  ,""  ,"tw",""  ,""  ,""  ,"dw",""  ,""  ,""  ,"tw",""  ,""  ,"tw"],
      [""  ,"dl",""  ,""  ,"dl",""  ,""  ,""  ,""  ,""  ,"dl",""  ,""  ,"dl",""  ],
      [""  ,""  ,"dl",""  ,""  ,"dw",""  ,""  ,""  ,"dw",""  ,""  ,"dl",""  ,""  ],
      [""  ,""  ,""  ,"tw",""  ,""  ,"tl",""  ,"tl",""  ,""  ,"tw",""  ,""  ,""  ] ] \
      if not wds_w_fr_sm else \
      [\
      ["tl",""  ,"tw",""  ,""  ,""  ,""  ,""  ,"tw",""  ,"tl"],
      [""  ,"dw",""  ,""  ,""  ,"dw",""  ,""  ,""  ,"dw",""  ],
      ["tw",""  ,"tl",""  ,"dl",""  ,"dl",""  ,"tl",""  ,"tw"],
      [""  ,""  ,""  ,"tl",""  ,""  ,""  ,"tl",""  ,""  ,""  ],
      [""  ,""  ,"dl",""  ,""  ,""  ,""  ,""  ,"dl",""  ,""  ],
      [""  ,"dw",""  ,""  ,""  ,"s" ,""  ,""  ,""  ,"dw",""  ],
      [""  ,""  ,"dl",""  ,""  ,""  ,""  ,""  ,"dl",""  ,""  ],
      [""  ,""  ,""  ,"tl",""  ,""  ,""  ,"tl",""  ,""  ,""  ],
      ["tw",""  ,"tl",""  ,"dl",""  ,"dl",""  ,"tl",""  ,"tw"],
      [""  ,"dw",""  ,""  ,""  ,"dw",""  ,""  ,""  ,"dw",""  ],
      ["tl",""  ,"tw",""  ,""  ,""  ,""  ,""  ,"tw",""  ,"tl"]])
      


    letter_scores = { 
        "a":1,
        "b":3,
        "c":3,
        "d":2,
        "e":1,
        "f":4,
        "g":2,
        "h":4,
        "i":1,
        "j":8,
        "k":5,
        "l":1,
        "m":3,
        "n":1,
        "o":1,
        "p":3,
        "q":10,
        "r":1,
        "s":1,
        "t":1,
        "u":1,
        "v":4,
        "w":4,
        "x":8,
        "y":4,
        "z":10,
        " ":0
    } if not wds_w_fr else {
        "a":1,
        "b":4,
        "c":4,
        "d":2,
        "e":1,
        "f":4,
        "g":3,
        "h":3,
        "i":1,
        "j":10,
        "k":5,
        "l":2,
        "m":4,
        "n":2,
        "o":1,
        "p":4,
        "q":10,
        "r":1,
        "s":1,
        "t":1,
        "u":2,
        "v":5,
        "w":4,
        "x":8,
        "y":3,
        "z":10,
        " ":0
    }

    scores = None
    played_spaces = None

    def __init__ (self ):
        self.clear_board()

    def clear_board( self ):
        self.scores = {}
        self.played_spaces = np.asarray([[""]*self.size]*self.size)



    def get_played_spaces( self ):
        return self.played_spaces.tolist()



    def find_word_gen( self, letters ):
        #lowercase the letters because blanks are represented
        #internally as capitals.
        #To pass in a blank use a space or underscore
        letters = letters.lower().replace( " ", "_" ).replace( "*", "_" )
        half_size = int((self.size-1)*.5)

        max_length_searched = [0]
        best_score = [0]

        print( "starting word search" )

        min_x_played, min_y_played, max_x_played, max_y_played = 0,0,0,0
        for x in range( -half_size, half_size+1 ):
            for y in range( -half_size, half_size+1 ):
                if self.played_spaces[y+half_size,x+half_size] != "":
                    min_x_played = min( min_x_played, x )
                    max_x_played = max( max_x_played, x )
                    min_y_played = min( min_y_played, y )
                    max_y_played = max( max_y_played, y )

        def combo_letters( picked_letters, remaining_letters, length_test ):
            if len( picked_letters ) > max_length_searched[0]:
                max_length_searched[0] = len( picked_letters )
                print( "searching using " + str(max_length_searched[0]) + " letters")
                yield ["log_message", "searching using " + str(max_length_searched[0]) + " letters" ]
            
            if len( picked_letters ) == length_test:
                for direction in [RIGHT,DOWN]:
                    x_start = y_start = -half_size
                    x_end   = y_end   =  half_size

                    y_end   = min(  max_y_played+1, y_end )
                    x_end   = min(  max_x_played+1, x_end )

                    #trim the search dimensions down to where it could
                    #possibly fit.
                    if direction == RIGHT:
                        x_start = max(  min_x_played-len(picked_letters), x_start )
                        y_start = max(  min_y_played-1, y_start )
                        x_end   = min(  half_size-len(picked_letters), x_end )
                    else:
                        x_start = max(  min_x_played-1, x_start )
                        y_start = max(  min_y_played-len(picked_letters), y_start )
                        y_end   = min(  half_size-len(picked_letters), y_end )
                    

                    for x in range( x_start, x_end+1 ):
                        for y in range( y_start, y_end+1 ):
                            try:
                                test_score, _, test_word = self.test_word( picked_letters, x, y, direction, skipy=True )
                                
                                if test_score > best_score[0]:
                                    print( "Found word " + test_word + " at " + str( x ) + "," + str( y ) + " going " + ("down" if direction == DOWN else "right" ) + " for " + str( test_score ) + " points" )
                                    print( "b.play_word( \"" + test_word + "\"," + str( x ) + "," + str( y ) + "," + ("DOWN" if direction == DOWN else "RIGHT" ) + ",  \"\"  )" )
                                    yield ["found_word", { "word": test_word, "x": x, "y": y, "direction": direction, "points":test_score  } ]
                                    yield ["log_message", "Found word " + test_word + " at " + str( x ) + "," + str( y ) + " going " + ("down" if direction == DOWN else "right" ) + " for " + str( test_score ) + " points" ] 
                                    best_score[0] = test_score

                                # if "_" in picked_letters:
                                #     print( "Found _ word " + test_word + " at " + str( x ) + "," + str( y ) + " going " + ("down" if direction == DOWN else "right" ) + " for " + str( test_score ) + " points" )

                            except:
                                pass     
            elif len( picked_letters ) < length_test:
                for letter_num in range( len( remaining_letters ) ):
                    new_picked_letters = picked_letters + remaining_letters[letter_num]
                    new_remaining_letters = remaining_letters[:letter_num] + remaining_letters[letter_num+1:]
                    for result in combo_letters( new_picked_letters, new_remaining_letters, length_test ):
                        yield result

        for length_test in range( 1, len( letters )+1 ):
            for result in combo_letters( "", letters, length_test ):
                yield result

        yield ["log_message", "Done searching." ]
        yield ["alert", "Done searching."]
        print( "Done searching" )

            
    def find_word( self, letters ):
        gen = self.find_word_gen( letters )
        for _ in gen:
            pass

    #Use upper case letters in the word to represent picked blank letters.
    def play_word( self, word, x,y, direction, who="", skipy=False, speak=True ):
        self.word_finder = None
        score, self.played_spaces, constructed_main_word = self.test_word( word, x, y, direction, skipy )
        if not who in self.scores:
            self.scores[who] = 0
        self.scores[who] += score
        if speak:
            print( "Scored " + str(score) + " points for word " + constructed_main_word + " for a total of " + str(self.scores[who]) + " for " + who )
        return score, constructed_main_word
    
    def adjust_score( self, amount, who, speak=True ):
        if not who in self.scores:
            self.scores[who] = 0
        self.scores[who] += amount
        if speak:
            print( "Adjusted " + who + " " + str(amount) + " points to " + str(self.scores[who]) )

    def test_word( self, word, x, y, direction, skipy ):

        test_board = np.copy( self.played_spaces )

        x_0,y_0 = int(x+((self.size-1)*.5)),int(y+((self.size-1)*.5))

        #keep track of what letters will work for any blanks.
        valid_blank_choices = []
        
        #keep track of how many leters are actually placed if we are not using skipy mode.
        placed_letters = 0

        #check if the letters will phisically fit
        strech_num = 0
        for letter in word:
            occupied = True
            sticking_with_occupied = False
            while occupied and not sticking_with_occupied:
                test_x,test_y = x_0,y_0
                if direction==RIGHT:
                    test_x += strech_num
                    if test_x >= self.size: raise Exception( "Off board" )
                else:
                    test_y += strech_num
                    if test_y >= self.size: raise Exception( "Off board" )

                if test_board[test_y,test_x] == "": 
                    occupied = False
                else:
                    if skipy:
                        strech_num += 1
                    else:
                        sticking_with_occupied = True

            if occupied and test_board[test_y,test_x] != letter:
                raise Exception( "Occupied" )
            
            
            if not occupied:
                placed_letters += 1

            #place the letter
            test_board[test_y,test_x] = letter
            strech_num += 1

        #check if all the words made are words
        #first check inline word.
        start_x,start_y=x_0,y_0
        can_backup = True
        while can_backup:
            prev_x,prev_y=start_x,start_y
            if direction==RIGHT:
                prev_x -= 1
            else:
                prev_y -= 1
    
            if prev_x < 0 or prev_y < 0 or test_board[prev_y,prev_x] == "":
                can_backup = False
            else:
                start_x, start_y = prev_x, prev_y

        is_connected_to_something = False
        total_word_score = 0
        this_word_score = 0
        word_multiple = 1

        #if seven letters were placed then we get a bingo.
        if placed_letters >= 7:
            total_word_score += 35 if wds_w_fr else 50

        constructed_main_word = ""
        walking_x,walking_y=start_x,start_y
        another_letter = True
        first_letter = True
        while another_letter:
            next_x,next_y=walking_x,walking_y
            if first_letter:
                first_letter = False
            else:
                if direction==RIGHT:
                    next_x += 1
                else:
                    next_y += 1
            if next_x >= self.size or next_y >= self.size or test_board[next_y,next_x] == "":
                another_letter = False
            else:
                walking_x,walking_y = next_x,next_y
                this_letter = test_board[walking_y,walking_x]
                constructed_main_word += this_letter
                #upper case letters represent picked blank letters.
                this_letter_score = self.letter_scores[this_letter] if this_letter.islower() else 0
                if self.played_spaces[walking_y,walking_x] != "": 
                    is_connected_to_something = True
                else:
                    #as we played this letter, see if it is on something special
                    this_special = self.special_squares[walking_y][walking_x]
                    if this_special == "dl":
                        this_letter_score *= 2
                    elif this_special == "tl":
                        this_letter_score *= 3
                    elif this_special == "dw":
                        word_multiple *= 2
                    elif this_special == "tw":
                        word_multiple *= 3
                    elif this_special == "s":
                        #TODO:  I think with non words with friends
                        #This should make a word_multiple *2 as well
                        #but I want to research before doing it.
                        is_connected_to_something = True
                this_word_score += this_letter_score
        total_word_score += this_word_score * word_multiple


        if not is_word2( constructed_main_word, valid_blank_choices, True, -1 ): raise Exception( "Not a word " + constructed_main_word )

        #now check all the side words
        root_walker_x,root_walker_y=x_0,y_0
        still_walking_root = True
        first_root_letter = True
        root_walk_blank_count = -1
        while still_walking_root:
            if first_root_letter:
                first_root_letter = False
            else:
                if direction==RIGHT:
                    root_walker_x+=1
                else:
                    root_walker_y+=1
            if root_walker_x >= self.size or root_walker_y >= self.size or test_board[root_walker_y,root_walker_x] == "":
                still_walking_root = False
            else:
                #only check spirs if the letter placed is ours.
                if self.played_spaces[root_walker_y,root_walker_x] == "":

                    #keep track of which blank is appart of a possible spir word.
                    if test_board[root_walker_y,root_walker_x] == "_": root_walk_blank_count += 1

                    #check for spirs.
                    start_x,start_y=root_walker_x,root_walker_y
                    can_backup = True
                    while can_backup:
                        prev_x,prev_y=start_x,start_y
                        if direction==DOWN: #wrong direction on purpose for spirs.
                            prev_x -= 1
                        else:
                            prev_y -= 1
                        if prev_x < 0 or prev_y < 0 or test_board[prev_y,prev_x] == "":
                            can_backup = False
                        else:
                            start_x, start_y = prev_x, prev_y
                            
                    this_word_score = 0
                    word_multiple = 1

                    constructed_spir_word = ""
                    walking_x,walking_y=start_x,start_y
                    another_letter = True
                    first_letter = True
                    while another_letter:
                        next_x,next_y=walking_x,walking_y
                        if first_letter:
                            first_letter = False
                        else:
                            if direction==DOWN: #wrong direction on purpose for spirs.
                                next_x += 1
                            else:
                                next_y += 1
                        if next_x >= self.size or next_y >= self.size or test_board[next_y,next_x] == "":
                            another_letter = False
                        else:
                            walking_x,walking_y = next_x,next_y
                            this_letter = test_board[walking_y,walking_x]
                            constructed_spir_word += this_letter
                            this_letter_score = self.letter_scores[this_letter] if this_letter.islower() else 0

                            if self.played_spaces[walking_y,walking_x] != "": 
                                is_connected_to_something = True
                            else:
                                #as we played this letter, see if it is on something special
                                this_special = self.special_squares[walking_y][walking_x]
                                if this_special == "dl":
                                    this_letter_score *= 2
                                elif this_special == "tl":
                                    this_letter_score *= 3
                                elif this_special == "dw":
                                    word_multiple *= 2
                                elif this_special == "tw":
                                    word_multiple *= 3
                            this_word_score += this_letter_score

                    #take spir words seriously only if they are longer then one letter.
                    if len( constructed_spir_word ) > 1:
                        if not is_word2( constructed_spir_word, valid_blank_choices, False, root_walk_blank_count ): raise Exception( "Not a word " + constructed_spir_word )
                        
                        total_word_score += this_word_score * word_multiple
        

        #check that the word connects or touches the start
        if not is_connected_to_something: raise Exception( "Not connected" )
        
    
        if "_" in constructed_main_word:
            chosen_valid_letters = random.choice( valid_blank_choices )

        blank_choice_index = 0
        while "_" in constructed_main_word:
            # if constructed_main_word == "dog__":
            #     print( "What did this do?")
            #pick the letter from the randomly chosen valid letters
            chosen_letter = chosen_valid_letters[blank_choice_index]
            #figure out how far into the word the offset is
            letter_offset = constructed_main_word.index("_")

            #figure out where in the test_board that offset goes
            replace_x, replace_y = x_0, y_0
            if direction==RIGHT:
                replace_x += letter_offset
            else:
                replace_y += letter_offset
            test_board[replace_y,replace_x] = chosen_letter
            constructed_main_word = constructed_main_word.replace( "_", chosen_letter, 1 )

            blank_choice_index += 1


        return total_word_score, test_board, constructed_main_word

#TODO: need to implement BINGOs.
def main():
    b = Board()
    # b.play_word( "dog", 0, 0, RIGHT )
    # b.play_word( "is" , 3,-1, DOWN  )
    # b.play_word( "lanai", -1, -1, RIGHT )
    # b.play_word( "shames", 0,1, RIGHT )
    # b.play_word( "fascine", 5,-1, DOWN )
    # b.play_word( "gazal", -4,-2, RIGHT )
    # b.play_word( "jaga", 2,-2, DOWN )
    # b.play_word( "born", 4,3, DOWN )
    # b.play_word( "rax", 6,-2, DOWN )
    # b.play_word( "auf", -5,-3, RIGHT )
    # b.play_word( "dev", 7,-1, DOWN )
    # b.play_word( "tatt", -7,-4, RIGHT )
    # b.play_word( "hoed", 6,2, DOWN )
    # b.play_word( "punce", 0,7, RIGHT )
    # b.play_word( "twite", -7,-7, DOWN )
    # b.play_word( "womb", -7,-6, RIGHT )
    # b.play_word( "egoism", 3,-4, DOWN )
    # b.play_word( "quern", 1, -4, RIGHT )
    # b.play_word( "ofter", -4,-7, RIGHT )
    # b.play_word( "ide", -7,-5, RIGHT )
    # b.play_word( "kyes", 6, -7, DOWN )
    # b.play_word( "trike", 3, -7, RIGHT )
    # b.play_word( "prow", 4, -5, DOWN )
    # b.play_word( "chi", 5,2, RIGHT )
    # b.play_word( "fy", -3,-7, DOWN )
    # b.play_word( "peel", 4,-5, RIGHT )
    # b.play_word( "iron", -2,6, RIGHT )
    # b.play_word( "qi", 1, -4, DOWN )
    # b.play_word( "ired", 3,5, RIGHT )
    # b.play_word( "luv", 2,3, DOWN )
    #b.find_word( "aaineln" )
    #b.find_word( "hssaema" )
    #b.find_word( "ienfcar" )
    #b.find_word( "algnrza" )
    #b.find_word( "rdxtjgt")
    #b.find_word( "nrtttob" )
    #b.find_word( "rdxttga" )
    #b.find_word( "tttfaua" )
    #b.find_word( "dttghev" )
    #b.find_word( "ttanut" )
    #b.find_word( "ttghode" )
    #b.find_word( "nutcpeb" )
    #b.find_word( "tgteewi" )
    #b.find_word( "abcdefghijklmnopqrstuvwxyz")
    #b.find_word( "tbmnrou" )
    #b.find_word( "rgteeok" )
    #b.find_word( "tnruqrd" )
    #b.find_word( "ftrkoye" )
    #b.find_word( "trdlvel" )
    #b.find_word( "kywsroe" )
    #b.find_word( "trlvlie" )
    #b.find_word( "wropiin" )
    #b.find_word( "lvliuei" )
    #b.find_word( "riinoyi" )
    #b.find_word( "lvluei" )
    #b.find_word( "riinoi" )
    #b.find_word( "vlui" )
    #b.find_word( "ii" )
    #b.find_word( "vlu" )
    # b.find_word( "i" )

    # b.play_word( "touzy", 0, 0, RIGHT, "comp" ) #comp
    # b.play_word( "oy", 0, 1, RIGHT, "Josh" ) #Joshua
    # b.play_word( "zenith", 3, 0, DOWN, "Jessica" ) #Jessica
    # b.play_word( "hit", 3, 5, RIGHT, "Hannah" ) #Hannah
    # b.play_word( "diether", 0, 4, RIGHT, "comp" )#comp
    # b.play_word( "rails", 7, 0, DOWN, "Josh" ) #josh
    # b.play_word( "duet", 0, 4, DOWN, "Jessica" ) #Jessica
    # b.play_word( "nurse", -4, 2, RIGHT, "Hannah"  ) #hannah
    # b.play_word( "loricae", -6,6, RIGHT, "comp" ) #comp
    # b.play_word( "qi", 6, 2, RIGHT, "Josh" ) #Josh
    # b.play_word( "xi", -7, 7, RIGHT, "Jessica" ) # Jessica
    # b.play_word( "coned", -4, 0, DOWN, "Hannah" ) #hannah
    # b.play_word( "finca", -7, 0, RIGHT, "comp" ) #comp
    # b.play_word( "os", 2, 6, RIGHT, "Josh" ) #Josh
    # b.play_word( "mingy", 4, -4, DOWN, "Jessica" ) #Jessica
    # b.play_word( "joy", 1,-1,DOWN, "Hannah" ) #hannah
    # b.play_word( "befog", 3, -7, DOWN, "comp" ) #comp
    # b.play_word( "breve", 3, -7, RIGHT, "Josh" ) #Josh
    # b.play_word( "bang", -5, -2, DOWN, "Jessica" )
    # b.play_word( "wop", 2, -6, DOWN, "Hannah" )

    #b.find_word( "ouelfgb" )
    #b.find_word( "bagoark" )
    #b.find_word("aoedpiw")
    # b.find_word( "ulmtpan")

    #b.play_word( "fish", 0, 0, RIGHT )
    #b.find_word( "dog___" )
    #b.play_word( "fish", 3, -3, DOWN )

    # b.play_word( "dowser",-5,  0, RIGHT, "comp"  )
    # b.play_word( "band",  -5, -3, DOWN,  "Dad F" )
    # b.play_word( "reavow",-3, -5, DOWN,  "comp"  )
    # b.play_word( "jeton", -4, -4, RIGHT, "Dad F" )
    # b.play_word( "xenIc", -1, -3, RIGHT, "comp"  )
    # b.play_word( "muck",   3, -5, DOWN,  "Dad F" )
    # b.play_word( "bandiest",-5,-3,DOWN,  "comp"  )
    # b.play_word( "preload",0, -1, DOWN,  "Dad F" )
    # b.play_word( "quiz",   2, -4, RIGHT, "comp"  )
    # b.play_word( "zas",    5, -4, DOWN,  "Dad F" )
    # b.play_word( "deafly", 0,  5, RIGHT, "comp"  )
    # b.play_word( "phis",   0, -1, RIGHT, "Dad F" )
    # b.play_word( "gox",   -1, -5, DOWN,  "comp"  )
    # b.find_word( "g" )
 
    # b.play_word( "word",    0, 0, RIGHT, "aibot"  )
    # b.play_word( "starves",-5, 1, RIGHT, "comp"   )
    # b.play_word( "lot",    -4,-1, DOWN,  "aibot"  )
    # b.play_word( "emeus",   4,-4, DOWN,  "comp"   )
    # b.play_word( "vis",    -1, 1, DOWN,  "aibot"  )
    # b.play_word( "koine",  -5,-5, DOWN,  "comp"   )
    # b.play_word( "hear",    2,-3, DOWN,  "aibot"  )
    # b.play_word( "axal",    5,-5, DOWN,  "comp"   )
    # b.play_word( "dif",     3, 0, DOWN,  "aibot"  )
    # b.play_word( "objEct", -4, 4, RIGHT, "comp"   )
    # b.play_word( "gee",    -5, 5, RIGHT, "aibot"  )
    # b.play_word( "knap",   -5,-5, RIGHT, "comp"   )
    # b.play_word( "Fiz",     3, 3, RIGHT, "aibot"  )
    # b.play_word( "dex",     3,-4, RIGHT, "comp"   )
    # b.play_word( "oy",     -4, 0, RIGHT, "comp"   )
    # b.find_word( "y" )

    
    # b.play_word( "zAyin",   -4,  0, RIGHT, "comp"  )
    # b.play_word( "mode",    -3, -1, RIGHT, "Dad F" )
    # b.play_word( "mAnager", -3, -1, DOWN,  "comp"  )
    # b.play_word( "kugels",  -5,  3, RIGHT, "Dad F" )
    # b.play_word( "racHises",-3,  5, RIGHT, "comp"  )
    # b.play_word( "qadi",    -1, -3, DOWN,  "Dad F" )
    # b.play_word( "hoaxes",   4,  0, DOWN,  "comp"  )
    # b.play_word( "bawd",    -2, -2, RIGHT, "Dad F" )
    # b.play_word( "rei",      5,  1, DOWN,  "comp"  )
    # b.play_word( "jota",     3, -3, DOWN,  "Dad F" )
    # b.find_word( "lfovei" )

    b.play_word( "hawks",-4, 0,RIGHT,"comp" )
    b.play_word( "taj",  -5,-1,RIGHT,"Dad F")
    b.play_word( "exist",-5,-5,DOWN, "comp" )
    b.play_word( "mis",  -4,-5,DOWN, "Dad F")
    b.play_word( "dare", -5, 1,RIGHT,"comp" )
    b.play_word( "doby", -5, 1,DOWN, "Dad F")
    b.play_word( "lev",  -3, 2,RIGHT,"comp" )
    b.play_word( "os",   -3,-5,DOWN, "Dad F")
    b.play_word( "sparid",0, 0,DOWN, "comp" )
    b.play_word( "dozen", 0,5,RIGHT, "Dad F")
    b.play_word( "requin",0,3,RIGHT, "comp" )
    b.find_word( "fanes", 5,1,DOWN,  "Dad F")
    b.find_word( "elgo" )

if __name__ == "__main__":
    main()