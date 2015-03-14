#!/usr/bin/python

import sys
import traceback
import math
import time
import datetime


class Random(object):
    '''
    Random class
    '''
    @staticmethod
    def randrange(min, max):
        '''
        A pseudo random number generator to replace random.randrange
        
        Works with an inclusive left bound and exclusive right bound.
        E.g. Random.randrange(0, 5) in [0, 1, 2, 3, 4] is always true
        '''
        return min + int(math.fmod(pow(time.clock() + math.pi, 2), 1.0) * (max - min))

    @staticmethod
    def shuffle(items):
        '''
        Method to shuffle a list of items
        '''
        i = len(items)
        while i > 1:
            i -= 1
            j = Random.randrange(0, i)
            items[j], items[i] = items[i], items[j]
        return items



class Suit (object):
    NAMES = { 'd': 'Diamonds',
        'c' : 'Clubs',
        'h' : 'Hearts' ,
        's' : 'Spades' }

    SHIFTS = {
        'd' : 0,
        'c' : 16,
        'h' : 32,
        's' : 48,
    }

    def __init__ (self, s):
        self._suitCode = s

    def __str__ (self):
        return Suit.getSuitName (self._suitCode)

    def getShift (self):
        return Suit.getSuitShift (self._suitCode)

    @staticmethod
    def getSuitName (s):
        return Suit.NAMES [s]

    @staticmethod
    def getSuitShift (s):
        return Suit.SHIFTS [s]

    def __eq__ (self, other):
        print self._suitCode 
        print other._suitCode

        return self._suitCode == other._suitCode

class Height (object):
    NUMBERS = {
        '2' : ('2', 0x0001),
        '3' : ('3', 0x0002),
        '4' : ('4', 0x0004),
        '5' : ('5', 0x0008),
        '6' : ('6', 0x0010),
        '7' : ('7', 0x0020),
        '8' : ('8', 0x0040),
        '9' : ('9', 0x0080),
        'T' : ('10', 0x0100),
        'J' : ('Jack', 0x0200),
        'Q' : ('Queen', 0x0400),
        'K' : ('King', 0x0800),
        'A' : ('Ace', 0x1000)
    }

    def __init__ (self, s):
        self._heightCode = s

    def __str__ (self):
        return Height.getHeightName (self._heightCode)

    def getValue (self):
        return Height.getHeightValue (self._heightCode)

    @staticmethod
    def getHeightName (h):
        return Height.NUMBERS [h][0]

    @staticmethod
    def getHeightValue (h):
        return Height.NUMBERS [h][1]

class Card (object):

    def __init__ (self, cardCode):
        self._height = Height (cardCode[0])
        self._suit = Suit (cardCode[1])
        self._cardCode = cardCode
        self._hexValue = self._height.getValue () << \
            self._suit.getShift ()

    def __str__ (self):
        return str(self._height) + " of " + str( self._suit)

    def getHexValue (self):
#v = self._height.getValue ()
#        return v << self._suit.getShift ()
        return self._hexValue 

    def getCardCode (self):
        return self._cardCode

    def __eq__ (self, other):
        return self._cardCode == other._cardCode


class Hand (object):

    def __init__ (self):
        self._cards = []
        self._hexValue = 0
        self._couples = 'None'
        self._trios = 'None'

    def addCard (self, c):
        self._cards.append (c)
        self._hexValue |= c._hexValue
        self._couples = 'None'
        self._trios = 'None'

    def __str__ (self):
        strValue = ""
        for c in self._cards:
            strValue += str(c) + "\n"

        return strValue

    def getHexValue (self):
        return self._hexValue

    def getNumberOfCards (self):
        return len (self._cards)

    def getCardCode (self):
        code = "["
        first = True
        for c in self._cards:
            if first:
                first = False
            else:
                code += ","
            code +=  c.getCardCode ()
        code+= "]"
        return code

    def parseHand (self, handStr):
        cards = handStr[1:-1].split (",")
        for c in cards:
            self.addCard (Card (c))

    def getCouples (self):
        if self._couples == 'None':
            self._couples = []
            for i in range (0, len(self._cards) -1):
                for j in range (i+1, len (self._cards)):
                    h = Hand ()
                    h.addCard (self._cards [i])
                    h.addCard (self._cards [j])
                    self._couples.append (h)
        return self._couples

    def getTrios (self):
        if self._trios == 'None':
            self._trios = []
            for i in range (0, len(self._cards) - 2):
                for j in range (i+1, len (self._cards) -1):
                    for k in range (j+1, len (self._cards)):
                        h = Hand ()
                        h.addCard (self._cards [i])
                        h.addCard (self._cards [j])
                        h.addCard (self._cards [k])
                        self._trios.append (h)
        return self._trios

    def cardInHand (self, card):
        found = False
        for c in self._cards:
            if c == card:
                found = True
                break
        return found

    def __add__ (self, other):
        H = Hand ()
        for c in self._cards:
            H.addCard (c)
        for c in other._cards:
            H.addCard (c)
        return H

    def clone (self):
        H = Hand ()
        for c in self._cards:
            H.addCard (c)
        return H

