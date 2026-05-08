"""
=============================================================
  SHOPCONTROL — API Flask
  Arquivo: flask_api.py
  Descrição: API que conecta o HTML ao Python/JSON
  
  Como rodar:
    pip install flask flask-cors
    python flask_api.py
  Acesse: http://localhost:5000
=============================================================
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from usuarios                           import (criar_usuario, listar_usuarios,
                                                 buscar_usuario, atualizar_usuario,
                                                 deletar_usuario, obter_estatisticas,
                                                 PERFIS_USUARIO, SHOPPINGS, GENEROS,
                                                 STATUS_USUARIO)
from modulos_sistema                    import (listar_modulos, verificar_acesso,
                                                 inicializar_modulos_padrao,
                                                 PERFIS_COM_ACESSO)
from ambientes                          import (listar_ambientes, criar_ambiente,
                                                 obter_estatisticas_ambientes,
                                                 inicializar_ambientes_padrao,
                                                 TIPOS_AMBIENTE, SHOPPINGS_CADASTRADOS)

app = Flask(__name__, static_folder=".")
CORS(app)  # Permite que o HTML acesse a API

# ─────────────────────────────────────────
#  SERVE O HTML
# ─────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory(".", "index.html")


# ─────────────────────────────────────────
#  ROTAS — USUÁRIOS
# ─────────────────────────────────────────
@app.route("/api/usuarios", methods=["GET"])
def get_usuarios():
    perfil  = request.args.get("perfil")
    status  = request.args.get("status")
    shopping = request.args.get("shopping")
    return jsonify(listar_usuarios(filtro_perfil=perfil, filtro_status=status, filtro_shopping=shopping))


@app.route("/api/usuarios", methods=["POST"])
def post_usuario():
    dados = request.json
    try:
        u = criar_usuario(**dados)
        return jsonify({"sucesso": True, "usuario": u}), 201
    except (ValueError, TypeError) as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 400


@app.route("/api/usuarios/<id_usuario>", methods=["GET"])
def get_usuario(id_usuario):
    u = buscar_usuario(id_usuario)
    if u:
        return jsonify(u)
    return jsonify({"erro": "Não encontrado"}), 404


@app.route("/api/usuarios/<id_usuario>", methods=["PUT"])
def put_usuario(id_usuario):
    try:
        u = atualizar_usuario(id_usuario, **request.json)
        return jsonify({"sucesso": True, "usuario": u})
    except ValueError as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 400


@app.route("/api/usuarios/<id_usuario>", methods=["DELETE"])
def delete_usuario(id_usuario):
    ok = deletar_usuario(id_usuario)
    return jsonify({"sucesso": ok})


@app.route("/api/usuarios/estatisticas", methods=["GET"])
def get_estatisticas():
    return jsonify(obter_estatisticas())


# ─────────────────────────────────────────
#  ROTAS — MÓDULOS
# ─────────────────────────────────────────
@app.route("/api/modulos", methods=["GET"])
def get_modulos():
    return jsonify(listar_modulos())


@app.route("/api/modulos/acesso", methods=["GET"])
def get_acesso():
    codigo = request.args.get("codigo")
    perfil = request.args.get("perfil")
    ok = verificar_acesso(codigo, perfil)
    return jsonify({"acesso": ok, "modulo": codigo, "perfil": perfil})


# ─────────────────────────────────────────
#  ROTAS — AMBIENTES
# ─────────────────────────────────────────
@app.route("/api/ambientes", methods=["GET"])
def get_ambientes():
    shopping = request.args.get("shopping")
    tipo     = request.args.get("tipo")
    return jsonify(listar_ambientes(filtro_shopping=shopping, filtro_tipo=tipo))


@app.route("/api/ambientes", methods=["POST"])
def post_ambiente():
    d = request.json
    try:
        a = criar_ambiente(**d)
        return jsonify({"sucesso": True, "ambiente": a}), 201
    except (ValueError, TypeError) as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 400


@app.route("/api/ambientes/estatisticas", methods=["GET"])
def get_estat_ambientes():
    return jsonify(obter_estatisticas_ambientes())


# ─────────────────────────────────────────
#  ROTAS — CONSTANTES (pro HTML preencher os selects)
# ─────────────────────────────────────────
@app.route("/api/constantes", methods=["GET"])
def get_constantes():
    return jsonify({
        "perfis_usuario":    PERFIS_USUARIO,
        "shoppings":         SHOPPINGS,
        "generos":           GENEROS,
        "status_usuario":    STATUS_USUARIO,
        "tipos_ambiente":    TIPOS_AMBIENTE,
        "shoppings_amb":     SHOPPINGS_CADASTRADOS,
        "perfis_com_acesso": PERFIS_COM_ACESSO,
    })


# ─────────────────────────────────────────
#  INICIALIZAÇÃO
# ─────────────────────────────────────────
@app.route("/api/inicializar", methods=["POST"])
def post_inicializar():
    inicializar_modulos_padrao()
    inicializar_ambientes_padrao()
    return jsonify({"sucesso": True, "mensagem": "Sistema inicializado!"})


if __name__ == "__main__":
    print("\n🚀 ShopControl API rodando em http://localhost:5000")
    print("   Abra o navegador e acesse: http://localhost:5000\n")
    app.run(debug=True, port=5000)
