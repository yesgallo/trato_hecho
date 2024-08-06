try:
    from flask import Flask
    print("Flask importado con éxito")
except ImportError:
    print("Error al importar Flask")