class Maze (object):

    def __init__ (self):
        self._cards = []

        for s in Suit.NAMES:
            for h in Height.NUMBERS:
                self._cards.append ( Card (h + s))

    def shuffle (self):
        Random.shuffle (self._cards)
        self._index = 0

    def __str__ (self):
        mazeStr  = ""
        for c in self._cards:
            mazeStr += str(c) + "\n"
        return mazeStr

    def deal (self):
        c = self._cards [self._index]
        self._index += 1
        return c

class Evaluate (object):

    NO_PAIR = 0
    PAIR = 0x01000000
    TWO_PAIR = 0x02000000
    THREE_OF_A_KIND = 0x03000000
    STRAIGHT = 0x04000000
    FLUSH = 0x05000000
    FULL_HOUSE = 0x06000000
    FOUR_OF_A_KIND = 0x07000000
    STRAIGHT_FLUSH = 0x08000000

    COUPLE_PAIR = 0x04000000
    COUPLE_CONSECUTIVE_COLOR = 0x03000000
    COUPLE_COLOR = 0x02000000
    COUPLE_CONSECUTIVE = 0x01000000
    COUPLE_NONE = 0x00000000

    RANK_SHIFT_1 = 4
    RANK_SHIFT_2 = 8
    RANK_SHIFT_3 = 12
    RANK_SHIFT_4 = 16

    STRAIGHTS = [ 0x001F, 0x003E, 0x007C, 0x00F8, 0x01F0, 0x03E0, 
        0x07C0, 0x0F80, 0x1F00]

    ARRAY_SIZE = 0x1FC0 + 1
    ACE_RANK = 14

    noOfRanks = []
    hiRank = []
    hiUpTo5Ranks = []


    @staticmethod
    def initialize ():
        Evaluate.noOfRanks.append (0)
        Evaluate.hiRank.append (0)
        Evaluate.hiUpTo5Ranks.append (0)
        for mask in range (1, Evaluate.ARRAY_SIZE):
            bitCount = 0
            ranks = 0
            shiftReg = mask
            i =  Evaluate.ACE_RANK - 2
            while (i >= 0):
                if ((shiftReg & 0x1000) != 0):
                    bitCount += 1
                    if bitCount < 5:
                        ranks <<= Evaluate.RANK_SHIFT_1
                        ranks += i
                        if bitCount == 1:
                            Evaluate.hiRank.append (i)
                i -= 1
                shiftReg <<= 1
            Evaluate.hiUpTo5Ranks.append(ranks)
            Evaluate.noOfRanks.append (bitCount)


    @staticmethod
    def getNoOfRanks (r):
        if len (Evaluate.noOfRanks) == 0:
            Evaluate.initialize ()

        return Evaluate.noOfRanks [r]

#numBits = 0
#for i in range (0, 13):
#if r & 0x1 == 0x1:
#numBits += 1
#r = r >> 1

#return numBits

    @staticmethod
    def getHighRank (r):
        if len (Evaluate.hiRank) == 0:
            Evaluate.initialize ()
        return Evaluate.hiRank [r]

#maxBit = 0
#        for i in range (0, 13):
#            if r & 0x01 == 0x01:
#                maxBit = i
#            r = r >> 1

#        return maxBit

    @staticmethod
    def getHighUpTo5bits (r):
        if len (Evaluate.hiUpTo5Ranks) == 0:
            Evaluate.initialize ()
        return Evaluate.hiUpTo5Ranks [r]
