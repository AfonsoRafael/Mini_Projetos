#   SISTEMA DE BIBLIOTECA

from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

class Biblioteca:
    def __init__(self, nome, endereco, telefono):
        self._nome = nome
        self._endereco = endereco
        self._telefone = telefono

    @property
    def nome(self):
        return self._nome
    
    @property
    def endereco(self):
        return self._endereco
    
    @property
    def telefone(self):
        return self._telefone
    
    def registrar_Usuario():
        pass

    def cadastrarLivro():
        pass

    def realizarEmprestimo():
        pass

    def processsarDevolucao():
        pass

    def gerarRelatorio():
        pass