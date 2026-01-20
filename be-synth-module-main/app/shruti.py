from enum import Enum

# Defining Hindustani classical Shrutis as an Enum
class Shruti(Enum):
    S  = 'S'
    r1 = 'r1'
    r2 = 'r2'
    R1 = 'R1'
    R2 = 'R2'
    g1 = 'g1'
    g2 = 'g2'
    G1 = 'G1'
    G2 = 'G2'
    M1 = 'M1'
    M2 = 'M2'
    m1 = 'm1'
    m2 = 'm2'
    P  = 'P'
    d1 = 'd1'
    d2 = 'd2'
    D1 = 'D1'
    D2 = 'D2'
    n1 = 'n1'
    n2 = 'n2'
    N1 = 'N1'
    N2 = 'N2'


# value that is to be multiplied to get next microtone(shruti)
freq_multipliers = {
    Shruti.S : 1,            
    Shruti.r1: 256 / 243,
    Shruti.r2: 16 / 15,
    Shruti.R1: 10 / 9,   
    Shruti.R2: 9 / 8,   
    Shruti.g1: 32 / 27,
    Shruti.g2: 6 / 5,   
    Shruti.G1: 5 / 4,
    Shruti.G2: 81 / 64,   
    Shruti.M1: 4 / 3,   
    Shruti.M2: 27 / 20,   
    Shruti.m1: 45 / 32,   
    Shruti.m2: 729 / 512, 
    Shruti.P : 3 / 2,         
    Shruti.d1: 128 / 81,   
    Shruti.d2: 8 / 5,   
    Shruti.D1: 5 / 3,
    Shruti.D2: 27 / 16, 
    Shruti.n1: 16 / 9,   
    Shruti.n2: 9 / 5,    
    Shruti.N1: 15 / 8,
    Shruti.N2: 243 / 128
}


sequence_tuple = (
    Shruti.S, 
    Shruti.r1, Shruti.r2,
    Shruti.R1, Shruti.R2,   
    Shruti.g1, Shruti.g2,   
    Shruti.G1, Shruti.G2,   
    Shruti.M1, Shruti.M2,   
    Shruti.m1, Shruti.m2, 
    Shruti.P,         
    Shruti.d1, Shruti.d2,   
    Shruti.D1, Shruti.D2, 
    Shruti.n1, Shruti.n2,    
    Shruti.N1, Shruti.N2
)


def get_pair_tuple(s: Shruti):
    pair_tuples = (
        (Shruti.S, ), 
        (Shruti.r1, Shruti.r2),
        (Shruti.R1, Shruti.R2),   
        (Shruti.g1, Shruti.g2),   
        (Shruti.G1, Shruti.G2),   
        (Shruti.M1, Shruti.M2),   
        (Shruti.m1, Shruti.m2), 
        (Shruti.P, ),         
        (Shruti.d1, Shruti.d2),   
        (Shruti.D1, Shruti.D2), 
        (Shruti.n1, Shruti.n2),    
        (Shruti.N1, Shruti.N2)
    )
    
    for pair in pair_tuples:
        if s in pair:
            return pair


default_shrutis = (
    Shruti.S, 
    Shruti.r2, Shruti.R1, 
    Shruti.g2, Shruti.G1, 
    Shruti.M1, Shruti.m1, 
    Shruti.P, 
    Shruti.d2, Shruti.D1, 
    Shruti.n2, Shruti.N1
)


# Shruti details including name and corresponding Swara
names = {
    Shruti.S  : {'shruti': None, 'swara': 'Shadja'},
    Shruti.r1 : {'shruti': 'Atikomal', 'swara': 'Rishabh'},
    Shruti.r2 : {'shruti': 'Komal', 'swara': 'Rishabh'},
    Shruti.R1 : {'shruti': 'Shuddha', 'swara': 'Rishabh'},
    Shruti.R2 : {'shruti': 'Teevra', 'swara': 'Rishabh'},
    Shruti.g1 : {'shruti': 'Atikomal', 'swara': 'Gandhar'},
    Shruti.g2 : {'shruti': 'Komal', 'swara': 'Gandhar'},
    Shruti.G1 : {'shruti': 'Shuddha', 'swara': 'Gandhar'},
    Shruti.G2 : {'shruti': 'Teevra', 'swara': 'Gandhar'},
    Shruti.M1 : {'shruti': 'Shuddha', 'swara': 'Madhyam'},
    Shruti.M2 : {'shruti': 'Ekashruti', 'swara': 'Madhyam'},
    Shruti.m1 : {'shruti': 'Teevra', 'swara': 'Madhyam'},
    Shruti.m2 : {'shruti': 'Teevratama', 'swara': 'Madhyam'},
    Shruti.P  : {'shruti': None, 'swara': 'Pancham'},
    Shruti.d1 : {'shruti': 'Atikomal', 'swara': 'Dhaivat'},
    Shruti.d2 : {'shruti': 'Komal', 'swara': 'Dhaivat'},
    Shruti.D1 : {'shruti': 'Shuddha', 'swara': 'Dhaivat'},
    Shruti.D2 : {'shruti': 'Teevra', 'swara': 'Dhaivat'},
    Shruti.n1 : {'shruti': 'Atikomal', 'swara': 'Nishad'},
    Shruti.n2 : {'shruti': 'Komal', 'swara': 'Nishad'},
    Shruti.N1 : {'shruti': 'Shuddha', 'swara': 'Nishad'},
    Shruti.N2 : {'shruti': 'Teevra', 'swara': 'Nishad'}
}