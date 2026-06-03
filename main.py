"""Ponto de entrada da aplicação para desenvolvimento."""

from app import app  # Importa a app Flask


if __name__ == "__main__":
    app.run(debug=True)  # Inicia servidor de desenvolvimento em debug