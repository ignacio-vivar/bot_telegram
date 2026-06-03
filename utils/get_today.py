from datetime import datetime
from zoneinfo import ZoneInfo

ARG_TZ = ZoneInfo("America/Argentina/Buenos_Aires")

def get_today():
    fecha_actual = datetime.now(ARG_TZ).date()
    fecha_epoca = datetime(1970, 1, 1).date()

    return (fecha_actual - fecha_epoca).days