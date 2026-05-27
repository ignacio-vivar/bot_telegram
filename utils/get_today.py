from datetime import datetime


def get_today():
    fecha_actual = datetime.now().date()
    fecha_epoca = datetime(1970, 1, 1).date()
    delta_days = (fecha_actual - fecha_epoca).days

    return delta_days