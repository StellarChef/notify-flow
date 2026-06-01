from enum import Enum


class OrderStatus(Enum):
    # OPEN
    ACCEPTED = "przyjete_do_realizacji"
    AWAITING_DELIVERY = "oczekiwanie_na_dostawe"
    IN_PROGRESS = "w_trakcie_kompletowania"
    AWAITING_PAYMENT = "oczekiwanie_na_platnosc"
    READY_TO_SHIP = "gotowe_do_wyslania"

    # CLOSED (COMPLETED)
    SHIPPED = "przesylka_wyslana"

    # CLOSED (NOT COMPLETED)
    CANCELLED = "anulowane"
    REJECTED = "odrzucone"
    RETURNED = "zwrocone"
    COMPLAINED = "reklamowane"


# Statusy które powinny trafić do szwalni
SEND_TO_TAILOR = {
    OrderStatus.ACCEPTED,
    OrderStatus.IN_PROGRESS,
    OrderStatus.READY_TO_SHIP,
}

# Statusy zamkniętych zamówień nic nie robimy
CLOSED = {
    OrderStatus.SHIPPED,
    OrderStatus.CANCELLED,
    OrderStatus.REJECTED,
    OrderStatus.RETURNED,
    OrderStatus.COMPLAINED,
}
