from myPyGPX import *

print("----- Suite de testes unitários a 9 métodos de myPyGPX -----")

# setup: ler um track de um ficheiro GPX
gpx = GPXDocument("FR935-25_04_2018_dois_trksegs_com_waypoints.gpx")
track = gpx.getTrack()

print("\n----- Testando produceXYdata() -----")
myListOfXYpoints = track.produceXYdata()
print("número de pontos =", len(myListOfXYpoints))
print("milésimo ponto:", myListOfXYpoints[999])

print("\n----- Testando _computeSpeedForEachTrackPoint() -----")
track._computeSpeedForEachTrackPoint()
myListOfTrackPoints = track.trackSegList[1].getPointList()
print("speed de um certo ponto:", myListOfTrackPoints[40].getSpeed(), "m/s")

print("\n----- Testando hidePartOfTrack() -----")
#centerPoint colocado na partida, radius = 1300
newTrack = track.hidePartOfTrack(38.649068, -9.244289, 1300)
myListOfTrackPoints = newTrack.trackSegList[1].getPointList()
print("número de pontos no 2º track segment =", len(myListOfTrackPoints))
aPoint = myListOfTrackPoints[10]
print("um certo ponto no 2º track segment: (" + str(aPoint.getLatitude()) + \
      ", " + str(aPoint.getLongitude()) + ")")

print("\n----- Testando totalTime() -----")
print("tempo total =", track.totalTime(), "segundos")

print("\n----- Testando totalDistance() -----")
print("distância total =", track.totalDistance(), "metros")

print("\n----- Testando totalAccumulatedElevation() -----")
print("desnível positivo acumulado =",
      track.totalAccumulatedElevation(), "metros")

print("\n----- Testando averageSpeed() -----")
print("ritmo médio =", track.averageSpeed(), "min/km")
print("velocidade média =",
      track.averageSpeed(expressAs = "speed km/h"), "km/h")

print("\n----- Testando Analyse.secondsToHoursMinSec() -----")
print("0 segundos corresponde a", Analyse.secondsToHoursMinSec(0))
print("1800 segundos corresponde a", Analyse.secondsToHoursMinSec(1800))
print("1872 segundos corresponde a", Analyse.secondsToHoursMinSec(1872))
print("3789 segundos corresponde a", Analyse.secondsToHoursMinSec(3789))
print("309789 segundos corresponde a", Analyse.secondsToHoursMinSec(309789))
print("309789.4 segundos corresponde a", Analyse.secondsToHoursMinSec(309789.4))
print("309789.9 segundos corresponde a", Analyse.secondsToHoursMinSec(309789.9))

print("\n----- Testando Analyse.paceDecimalMinutesToMinSec() -----")
print("ritmo de 4.0 min/km corresponde a",
      Analyse.paceDecimalMinutesToMinSec(4.0))
print("ritmo de 4.5 min/km corresponde a",
      Analyse.paceDecimalMinutesToMinSec(4.5))
print("ritmo de 4.9 min/km corresponde a",
      Analyse.paceDecimalMinutesToMinSec(4.9))
print("ritmo de 4.99 min/km corresponde a",
      Analyse.paceDecimalMinutesToMinSec(4.99))
print("ritmo de 4.994 min/km corresponde a",
      Analyse.paceDecimalMinutesToMinSec(4.994))
print("ritmo de 67.3 min/km corresponde a",
      Analyse.paceDecimalMinutesToMinSec(67.3))
