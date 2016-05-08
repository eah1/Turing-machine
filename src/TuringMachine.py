
import sys
import binascii

class ReadFile( ):


    file , M = None, None

    def __init__( self, file ):
        self.file = file
        self.M = self.read( )

    def read( self ):
        with open( self.file, "r" ) as ins:
            array = []
            for line in ins:
                array.append( line )
        return array[0]


class TuringMachine():


    states, alfabetInput, alfabetTape, transitions, init, final, numberStates \
         = list(), [ '0', '1' ], list(), dict(), None, None, None 
    
    def __init__( self, config ):

        self.numberStates = self.__counterZeros( reversed( config ) )
        self.__initVars()
        self.__transition( config[ : - ( self.numberStates + 3 ) ] )

    def __initVars( self ):

        for i in range( 1, self.numberStates + 1):
            self.states.append( "q" + str( i ) )
            self.transitions.update( { "q" + str( i ): dict() } )

        self.init = self.states[ 0 ]
        self.final = self.states[ -1 ]

    def __transition( self, config ):

        while len( config ) != 0 :

            index = 0
 
            qi = self.__counterZeros( config )
            index = qi

            aj = config[ index + 1 : index + 9 ]
            b1 = int( '0b' + ''.join( aj  ), 2 )
            
            index = index + len( config[ index + 1 : index + 9 ] ) + 1

            qr = self.__counterZeros( config[ index + 1 : ] )
            index = index + qr + 1

            ax =  config[ index + 1 : index + 9 ]
            b2 = int( '0b' + ''.join( ax ) , 2 )

            index = index + len(config[ index + 1 : index + 9 ]) + 1
            mh = self.__counterZeros( config[ index + 1 : ] )

            del config[ : index + mh + 3 ]

            if binascii.unhexlify('%x' % b1) is not self.transitions[ "q" + str(qi) ] :
                self.transitions[ "q" + str(qi) ].update( \
                        {   \
                            binascii.unhexlify('%x' % b1) : \
                            ( \
                                "q" + str(qi), \
                                binascii.unhexlify('%x' % b1), \
                                "q" + str(qr), \
                                binascii.unhexlify('%x' % b2), \
                                self.__mov(mh) \
                            ) \
                        } )

            self.alfabetTape.append( binascii.unhexlify('%x' % b1) )
            self.alfabetTape.append( binascii.unhexlify('%x' % b2) )

    def __counterZeros( self, config ):

        counter = 0

        for value in config :
            if value == '0': counter += 1
            else : break

        return counter

    def __mov( self, number ):

        switcher = { 1: "E", 2: "D", 3: "N" }
        return switcher.get(number, "mov")

    def machineTuringPrint( self ):

        for i in self.transitions:
            print "State " + i
            if len( self.transitions[ i ] ) > 0 :
                for x in self.transitions[i]:
                    print "---> " + str( self.transitions[i][x] )
            else: print "{}"


class TravelTap():


    MT, w, stateFinal = None, None, None

    def __init__( self, MT, w ):

        self.MT = MT
        self.w = w

    def travel( self ):

        index, state = 0, self.MT.init
        while index != len( self.w ):

            print "--------------------------------------------------"
            print "Index word " + str( index )
            print "In this case " + state

            if self.w[ index ] in self.MT.transitions[ state ]:

                transition = self.MT.transitions[ state ][ self.w[ index ] ]
                print "The symbol " + transition[1] + " to change " + transition[3] +\
                    " next state " + transition[2]
                self.w[index] = transition[3]
                print "The word modified " + str( self.w )
                index = self.__modificationIndex( transition[4], index )
                print "The mov " + transition[4]
                state = transition[2]
                print "--------------------------------------------------"
            else: break

        self.stateFinal = state

    def isWordAccept( self ):

        if self.stateFinal == self.MT.final: print "Word is accepted"
        else : print "Word is not accepted"

    def __modificationIndex( self, mov, index ):

        if mov == "D": index += 1
        if mov == "E": index -= 1
        return index


def main( argv ):

    if len( argv ) > 1 :

        infoFile = ReadFile( argv[1] )
        M = list( infoFile.M )

        if checkBeginAndEnd( M[ 0 : 4 ] ) and checkBeginAndEnd( M[ -4 : ] ):

            MT = TuringMachine( M[ 4 : -4 ] )

            while  True:

                print "#1: Exit"
                print "#2: Machine Info"
                print "#3: Macine .dot"
                print "#4: Enter Sequence"
                n = int(input("#"))
                checkInput( n, MT )

        else: sys.exit( 0 )
    else : sys.exit( 0 )

def checkBeginAndEnd( section ):

    state = True
    for value in section:
        if value != '1' : 
            state = False
            break
    return state

def checkInput( opt, MT ):

    if opt == 1 : sys.exit( 0 )
    if opt == 2 : opt2( MT )
    if opt == 3 : opt3( MT )
    if opt == 4 : opt4( MT )

def opt2( MT ):

    print ""
    print "List states " + str( MT.states )
    print "List alfabet input " + str ( MT.alfabetInput )
    print "List alfabet tape " + str( list ( set( MT.alfabetTape ) ) )
    print "Transitions "
    MT.machineTuringPrint()
    print "State initial " + str( MT.init ) + " State final " + str( MT.final )
    print ""

def opt3( MT ):
    pass

def opt4( MT ):

    print "--------------------------------------------------"
    print ""
    s = raw_input( "Sequence: " )
    tape = list( s )
    print ""
    tape.append('_')
    Tap = TravelTap( MT, tape )
    Tap.travel()
    print ""
    Tap.isWordAccept()
    print "--------------------------------------------------"
    print ""

if __name__ == "__main__":

    main( sys.argv )