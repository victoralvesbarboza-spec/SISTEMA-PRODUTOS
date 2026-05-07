from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configuração do Banco de Dados
bd_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Tecnologia@2025',
    'database': 'sistema_produtos'
}

def get_db():
    return mysql.connector.connect(**bd_config)

@app.route('/')
def listar_produtos():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM produtos")
    lista = cursor.fetchall()
    cursor.close()
    conn.close()
    # Usando index.html conforme aparece na sua pasta de templates
    return render_template('index.html', produtos=lista)

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    preco = request.form['preco']
    estoque = request.form['estoque']
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produtos (nome, preco, estoque) VALUES (%s, %s, %s)", (nome, preco, estoque))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('listar_produtos'))

@app.route('/excluir/<int:id>')
def excluir(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id_produto = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('listar_produtos'))

if __name__ == '__main__':
    app.run(debug=True)
