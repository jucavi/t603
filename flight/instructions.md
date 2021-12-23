#La aplicación permitirá:

    Comprar modificar y cancelar vuelos
    Indicar tiempo estimado de vuelo y hora de llegada en los usos horarios de origen y destino

#Para realizar esta actividad necesitaremos:

    Módulo datetime
    Una clase vuelo (Flight)
    Un JSON para guardar los vuelos comprados
    Un decorador para guardar los vuelos en el JSON

#Clase vuelo:

    origin: str
    destination: str
    departures_hours: list (horarios de partida)
    tiempo de vuelo: float
    ETA: method -> float (Estimated Time of Arrival)

#JSON

    Tendrá un identificador único
    Registrará las propiedades mencionadas en la clase Flight
    Indicar la hora de compra (UTC +/- 0)