#ranks = 0
#shifts = 0
#for i in range (0, 13):
#if r & 0x01 == 0x01:
#ranks |= i << (4 * shifts)
#shifts += 1
#
#r = r >> 1
#
#return ranks

    @staticmethod
    def getStraightValue (r):
        v = 0
        if r in Evaluate.STRAIGHTS:
            v = Evaluate.STRAIGHT | \
                       Evaluate.hiRank [r] << Evaluate.RANK_SHIFT_4
        elif r == 0x100F:
            v = Evaluate.STRAIGHT | \
                       Evaluate.hiRank [0x0010] << Evaluate.RANK_SHIFT_4
        return v

    @staticmethod
    def eval5 (hand):
        """ Receives a long number returns strength """
        strength = Evaluate.NO_PAIR
        d = hand & 0x1FFF;
        c = (hand >> 16) & 0x1FFF;
        h = (hand >> 32) & 0x1FFF;
        s = (hand >> 48) & 0x1FFF;

        ranks = d | c | h | s

        noOfRanks = Evaluate.noOfRanks [ranks]
        if noOfRanks == 2:
            if (c & d & h & s == 0):
                i = c ^ d ^ h ^ s
                strength = Evaluate.FULL_HOUSE | \
                           Evaluate.hiRank [i] << Evaluate.RANK_SHIFT_4 | \
                           Evaluate.hiRank [i^ranks] << Evaluate.RANK_SHIFT_3
            else:
                i = c & d
                strength = Evaluate.FOUR_OF_A_KIND | \
                           Evaluate.hiRank [i] << Evaluate.RANK_SHIFT_4 | \
                           Evaluate.hiRank [i^ranks] << Evaluate.RANK_SHIFT_3
            
        elif noOfRanks == 3:
            i = c ^ d ^ h ^ s 
            if (i == ranks):
                i = c & d
                if i == 0:
                    i = c & h
                    if i == 0:
                        i = d & h
                strength = Evaluate.THREE_OF_A_KIND |\
                    Evaluate.hiRank [i] << Evaluate.RANK_SHIFT_4 |\
                    Evaluate.hiUpTo5Ranks [i^ranks] << Evaluate.RANK_SHIFT_2
            else:
                i = c ^ d ^ h ^ s 
                strength = Evaluate.TWO_PAIR |\
                    Evaluate.hiUpTo5Ranks [i^ ranks] << Evaluate.RANK_SHIFT_3 |\
                    Evaluate.hiRank [i] << Evaluate.RANK_SHIFT_2
        elif noOfRanks == 4:
            i = c ^ d ^ h ^ s 
            strength = Evaluate.PAIR |\
                Evaluate.hiRank [ranks ^ i] << Evaluate.RANK_SHIFT_4 |\
                Evaluate.hiUpTo5Ranks [i ] << Evaluate.RANK_SHIFT_1

        else:
            i = Evaluate.getStraightValue (ranks)
            if i == 0:
                i = Evaluate.hiUpTo5Ranks [ranks]

            if c != 0:
                if c != ranks:
                    strength = i # No flush
                    return strength
            else:
                if d != 0:
                    if d != ranks:
                        strength = i # No flush
                        return strength
                else:
                    if h != 0:
                        if h != ranks:
                            strength = i # No flush
                            return strength
            
            # There is a flush
            if i < Evaluate.STRAIGHT:
                strength = Evaluate.FLUSH | i
            else:
                strength = (Evaluate.STRAIGHT_FLUSH - Evaluate.STRAIGHT) + i

        return strength

    @staticmethod
    def eval2Cards (pair):
        strength = Evaluate.COUPLE_NONE
        d = pair & 0x1FFF;
        c = (pair >> 16) & 0x1FFF;
        h = (pair >> 32) & 0x1FFF;
        s = (pair >> 48) & 0x1FFF;

        ranks = d | c | h | s
        noOfRanks = Evaluate.noOfRanks [ranks]
        if noOfRanks == 1:
            strength = Evaluate.COUPLE_PAIR | \
                Evaluate.hiRank[ranks] << Evaluate.RANK_SHIFT_4 
        else:
            noOfZeros = 0
            if d == 0:
                noOfZeros += 1
            if c == 0:
                noOfZeros += 1
            if h == 0:
                noOfZeros += 1
            if s == 0:
                noOfZeros += 1

            sameColor = False
            if noOfZeros == 3:
                sameColor = True

            consecutive = False
            state = 0
            r = ranks
            for i in range (0,13):
                if r & 0x1 == 0x1:
                    if state == 0:
                        state = 1
                    else:
                        consecutive = True
                        break
                else:
                    if state == 1:
                        break;
                r= r >> 1

            strength = Evaluate.hiUpTo5Ranks [ranks] << Evaluate.RANK_SHIFT_3
            if sameColor:
                if consecutive:
                    strength |= Evaluate.COUPLE_CONSECUTIVE_COLOR
                else:
                    strength |= Evaluate.COUPLE_COLOR
            else:
                if consecutive:
                    strength |= Evaluate.COUPLE_CONSECUTIVE
                
        return strength

    @staticmethod
    def eval9cards (hand, table):
        score = Evaluate.NO_PAIR
        C = hand.getCouples ()
        T = table.getTrios ()
        for c in C:
            c_hex = c._hexValue 
            for t in T:
                s = Evaluate.eval5(c_hex | t._hexValue)
                if s > score:
                    score = s
        return score

    @staticmethod 
    def getNextCard (hand, table, maze):
        exitLoop = False
        while not exitLoop:
            C = maze.deal ()
            if not hand.cardInHand (C) and not table.cardInHand (C):
                exitLoop = True
        return C

    @staticmethod
    def calcProbabilities (hand, table, no_of_players, iterations):
        myScore = 'None'
        wins = 0
        M = Maze ()
        
        for i in range (0, iterations):
            M.shuffle ()

            T = table.clone ()

            for j in range (table.getNumberOfCards (), 5):
                T.addCard (Evaluate.getNextCard (hand, table, M))

            if (table.getNumberOfCards () < 5) or (myScore == 'None'):
                myScore = Evaluate.eval9cards (hand, T)

            Iwin = True
            for p in range (0, no_of_players):
                H = Hand ()
                for j in range (0, 4):
                    H.addCard (Evaluate.getNextCard (hand, table, M))

                otherScore = Evaluate.eval9cards (H, T)

