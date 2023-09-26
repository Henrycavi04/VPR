from flask import Flask, render_template, request
import math
from operator import itemgetter

app = Flask(__name__)

@app.route("/")
def principal():
    return render_template("index.html")

@app.route("/resultado")
def resultado():
    # Obtener los valores de los pedidos
    pedido_jilo = int(request.args.get('pedido_jilotepec'))
    pedido_tolu = int(request.args.get('pedido_toluca'))
    pedido_atla = int(request.args.get('pedido_atlacomulco'))
    pedido_guad = int(request.args.get('pedido_guadalajara'))
    pedido_mont = int(request.args.get('pedido_monterrey'))
    pedido_canc = int(request.args.get('pedido_cancun'))
    pedido_more = int(request.args.get('pedido_morelia'))
    pedido_agua = int(request.args.get('pedido_aguascalientes'))
    pedido_quer = int(request.args.get('pedido_queretaro'))
    pedido_cdmx = int(request.args.get('pedido_cdmx'))

    def distancia(coord1, coord2):
        lat1 = coord1[0]
        lon1 = coord1[1]
        lat2 = coord2[0] 
        lon2 = coord2[1]
        return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

    def en_ruta(rutas, c):
        ruta = None
        for r in rutas:
            if c in r:
                ruta = r
        return ruta

    def peso_ruta(ruta):
        total = 0
        for c in ruta:
            total = total + pedidos[c]
        return total
        
    def vrp_voraz():
        #Calcular los ahorros
        s={}
        for c1 in coord:
            for c2 in coord:
                if c1 != c2:
                    if not (c2,c1) in s:
                        d_c1_c2 = distancia(coord[c1], coord[c2])
                        d_c1_almacen = distancia (coord[c1], almacen)
                        d_c2_almacen = distancia (coord[c2], almacen)
                        s[c1,c2] = d_c1_almacen + d_c2_almacen - d_c1_c2
        #Ordenar Ahorros
        s = sorted(s.items(), key = itemgetter(1), reverse = True)

        #Construir rutas
        rutas = []
        for k,v in s:
            rc1 = en_ruta(rutas, k[0])
            rc2 = en_ruta(rutas, k[1])
            if rc1 == None and rc2 ==None:
                #No estan en nunguna ruta. Crear la ruta.
                if peso_ruta([k[0], k[1]]) <= max_carga:
                    rutas.append([k[0], k[1]])
            elif rc1 != None and rc2 == None:
                #Ciudad 1 ya esta en ruta. Agregar la ciudad 2
                if rc1[0] == k[0]:
                    if peso_ruta(rc1) + peso_ruta([k[1]]) <= max_carga:
                        rutas[rutas.index(rc1)].insert(0, k[1])
                elif rc1[len(rc1)-1]== k[0]:
                    if peso_ruta(rc1) + peso_ruta([k[1]]) <= max_carga:
                        rutas[rutas.index(rc1)].append(k[1])
            elif rc1 == None and rc2 != None:
                #Ciudad 2 ya esta en ruta. Agregar la ciudad 1
                if rc2[0] == k[1]:
                    if peso_ruta(rc2) + peso_ruta([k[0]]) <= max_carga:
                        rutas [rutas.index(rc2)].insert(0,k[0])
                elif rc2[len(rc2) - 1] == k[1]:
                    if peso_ruta(rc2) + peso_ruta([k[0]]) <=max_carga:
                        rutas[rutas.index(rc2)].append(k[0])
            elif rc1 != None and rc2 != None and rc1 != rc2:
                #Ciudad 1 y 2 ya estan en una ruta.
                if rc1[0] == k[0] and rc2[len(rc2) -1] == k[1]:
                    if peso_ruta(rc1) + peso_ruta(rc2) <= max_carga:
                        rutas[rutas.index(rc2)].extend(rc1)
                        rutas.remove(rc1)
                elif rc1[len(rc1) -1] == k[0] and rc2 [0] == k[1]:
                    if peso_ruta(rc1) + peso_ruta(rc2) <= max_carga:
                        rutas[rutas.index(rc1)].extend(rc2)
                        
                        rutas.remove(rc2)
        return rutas

    if __name__ == "__main__":
        coord = {
            'Jilotepec': (19.984146, -99.519127),
            'Toluca': (19.286167856525594, -99.65473296644892),
            'Atlacomulco': (19.796802401380955, -99.87643301629244),
            'Guadalajara': (20.655773344775373, -103.35773871581326),
            'Monterrey': (25.675859554333684, -100.31405053526082),
            'Cancún': (21.158135651777727, -86.85092947858692),
            'Morelia': (19.720961251258654, -101.15929186858635),
            'Aguascalientes': (21.88473831747085, -102.29198705069501),
            'Queretaro': (20.57005870003398, -100.45222862892079),
            'CDMX': (19.429550164848152, -99.13000959477478)
        }
        pedidos = {
            'Jilotepec': pedido_jilo,
            'Toluca': pedido_tolu,
            'Atlacomulco': pedido_atla,
            'Guadalajara': pedido_guad,
            'Monterrey': pedido_mont,
            'Cancún': pedido_canc,
            'Morelia': pedido_more,
            'Aguascalientes': pedido_agua,
            'Queretaro': pedido_quer,
            'CDMX': pedido_cdmx
    }
        almacen = (40.23, -3.40)
        max_carga = int(request.args.get('maxcarga'))
        

    # Asegúrate de que `rutas` contiene las rutas calculadas
    rutas = vrp_voraz()
    for ruta in rutas:
            print (ruta)

    # Renderiza la plantilla "resultado.html" con las variables apropiadas
    return render_template("resultado.html", maxcarga=max_carga, rutas=rutas)

if __name__ == '__main__':
    app.run()
