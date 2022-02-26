#Perhaps I can expose this using xtermjs with the xterm-addon-attach addon.
#https://github.com/xtermjs/xterm.js/tree/master/addons/xterm-addon-attach
import random,sys

max_length = 5

from collections import defaultdict
def test_word( word, rules ):

    if len( word ) != max_length: return False

 
    #letter to contain count
    max_count = defaultdict( lambda: max_length )
    min_count = defaultdict( lambda: 0 )
    not_at = defaultdict( lambda: [] )
    is_at = defaultdict( lambda: None )

    for other_word,rule in rules.items():
        for letter in "abcdefghijklmnopqrstuvwxyz":
            green_count = 0
            yellow_count = 0
            black_count = 0
            for i in range(len(other_word)):
                if other_word[i] == letter:
                    if rule[i] == "g":
                        green_count += 1
                        is_at[i] = letter
                    elif rule[i] == 'y':
                        yellow_count += 1
                        not_at[i].append( letter )
                    elif rule[i] == 'b':
                        black_count += 1
                        not_at[i].append( letter )
                    else:
                        assert( False, "Bad rule" )
            found_min = green_count + yellow_count
            found_max = found_min if black_count > 0 else max_length
            min_count[letter] = max( min_count[letter], found_min )
            max_count[letter] = min( max_count[letter], found_max )

    # max_count = defaultdict( lambda: max_length )
    # min_count = defaultdict( lambda: 0 )
    # not_at = defaultdict( lambda: [] )
    # is_at = defaultdict( lambda: None )

    for letter,max_ in max_count.items():
        if word.count( letter ) > max_: return False

    for letter,min_ in min_count.items():
        if word.count( letter ) < min_: return False

    for i,letter in enumerate(word):
        if letter in not_at[i]: return False
        if i in is_at.keys() and letter != is_at[i]: return False
    return True

def test():
    t = {
    'zymes':'bbbbb',
    'wuxia':'bbbby',
    'vocal':'bybyy',
    'paolo':'bygyb',
    }
    with open( "words.txt", "rt" ) as words:
        for word in words:
            word = word.strip().lower()
            if test_word( word, t ):
                print( word )
                #break

#def main

def main():
    done = False
    rules = {}
    while not done:
        new_word = ""
        while len(new_word) != max_length:
            new_word = input( "\nenter the word you tried: " )

        new_rule = ""

        i = 0
        while i < len(new_word):
            print()
            print( new_word )
            print( " " * i + "^" )
            color = input( f"what color is this {new_word[i]}? ")

            if color.lower() == "green":
                new_rule += "g"
                i += 1
            elif color.lower() in ["gray","black"]:
                new_rule += "b"
                i += 1
            elif color.lower() == "yellow":
                new_rule += "y"
                i += 1
            else:
                print( "\nValid colors are green, yellow or black" )
        

        rules[new_word] = new_rule

        valid_words = []
        with open( "words.txt", "rt" ) as words:
            for word in words:
                word = word.strip().lower()
                if test_word( word, rules ):
                    valid_words.append( word )

        print( f"\nYour rules are currently {rules}")
            
        max_visible = 20
        num_valid = len(valid_words)
        if num_valid > max_visible:
            print( f"\nThere are {num_valid} possible choices.  Here is a random {max_visible} of them." )
            for word in random.sample( valid_words, max_visible ):
                print( word )
        else:
            print( f"\nThere are {num_valid} possible choices.  Here are all of them." )
            for word in valid_words:
                print( word )


def webapp_main():
    import pyxtermjs.app
    sys.argv = [ sys.argv[0], "--command", "python", "--cmd-args",  "wordle.py run" ]
    pyxtermjs.app.main()

#if __name__ == '__main__': main()
if __name__ == '__main__':
    if sys.argv[-1] == "run":
        main()
    else:
        webapp_main()
        