#print "I: "+ " 0x%08x " % myScore,
#print " other " + " 0x%08x " % otherScore

                if otherScore > myScore:
                    Iwin = False
                    break

            if Iwin:
                wins += 1
        return (wins * 100) / iterations

        

Evaluate.initialize ()

class BelongTrapezoid (object):
    def __init__ (self, name, x0, x1, x2, x3, y):
        self._name = name
        self._x0 = x0
        self._x1 = x1
        self._x2 = x2
        self._x3 = x3
        self._y = y

    def firstTriangleArea (self):
        area = (self._x1 - self._x0) * self._y / 2.0
        return area

    def rectangleArea (self):
        area = (self._x2 - self._x1) * self._y 
        return area

    def secondTriangleArea (self):
        area = (self._x3 - self._x2) * self._y / 2.0
        return area

    def calculateArea (self):
        # Two triangles and a rectangle
        area = self.firstTriangleArea ()
        area += self.rectangleArea ()
        area += self.secondTriangleArea ()
        return area

    def calculateCentroid (self): 
        # First triangle
        c = (self._x0 + self._x1 + self._x1) * self.firstTriangleArea () / 3.0

        # Rectangle 
        c += (self._x1 + self._x2) * self.rectangleArea () / 2.0

        # Second triangle
        c += (self._x2 + self._x2 + self._x3) * self.secondTriangleArea () / 3.0

        a = self.calculateArea ()

        if a > 0:
            c /= self.calculateArea ()

        return c

    def __str__ (self):
        retVal = self._name
        retVal += " " + str (self._x0)
        retVal += " " + str (self._x1)
        retVal += " " + str (self._x2)
        retVal += " " + str (self._x3)
        retVal += " " + str (self._y)
        return retVal

class FuzzyOperators (object):

    @staticmethod
    def op_and (x1, x2):
        return min (x1, x2);

    @staticmethod
    def op_or (x1, x2):
        return max (x1, x2);

    @staticmethod
    def op_not (x):
        return (1-x);


class FuzzyVar (object):
    def __init__ (self, name):
        self._name = name

    def getName (self):
        return self._name
    
    def setName (self, name):
        self._name = name


class TriangleVar (FuzzyVar):
    def __init__ (self, name, x0, x1, x2):
        FuzzyVar.__init__ (self, name)
        self._x0 = x0
        self._x1 = x1
        self._x2 = x2

    def belong (self, x):
        if self._x0 == self._x1 and x == self._x0:
            value = 1.0
        elif self._x1 == self._x2 and x == self._x1:
            value = 1.0
        elif x < self._x0:
            value = 0.0
        elif x <= self._x1:
            value = (x - self._x0) / (self._x1 - self._x0)
        elif x <= self._x2:
            value = (self._x2 - x) / (self._x2 - self._x1)
        else:
            value = 0.0
        return value

    def getBelongTrapezoid (self, x):
        if x <= self._x0:
            T = None
        elif x <= self._x1:
            y = (x - self._x0)/ (self._x1 - self._x0)
            x2 = self._x2  - (y * (self._x2 - self._x1))
            T = BelongTrapezoid (self._name, 
                    self._x0, x, x2, self._x2, y)
        elif x <= self._x2:
            y = (self._x2 - x)/ (self._x2 - self._x1)
            x2 = y * (self._x1 - self._x0) + self._x0
            T = BelongTrapezoid (self._name, 
                    self._x0, x2, x, self._x2, y)
        else:
            T = None

        return T

    def getBelongTrapezoidY (self, y):
        x1 = y * (self._x1 - self._x0) + self._x0
        x2 = self._x2  - (y * (self._x2 - self._x1))
        T = BelongTrapezoid (self._name, 
                    self._x0, x1, x2, self._x2, y)
        return T


class Trapezoid (FuzzyVar):
    def __init__ (self, name, x0, x1, x2, x3):
        FuzzyVar.__init__ (self, name)
        self._x0 = x0
        self._x1 = x1
        self._x2 = x2
        self._x3 = x3

    def belong (self, x):
        if self._x0 == self._x1 and x == self._x0:
            value = 1.0
        elif self._x1 == self._x2 and x == self._x1:
            value = 1.0
        elif self._x2 == self._x3 and x == self._x2:
            value = 1.0
        elif x <= self._x0:
            value = 0.0
        elif x <= self._x1:
            value = (x - self._x0) / (self._x1 - self._x0)
        elif x <= self._x2:
            value = 1.0
        elif x <= self._x3:
            value = (self._x3 - x) / (self._x3 - self._x2)
        else:
            value = 0.0
        return value

    def getBelongTrapezoid (self, x):
        if x <= self._x0:
            T = None
        elif x <= self._x1:
            y = (x - self._x0)/ (self._x1 - self._x0)
            x2 = self._x3  - (y * (self._x3 - self._x2))
            T = BelongTrapezoid (self._name, 
                    self._x0, x, x2, self._x3, y)
        elif x <= self._x2:
            T = BelongTrapezoid (self._name, 
                    self._x0, self._x1, self._x2, self._x3, 1.0)
        elif x <= self._x3:
            y = (self._x3 - x)/ (self._x3 - self._x2)
            x2 = y * (self._x1 - self._x0) + self._x0
            T = BelongTrapezoid (self._name, 
                    self._x0, x2, x, self._x3, y)
        else:
            T = None

        return T

