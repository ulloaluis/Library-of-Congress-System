# Library-of-Congress-System
Interactive program for learning how to sort books based on call numbers from the LC system

Python 3+ (2 not supported)

From the class docstring:

    Library of Congress System for sorting books.

    This class represents a call ID for a book sorted under the Library of
    Congress System.
    
    Intended Usage (testing): Practice sorting multiple ID's based on the LC system.
    interactive_testing(list of id lists (each id list represents a level))
    
    -runs terminal-based test that allows you to practice sorting with respect
    the LC system
    
    -arguments passed can be either a list of LC lists, or a list of id string lists
    
    Notes:
    
    1. Class numbers do not begin with O, I, W, X, Y. The letter O is removes since
    it conflicts with another naming standard. I, W, X, Y are removed since they
    are not necessary for my purposes, though you may want to add these back in.
    
    2. String representations have a chance of being printed without a '.' separating
    cutter numbers. This is to help practice with book tags that may be formatted that way.
    Randomly Generated class numbers:
    
    3. The number of cutters, number of letters and size of whole number in class number,
    and related factors are all chosen randomly. See the class constants for percentages.
    Specified class numbers:
    
    4. format: LC('XXX0000.frac.cutter.cutter ...')
    
    -Could exclude class num fraction, variable amount of cutters, etc
    
    -Required:
        
        Class Number:
            
            -Must always have a class number
            
            -Starts with at least one letter (capital)
            
            -Has a whole number immediately after (fraction (.2, .131231, etc.) optional)
        
        Cutters (if used, must be formatted this way):
            
            -First character is a '.'
            
            -Second character is a letter
            
            -Rest must be some whole number (but by the LC system, this number is read as a decimal)
    
    Examples: LC('A4.23.B9.C13'), LC('A4'), LC('C3.2'), LC(A1.B235)


Example Terminal Runs:
![Example run](https://github.com/ulloaluis/Library-of-Congress-System/blob/master/images/ex-run.png)

Using stop keyword
![Example run with stop](https://github.com/ulloaluis/Library-of-Congress-System/blob/master/images/ex-run-stop.png)

-Executed with current state of program in library (the command uncommented in if _ _ name _ _ == '_ _ main _ _')


Note:
Design is not the most efficient or the cleanest; I wrote this in a few hours so I could quickly get to studying, so I didn't put too much thought into design (considering I was learning the system as I was writing the program). However, functionality is well-tested, so this program is suitable for testing. If you find any issues, please let me know.
