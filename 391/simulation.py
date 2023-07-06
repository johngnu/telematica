import scipy.stats as ss

def llegadas(Lambda, x):
    # calculo poisson
    P = ss.poisson(Lambda)
    return P

def servicio(Lambda, x):
    # calculo exponencial
    ss.expon.sf(4, loc=0, scale=1)  # 0.018315638888734179
    ss.expon.cdf(1.5, loc=0, scale=1)  # 0.77686983985157021
    return

NA = 0     # No. de clinetestendidos
NNA = 0    # No. de clientes no atendidos
NS = 1     # No. de servidores
T = 600    # minutos (Tiempo de servicio)
L = 20     # cantidad personas max. en la fila
Lambda = 4 # Dist. Poisson para llegadas
Betha = 4  # Dist. Exponencial para sarvicio
S = 0      # Estado del servidor
Wq = 0     # T. promedio de espera en la fila
Lq = 0     # N. promedio de clientes en la fila
TTS = 0    # Tiempo taltal del servicio
TTL = 0    # Tiempo total de llegadas
TT = 0     # Tiempo total
CF = 0     # No. de clientes en la fila

T = llegadas(Lambda)

TT = TT + TTL
if S == 0:
    servicio(Lambda)
    if T > 600:
        print(NA)
        print(NNA)
        print(NS)
        print(T)
        print(L)
        print(Lambda)
        print(Betha)
        print(S)
        print(Wq)
        print(Lq)
        print(TTS)
        print(TTL)
        print(TT)
        print(CF)
    else:
        servicio(Lambda)
else:
    if L < 20:
        CF = CF + 1
    else:
        NNA = NNA + 1