class inputSet (object):
    def __init__ (self, name):
        " A list of FuzzyVar objects "
        self._input = []
        self._name = name

    def addValue (self, FV):
        self._input.append (FV)

    def getValues (self, val):
        values = {}
        for i in self._input:
            v = i.belong (val)
            values [i.getName()] = v

        return values

class outputSet (object):
    """ If we want a discrete output. """
    def __init__ (self, name, out_range):
        self._output = []
        self._name = name
        self._out_range = out_range
        self._sets = []

    def addValue (self, name, value):
        self._output.append ((name, value))

    def getClosestValue (self, value):
        closestVal = 10000000000.0
        closestName = None

        for o in self._output:
            diff = abs (value - o[1])
            if diff < closestVal:
                closestVal = diff
                closestName = o[0]

        return closestName

    def proccessSets (self):

        index = 0
        for o in self._output:
            if index == 0:
                prevValue = self._out_range[0]
            else:
                prevValue = self._output[index-1][1]

            if index == len (self._output) -1:
                nextValue = self._out_range [1]
            else:
                nextValue = self._output [index+1][1]

            self._sets.append (TriangleVar (o[0], prevValue, o[1], nextValue))

            index += 1

    def getCentroid (self, values_dict):
        R = ResultSet ()
        for key in values_dict:
            for s in self._sets:
                if s.getName () == key:
#print key, values_dict[key]
                    R.addBelongTrapezoid (s.getBelongTrapezoidY (values_dict[key]))
                    break

        return R.getCentroid ()

class ResultSet (object):
    def __init__ (self):
        self._results = []

    def addBelongTrapezoid (self, T):
        if T != None:
            self._results.append (T)

    def getCentroid (self):
        totalArea = 0.0
        centroid = 0.0
        for T in self._results:
            a  = T.calculateArea ()
            c  = T.calculateCentroid ()
            centroid += (a * c)
            totalArea += a

        centroid /= totalArea
        return centroid
            
class GameTypeCalculator:
    def __init__ (self, initial_pot):

        self._initial_pot = initial_pot

        self._CI = inputSet ("Chips")
        self._CI.addValue (Trapezoid ("FEW", 0.0, 0.0,
                    initial_pot * 0.15 , initial_pot * 0.66))
        self._CI.addValue (Trapezoid ("AVERAGE", initial_pot * 0.33, 
            initial_pot * 0.85, initial_pot * 1.15, initial_pot * 1.66))
        self._CI.addValue (Trapezoid ("LOTS", initial_pot * 1.33, 
            initial_pot * 185, initial_pot * 2.0, initial_pot * 2.0))

        self._O = outputSet ("GAME_TYPE", (0.0, 5.0))
        self._O.addValue ("SUICIDAL", 1.0)
        self._O.addValue ("AGGRESIVE", 2.0)
        self._O.addValue ("CAUTIOUS", 3.0)
        self._O.addValue ("CONSERVATIVE", 4.0)
        self._O.proccessSets ()

    def calculateGameType (self, chips):
        ci = self._CI.getValues (chips)

        todo = {}
        val = FuzzyOperators.op_and (ci['FEW'], 
            FuzzyOperators.op_not (ci['AVERAGE']))
        todo ['SUICIDAL'] = val
        val = FuzzyOperators.op_and (ci['FEW'], ci['AVERAGE'])
        todo ['AGGRESIVE'] = val
        todo ['CAUTIOUS'] = ci ['AVERAGE']
        val = FuzzyOperators.op_and (ci['LOTS'], 
            FuzzyOperators.op_not (ci['AVERAGE']))
        todo ['CONSERVATIVE'] = val 
        c = self._O.getCentroid (todo)

        return 2.0, 'AGGRESIVE'
#return c, self._O.getClosestValue (c)

