"""Aplicación web vulnerable de prueba para integración.

Crea un servidor Flask simple con vulnerabilidades XSS y SQLi
para probar la detección de VulnLab Scanner.
"""

from flask import Flask, request, render_template_string, jsonify
import sqlite3
import os

app = Flask(__name__)

# Configuración
app.config['SECRET_KEY'] = 'secret-key-insecure'

# Inicializar base de datos (por solicitud para evitar problemas de hilos)
def get_db():
    if not hasattr(get_db, "conn"):
        get_db.conn = sqlite3.connect(':memory:', check_same_thread=False)
        cursor = get_db.conn.cursor()
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                password TEXT
            )
        ''')
        cursor.execute('''
            INSERT INTO users (username, password) VALUES 
            ('admin', 'admin123'),
            ('test', 'test123')
        ''')
        get_db.conn.commit()
    return get_db.conn


@app.route('/')
def home():
    return '''
    <h1>Bienvenido a la App Vulnerable de Prueba</h1>
    <p>Usa /search?q= para probar XSS</p>
    <p>Usa /login para probar SQLi</p>
    '''


@app.route('/search')
def search():
    """Endpoint vulnerable a XSS reflejado."""
    query = request.args.get('q', '')
    # Vulnerabilidad: Reflected XSS (sin sanitizar)
    template = f'''
    <html>
        <body>
            <h2>Resultados de búsqueda para: {query}</h2>
            <p>No se encontraron resultados.</p>
        </body>
    </html>
    '''
    return render_template_string(template)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Endpoint vulnerable a SQL Injection."""
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        # Vulnerabilidad: SQL Injection
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(query)
            user = cursor.fetchone()
            
            if user:
                return f"<h2>Login exitoso para: {username}</h2>"
            else:
                return "<h2>Login fallido</h2>"
        except sqlite3.OperationalError as e:
            # La query malformada causará un error SQL
            return f"<h2>Error en la base de datos: {str(e)}</h2>", 500
    
    return '''
    <html>
        <body>
            <form method="post">
                Usuario: <input type="text" name="username"><br>
                Contraseña: <input type="password" name="password"><br>
                <input type="submit" value="Login">
            </form>
        </body>
    </html>
    '''


@app.route('/api/headers')
def check_headers():
    """Endpoint para verificar headers."""
    return jsonify({"message": "Test endpoint"})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050, debug=True)
