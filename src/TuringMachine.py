
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
            self.transitions.update( { "q" + str( i ): list( ) } )

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

            self.transitions[ "q" + str(qi) ].append( \
                (   "q" + str(qi),\
                    binascii.unhexlify('%x' % b1),\
                    "q" + str(qr),\
                    binascii.unhexlify('%x' % b2),\
                    self.__mov(mh)\
                ) )
            
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


def main( argv ):
    if len( argv ) > 1 :
        infoFile = ReadFile( argv[1] )
        M = list( infoFile.M )
        if checkBeginAndEnd( M[ 0 : 4 ] ) and checkBeginAndEnd( M[ -4 : ] ):
            MT = TuringMachine( M[ 4 : -4 ] )
            while  True:
                print "#1: Exit"
                print "#2: Enter Sequence"
                n = int(input("#"))

                if n == 1 :
                    sys.exit( 0 )
                if n == 2 :
                    print "--------------------------------------------------"
                    s = raw_input("Sequence: ")
                    tape = list(s)
                    tape.append('_')
                    wIsAccepted( tape, MT )
                    print "--------------------------------------------------"
        else: sys.exit( 0 )
    else : sys.exit( 0 )

def checkBeginAndEnd( section ):
    state = True
    for value in section:
        if value != '1' : 
            state = False
            break
    return state

def wIsAccepted( w, MT ):
    print w
    print MT.alfabetInput

if __name__ == "__main__":
    main( sys.argv )