class ActionCalculator (object):
    RAISE_MAX_VALUE  = 5.0
    RAISE_MED_VALUE  = 4.0
    RAISE_MIN_VALUE  = 3.0
    CALL_VALUE = 2.0
    FOLD_VALUE = 1.0

    RAISE_MAX_NAME = "RAISE MAX"
    RAISE_MIN_NAME = "RAISE MIN"
    RAISE_MED_NAME = "RAISE MED"
    CALL_NAME = "CALL"
    FOLD_NAME = "FOLD"

    def __init__ (self):
        self._O = outputSet ("ACTION", (0.0, 6.0))
        self._O.addValue ("FOLD", ActionCalculator.FOLD_VALUE)
        self._O.addValue ("CALL", ActionCalculator.CALL_VALUE)
        self._O.addValue ("RAISE MIN", ActionCalculator.RAISE_MIN_VALUE)
        self._O.addValue ("RAISE MED", ActionCalculator.RAISE_MED_VALUE)
        self._O.addValue ("RAISE MAX", ActionCalculator.RAISE_MAX_VALUE)
        self._O.proccessSets ()

        self._GT = inputSet ("GAME_TYPE")
        self._GT.addValue (TriangleVar ("SUICIDAL", 0.0, 1.0, 2.0))
        self._GT.addValue (TriangleVar ("AGGRESIVE",1.0, 2.0, 3.0))
        self._GT.addValue (TriangleVar ("CAUTIOUS", 2.0, 3.0, 4.0))
        self._GT.addValue (TriangleVar ("CONSERVATIVE", 3.0, 4.0, 5.0))

    def applyRules (self, game_type, hand_prob):
        todo = {}
        gt = self._GT.getValues (game_type)
        hp = self._Hand.getValues (hand_prob)

        Bot.writeMsg ("hand_prob " + str(hand_prob) + ", game_type " + \
                str(game_type))
        Bot.writeMsg ("applyRules " + str(hp))

        todo['RAISE MAX' ] = gt ['SUICIDAL']

        todo['RAISE MAX' ] += FuzzyOperators.op_and (gt['AGGRESIVE'],
                hp ['VERY GOOD'])
        todo['RAISE MED' ] = FuzzyOperators.op_and (gt['AGGRESIVE'],
                hp ['GOOD'])
        todo['CALL' ] = FuzzyOperators.op_and (gt['AGGRESIVE'], 
                hp ['REGULAR'])
        todo['FOLD' ] = FuzzyOperators.op_and (gt['AGGRESIVE'], 
                hp ['BAD'])

        todo['RAISE MED' ] += FuzzyOperators.op_and (gt['CAUTIOUS'],
                hp ['VERY GOOD'])
        todo['RAISE MIN' ] = FuzzyOperators.op_and (gt['CAUTIOUS'],
                hp ['GOOD'])
        todo['CALL' ] += FuzzyOperators.op_and (gt['CAUTIOUS'], 
                hp ['REGULAR'])
        todo['FOLD' ] += FuzzyOperators.op_and (gt['CAUTIOUS'], 
                hp ['BAD'])

        todo['RAISE MIN' ] += FuzzyOperators.op_and (gt['CONSERVATIVE'],
                hp ['VERY GOOD'])
        todo['CALL' ] += FuzzyOperators.op_and (gt['CONSERVATIVE'],
                hp ['GOOD'])
        todo['FOLD' ] += FuzzyOperators.op_and (gt['CONSERVATIVE'], 
                hp ['REGULAR'])
        todo['FOLD' ] += FuzzyOperators.op_and (gt['CONSERVATIVE'], 
                hp ['BAD'])

        c = self._O.getCentroid (todo)
        return c, self._O.getClosestValue (c)

class ActionCalculatorPreFlop (ActionCalculator):
    def __init__ (self):
        ActionCalculator.__init__ (self)
        self._Hand = inputSet ("HAND_PROB")
        self._Hand.addValue (TriangleVar ("VERY GOOD", 98.0, 100.0, 
                    100.0))
        self._Hand.addValue (Trapezoid ("GOOD", 55.0, 60.0, 100.0, 100.0))
        self._Hand.addValue (TriangleVar ("REGULAR", 40.0, 50.0, 60.0))
        self._Hand.addValue (Trapezoid ("BAD", 0.0, 0.0, 30.0, 45.0))

class ActionCalculatorFlop (ActionCalculator):
    def __init__ (self):
        ActionCalculator.__init__ (self)
        self._Hand = inputSet ("HAND_PROB")
        self._Hand.addValue (Trapezoid ("VERY GOOD", 70.0, 80.0, 
                    100.0, 100.0))
        self._Hand.addValue (Trapezoid ("GOOD", 55.0, 60.0, 70.0, 80.0))
        self._Hand.addValue (TriangleVar ("REGULAR", 40.0, 50.0, 60.0))
        self._Hand.addValue (Trapezoid ("BAD", 0.0, 0.0, 30.0, 45.0))
    
class ActionCalculatorTurn (ActionCalculator):
    def __init__ (self):
        ActionCalculator.__init__ (self)
        self._Hand = inputSet ("HAND_PROB")
        self._Hand.addValue (Trapezoid ("VERY GOOD", 75.0, 85.0, 
                    100.0, 100.0))
        self._Hand.addValue (Trapezoid ("GOOD", 60.0, 65.0, 75.0, 85.0))
        self._Hand.addValue (TriangleVar ("REGULAR", 45.0, 55.0, 65.0))
        self._Hand.addValue (Trapezoid ("BAD", 0.0, 0.0, 35.0, 50.0))

