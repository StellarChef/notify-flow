from abc import ABC, abstractmethod


class Adapter:
    @abstractmethod
    def fetch():
        return

    @abstractmethod
    def parse():
        return


class ShoperAdapter(Adapter):
    def init():
        return