class ActionCalculatorRiver (ActionCalculator):
    def __init__ (self):
        ActionCalculator.__init__ (self)
        self._Hand = inputSet ("HAND_PROB")
        self._Hand.addValue (Trapezoid ("VERY GOOD", 75.0, 85.0, 
                    100.0, 100.0))
        self._Hand.addValue (Trapezoid ("GOOD", 60.0, 65.0, 75.0, 85.0))
        self._Hand.addValue (TriangleVar ("REGULAR", 45.0, 55.0, 65.0))
        self._Hand.addValue (Trapezoid ("BAD", 0.0, 0.0, 35.0, 50.0))


class PlayerInfo (object):

    def __init__ (self):
        pass

    def parseLine (self, settings):
        if settings [0] == 'stack':
            self._stack = int (settings[1])
        elif settings[0] == 'post':
            self._post = int (settings[1])
        elif settings[0] == 'hand':
            self._hand = Hand ()
            self._hand.parseHand (settings[1])
            Bot.writeMsg ("Hand " + str(self._hand))

    def getStack (self):
        return self._stack

    def getHand (self):
        return self._hand


class Bot (object):
    ITERATIONS = 200
    def __init__ (self):
        self._ACPF = ActionCalculatorPreFlop ()
        self._ACF = ActionCalculatorFlop ()
        self._ACT = ActionCalculatorTurn ()
        self._ACR = ActionCalculatorRiver ()
        self._GT = None

    @staticmethod
    def writeMsg (msg):
#fp = open ("perro.txt", "a+")
#        fp.write (str(datetime.datetime.now()) + " " + msg + "\n")
#        fp.flush ()
#        fp.close ()
        pass

    def parseSettings (self, settings):   
        if settings[0] == 'timeBank':
            self._timeBank = int (settings[1])
        elif settings[0] == 'timePerMove':
            self._timePerMove = int (settings[1])
        elif settings[0] == 'handsPerLevel':
            self._handsPerLevel = int (settings[1])
        elif settings[0] == 'startingStack':
            self._startingStack = int (settings[1])
            self._GT = GameTypeCalculator (self._startingStack)
        elif settings[0] == 'yourBot':
            self._yourBot = settings[1]
            Bot.writeMsg ("yourBot " +  self._yourBot)


    def parseMatch (self, settings):
        if settings[0] == 'round':
            self._round = int (settings[1])
            self._table = None
            self._preFlop = False
            self._flop = False
            self._turn = False
            self._river = False
        elif settings[0] == 'smallBlind':
            self._smallBlind = int (settings[1])
        elif settings[0] == 'bigBlind':
            self._bigBlind = int (settings[1])
        elif settings[0] == 'onButton':
            self._hasButton = False
            if settings [1] == self._yourBot:
                self._hasButton = True
            Bot.writeMsg ("Has button " +  str(self._hasButton))
        elif settings[0] == 'maxWinPot':
            self._maxWinPot = int (settings[1])
            Bot.writeMsg ("Max win pot " +  str(self._maxWinPot))
        elif settings[0] == 'amountToCall':
            self._ammountToCall = int (settings[1])
            Bot.writeMsg ("Ammount to call " +  str(self._ammountToCall))
        elif settings[0] == 'table':
            self._table = Hand ()
            self._table.parseHand (settings[1])
            Bot.writeMsg ("Table " + str(self._table))

    def doPlay (self, value, name):
        minRaise = self._bigBlind
        maxRaise = self._maxWinPot

        # Limit the ammount to gamble in one hand
        if name != ActionCalculator.RAISE_MAX_NAME and \
           name != ActionCalculator.CALL_NAME and \
           name != ActionCalculator.FOLD_NAME:
           if maxRaise > (10 * minRaise):
               Bot.writeMsg ("Capping to CALL")
               name = ActionCalculator.CALL_NAME
               value = ActionCalculator.CALL_VALUE


        if value > ActionCalculator.RAISE_MIN_VALUE:
            if self._raises == 0:
                self._raises += 1
                r = (maxRaise - minRaise) * \
                    (value - ActionCalculator.RAISE_MIN_VALUE)/ \
                    (ActionCalculator.RAISE_MAX_VALUE - ActionCalculator.RAISE_MIN_VALUE)\
                    + minRaise + self._ammountToCall
                r = int(r)

                sys.stdout.write ("raise " + str(r) + "\n");
            elif self._ammountToCall > 0:
                sys.stdout.write ("call " + str(self._ammountToCall) + "\n");
            else:
                sys.stdout.write ("check 0\n");
        elif name == ActionCalculator.RAISE_MIN_NAME:
            if self._raises == 0:
                self._raises += 1
                r = self._ammountToCall + minRaise
                sys.stdout.write ("raise " + str(r) + "\n");
            elif self._ammountToCall > 0:
                sys.stdout.write ("call " + str(self._ammountToCall) + "\n");
            else:
                sys.stdout.write ("check 0\n");
        elif name == ActionCalculator.CALL_NAME or\
             name == ActionCalculator.FOLD_NAME:
            Bot.writeMsg ("HH CALL or FOLD " + str(value) + " max " + str(maxRaise) + " amount " + str(self._ammountToCall))
            if self._ammountToCall > 0:
                x = (value - ActionCalculator.FOLD_VALUE) * maxRaise /\
                    (ActionCalculator.CALL_VALUE - ActionCalculator.FOLD_VALUE)

                if x >= self._ammountToCall:
                    sys.stdout.write ("call " + str(self._ammountToCall) + "\n");
                else:
                    sys.stdout.write ("fold 0\n");
            else:
                sys.stdout.write ("check 0\n");
        sys.stdout.flush ()

    def doPreFlop (self):
        if not self._preFlop:
            self._preFlop = True
            self._raises = 0
            if self._GT == None:
                self._GT = GameTypeCalculator (self._playerInfo.getStack())
            self._game_type, dummy = self._GT.calculateGameType (self._playerInfo.getStack ())
            self._prob = Evaluate.calcProbabilities (
                    self._playerInfo.getHand(), Hand(), 1, Bot.ITERATIONS)

        Bot.writeMsg ("GT " + str(self._game_type) + " prob " + str(self._prob))
        value, name = self._ACPF.applyRules (self._game_type, float(self._prob))
        self.doPlay (value, name)

    def doFlop (self):
        Bot.writeMsg ("doFlop ")
        if not self._flop:
            self._flop = True
            self._raises = 0
            self._game_type, dummy = self._GT.calculateGameType (self._playerInfo.getStack ())
            self._prob = Evaluate.calcProbabilities (
                    self._playerInfo.getHand(), self._table, 1, Bot.ITERATIONS)

        value, name = self._ACF.applyRules (self._game_type, float(self._prob))
        self.doPlay (value, name)


    def doTurn (self):
        Bot.writeMsg ("doTurn ")
        if not self._turn:
            self._turn = True
            self._raises = 0
            self._game_type, dummy = self._GT.calculateGameType (self._playerInfo.getStack ())
            self._prob = Evaluate.calcProbabilities (
                    self._playerInfo.getHand(), self._table, 1, Bot.ITERATIONS)

        value, name = self._ACT.applyRules (self._game_type, float(self._prob))
        self.doPlay (value, name)


    def doRiver (self):
        Bot.writeMsg ("doRiver ")
        if not self._river:
            self._river = True
            self._raises = 0
            self._game_type, dummy = self._GT.calculateGameType (self._playerInfo.getStack ())
            self._prob = Evaluate.calcProbabilities (
                    self._playerInfo.getHand(), self._table, 1, Bot.ITERATIONS)

        value, name = self._ACR.applyRules (self._game_type, float(self._prob))
        self.doPlay (value, name)

    def doAction (self):
        Bot.writeMsg ("doAction")
        if (self._table == None ):
            self.doPreFlop ()
        elif (self._table.getNumberOfCards () == 3):
            self.doFlop ()
        elif (self._table.getNumberOfCards () == 4):
            self.doTurn ()
        elif (self._table.getNumberOfCards () == 5):
            self.doRiver ()

    def parseAction (self, settings):
        if settings[0] == self._yourBot:
            self._actionTime = int (settings[1])
            Bot.writeMsg ("Player action " +  str(self._actionTime))
            self.doAction ()
            
    def parseYourBot (self, settings):
        self._playerInfo.parseLine (settings)

    def parseOtherBot (self, settings):
        self._otherInfo.parseLine (settings)

    def run (self):
        self._playerInfo = PlayerInfo ()
        self._otherInfo = PlayerInfo ()
        while not sys.stdin.closed:
            try:
                rawline = sys.stdin.readline ()

                if len (rawline) == 0:
                    break

                line = rawline.strip ()
                    
                Bot.writeMsg (line)

                parts = line.split ()

                if parts[0] == 'Settings':
                    self.parseSettings (parts[1:])
                elif parts[0] == 'Match':
                    self.parseMatch (parts[1:])
                elif parts[0] == 'Action':
                    self.parseAction (parts[1:])
                elif parts[0] == self._yourBot:
                    self.parseYourBot (parts[1:])
                else:
                    self.parseOtherBot (parts[1:])

            except EOFError:
                return
            except Exception, e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                Bot.writeMsg ( str(e))
                Bot.writeMsg ( repr(traceback.extract_tb(exc_traceback)) )
                sys.stderr.write (str(e))
                sys.stderr.write ( repr(traceback.extract_tb(exc_traceback)) )
                return  

if __name__ == '__main__':
    B = Bot ()
    B.run ()
