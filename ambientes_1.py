"""
=============================================================
  MÓDULO 1 - CONTROLE DE ACESSO
  Arquivo: ambientes.py
  Descrição: CRUD de ambientes (prédios/shoppings) e seus setores
  Projeto: PROJETOFINAL_4TIERAI_CNAK
=============================================================
"""

import json
import os
import uuid
from datetime import datetime

# ─────────────────────────────────────────
#  CAMINHO DO BANCO DE DADOS JSON
# ─────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQUIVO_JSON = os.path.join(BASE_DIR, "dados", "ambientes.json")


# ─────────────────────────────────────────
#  CONSTANTES
# ─────────────────────────────────────────

TIPOS_AMBIENTE = [
    "shopping",          # prédio principal do shopping
    "estacionamento",    # área de estacionamento
    "corredor",          # corredor interno
    "loja",              # espaço de uma loja específica
    "praça_de_alimentação",
    "banheiro",
    "área_externa",
    "administração",
    "depósito",
]

STATUS_AMBIENTE = ["ativo", "inativo", "em_reforma", "interditado"]

SHOPPINGS_CADASTRADOS = [
    "Shopping Norte",
    "Shopping Sul",
    "Shopping Leste",
    "Shopping Oeste",
]

# Ambientes padrão dos 4 shoppings
AMBIENTES_PADRAO = [
    # ── Shopping Norte ──────────────────
    {"nome": "Shopping Norte — Prédio Principal", "shopping": "Shopping Norte", "tipo": "shopping",
     "andar": "Todos", "capacidade_max": 5000, "area_m2": 45000},
    {"nome": "Shopping Norte — Estacionamento Térreo", "shopping": "Shopping Norte", "tipo": "estacionamento",
     "andar": "Térreo", "capacidade_max": 800, "area_m2": 12000},
    {"nome": "Shopping Norte — Praça de Alimentação", "shopping": "Shopping Norte", "tipo": "praça_de_alimentação",
     "andar": "2º", "capacidade_max": 600, "area_m2": 2500},
    {"nome": "Shopping Norte — Corredor Principal L1", "shopping": "Shopping Norte", "tipo": "corredor",
     "andar": "1º", "capacidade_max": 300, "area_m2": 800},

    # ── Shopping Sul ─────────────────────
    {"nome": "Shopping Sul — Prédio Principal", "shopping": "Shopping Sul", "tipo": "shopping",
     "andar": "Todos", "capacidade_max": 4500, "area_m2": 40000},
    {"nome": "Shopping Sul — Estacionamento Coberto", "shopping": "Shopping Sul", "tipo": "estacionamento",
     "andar": "Subsolo", "capacidade_max": 700, "area_m2": 10500},
    {"nome": "Shopping Sul — Praça de Alimentação", "shopping": "Shopping Sul", "tipo": "praça_de_alimentação",
     "andar": "3º", "capacidade_max": 500, "area_m2": 2000},

    # ── Shopping Leste ───────────────────
    {"nome": "Shopping Leste — Prédio Principal", "shopping": "Shopping Leste", "tipo": "shopping",
     "andar": "Todos", "capacidade_max": 3800, "area_m2": 35000},
    {"nome": "Shopping Leste — Estacionamento Externo", "shopping": "Shopping Leste", "tipo": "estacionamento",
     "andar": "Externo", "capacidade_max": 600, "area_m2": 9000},

    # ── Shopping Oeste ───────────────────
    {"nome": "Shopping Oeste — Prédio Principal", "shopping": "Shopping Oeste", "tipo": "shopping",
     "andar": "Todos", "capacidade_max": 4200, "area_m2": 38000},
    {"nome": "Shopping Oeste — Estacionamento Térreo", "shopping": "Shopping Oeste", "tipo": "estacionamento",
     "andar": "Térreo", "capacidade_max": 650, "area_m2": 9750},
    {"nome": "Shopping Oeste — Área Externa/Lazer", "shopping": "Shopping Oeste", "tipo": "área_externa",
     "andar": "Externo", "capacidade_max": 400, "area_m2": 3000},
]


# ─────────────────────────────────────────
#  FUNÇÕES AUXILIARES
# ─────────────────────────────────────────

def _carregar_dados() -> dict:
    if not os.path.exists(ARQUIVO_JSON):
        return {"metadados": _metadados_inicial(), "ambientes": []}
    with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def _salvar_dados(dados: dict):
    os.makedirs(os.path.dirname(ARQUIVO_JSON), exist_ok=True)
    dados["metadados"]["ultima_atualizacao"] = datetime.now().isoformat()
    dados["metadados"]["total_ambientes"] = len(dados["ambientes"])
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def _metadados_inicial() -> dict:
    return {
        "criado_em": datetime.now().isoformat(),
        "total_ambientes": 0,
        "versao": "1.0",
        "ultima_atualizacao": datetime.now().isoformat(),
    }


def _gerar_id() -> str:
    return uuid.uuid4().hex[:8].upper()


# ─────────────────────────────────────────
#  C R U D
# ─────────────────────────────────────────

def criar_ambiente(
    nome: str,
    shopping: str,
    tipo: str,
    andar: str,
    capacidade_max: int,
    area_m2: float,
    descricao: str = None,
    coordenadas_mapa: dict = None,
) -> dict:
    """
    Cadastra um novo ambiente (setor do shopping).
    coordenadas_mapa: {"x": 0.35, "y": 0.72} — posição relativa no mapa do shopping
                      (usada para plotar o mapa de calor futuramente).
    """
    if tipo not in TIPOS_AMBIENTE:
        raise ValueError(f"Tipo inválido. Opções: {TIPOS_AMBIENTE}")
    if shopping not in SHOPPINGS_CADASTRADOS:
        raise ValueError(f"Shopping inválido. Opções: {SHOPPINGS_CADASTRADOS}")
    if capacidade_max <= 0:
        raise ValueError("Capacidade deve ser maior que zero.")

    dados = _carregar_dados()

    ambiente = {
        "id": _gerar_id(),
        "nome": nome,
        "shopping": shopping,
        "tipo": tipo,
        "andar": andar,
        "capacidade_max": capacidade_max,
        "area_m2": area_m2,
        "descricao": descricao,
        "coordenadas_mapa": coordenadas_mapa or {},   # para o mapa de calor
        "status": "ativo",
        "data_cadastro": datetime.now().isoformat(),
        "ultima_atualizacao": datetime.now().isoformat(),
        "equipamentos_instalados": [],   # preenchido pelo módulo de equipamentos
        "monitoramento": {               # preenchido pelo módulo de monitoramento
            "ocupacao_atual": 0,
            "fluxo_hoje": 0,
            "media_permanencia_min": 0,
            "ultima_leitura": None,
        },
        "lojas": [],   # sub-ambientes (lojas dentro deste setor)
    }

    dados["ambientes"].append(ambiente)
    _salvar_dados(dados)
    print(f"✅ Ambiente '{nome}' cadastrado com ID {ambiente['id']}.")
    return ambiente


def listar_ambientes(
    filtro_shopping: str = None,
    filtro_tipo: str = None,
    filtro_status: str = None,
) -> list:
    """Lista ambientes com filtros opcionais."""
    dados = _carregar_dados()
    ambientes = dados["ambientes"]

    if filtro_shopping:
        ambientes = [a for a in ambientes if a["shopping"] == filtro_shopping]
    if filtro_tipo:
        ambientes = [a for a in ambientes if a["tipo"] == filtro_tipo]
    if filtro_status:
        ambientes = [a for a in ambientes if a["status"] == filtro_status]

    return ambientes


def buscar_ambiente(identificador: str) -> dict | None:
    """Busca por ID ou nome do ambiente."""
    dados = _carregar_dados()
    for a in dados["ambientes"]:
        if a["id"] == identificador.upper() or \
           a["nome"].lower() == identificador.lower():
            return a
    return None


def atualizar_ambiente(id_ambiente: str, **campos) -> dict:
    """Atualiza campos de um ambiente existente."""
    dados = _carregar_dados()
    for i, a in enumerate(dados["ambientes"]):
        if a["id"] == id_ambiente.upper():
            campos_protegidos = {"id", "data_cadastro", "equipamentos_instalados", "monitoramento"}
            for campo, valor in campos.items():
                if campo in campos_protegidos:
                    print(f"⚠️  Campo '{campo}' não pode ser alterado diretamente.")
                    continue
                if campo == "status" and valor not in STATUS_AMBIENTE:
                    raise ValueError(f"Status inválido. Opções: {STATUS_AMBIENTE}")
                if campo == "tipo" and valor not in TIPOS_AMBIENTE:
                    raise ValueError(f"Tipo inválido. Opções: {TIPOS_AMBIENTE}")
                dados["ambientes"][i][campo] = valor
            dados["ambientes"][i]["ultima_atualizacao"] = datetime.now().isoformat()
            _salvar_dados(dados)
            print(f"✅ Ambiente {id_ambiente} atualizado.")
            return dados["ambientes"][i]
    raise ValueError(f"Ambiente '{id_ambiente}' não encontrado.")


def deletar_ambiente(id_ambiente: str) -> bool:
    """Remove um ambiente pelo ID."""
    dados = _carregar_dados()
    antes = len(dados["ambientes"])
    dados["ambientes"] = [a for a in dados["ambientes"] if a["id"] != id_ambiente.upper()]
    if len(dados["ambientes"]) < antes:
        _salvar_dados(dados)
        print(f"🗑️  Ambiente {id_ambiente} removido.")
        return True
    print(f"❌ Ambiente {id_ambiente} não encontrado.")
    return False


def adicionar_loja_ao_ambiente(id_ambiente: str, nome_loja: str, segmento: str, area_m2: float) -> dict:
    """
    Cadastra uma loja dentro de um ambiente (ex: loja dentro do corredor do shopping).
    """
    dados = _carregar_dados()
    for i, a in enumerate(dados["ambientes"]):
        if a["id"] == id_ambiente.upper():
            loja = {
                "id_loja": _gerar_id(),
                "nome": nome_loja,
                "segmento": segmento,    # ex: "moda", "alimentação", "tecnologia"
                "area_m2": area_m2,
                "status": "ativa",
                "data_cadastro": datetime.now().isoformat(),
            }
            dados["ambientes"][i]["lojas"].append(loja)
            _salvar_dados(dados)
            print(f"✅ Loja '{nome_loja}' adicionada ao ambiente {id_ambiente}.")
            return loja
    raise ValueError(f"Ambiente '{id_ambiente}' não encontrado.")


def atualizar_monitoramento(id_ambiente: str, ocupacao: int, fluxo_adicional: int = 0):
    """
    Atualiza dados de monitoramento de um ambiente.
    Chamado pelo Módulo de Monitoramento em tempo real.
    """
    dados = _carregar_dados()
    for i, a in enumerate(dados["ambientes"]):
        if a["id"] == id_ambiente.upper():
            dados["ambientes"][i]["monitoramento"]["ocupacao_atual"] = ocupacao
            dados["ambientes"][i]["monitoramento"]["fluxo_hoje"] += fluxo_adicional
            dados["ambientes"][i]["monitoramento"]["ultima_leitura"] = datetime.now().isoformat()
            _salvar_dados(dados)
            return
    raise ValueError(f"Ambiente '{id_ambiente}' não encontrado.")


def obter_estatisticas_ambientes() -> dict:
    """Resumo estatístico dos ambientes cadastrados."""
    ambientes = listar_ambientes()
    if not ambientes:
        return {}

    stats = {
        "total": len(ambientes),
        "por_shopping": {},
        "por_tipo": {},
        "por_status": {},
        "capacidade_total": sum(a["capacidade_max"] for a in ambientes),
        "area_total_m2": sum(a["area_m2"] for a in ambientes),
    }

    for a in ambientes:
        for campo, chave in [
            ("shopping", "por_shopping"),
            ("tipo", "por_tipo"),
            ("status", "por_status"),
        ]:
            val = a.get(campo, "desconhecido")
            stats[chave][val] = stats[chave].get(val, 0) + 1

    return stats


def inicializar_ambientes_padrao():
    """
    Cria os ambientes padrão dos 4 shoppings se ainda não existirem.
    """
    dados = _carregar_dados()
    existentes = {a["nome"] for a in dados["ambientes"]}
    criados = 0
    for amb in AMBIENTES_PADRAO:
        if amb["nome"] not in existentes:
            criar_ambiente(
                nome=amb["nome"],
                shopping=amb["shopping"],
                tipo=amb["tipo"],
                andar=amb["andar"],
                capacidade_max=amb["capacidade_max"],
                area_m2=amb["area_m2"],
            )
            criados += 1
    if criados:
        print(f"\n✅ {criados} ambientes padrão inicializados.")
    else:
        print("ℹ️  Ambientes padrão já existem.")


# ─────────────────────────────────────────
#  MENU INTERATIVO
# ─────────────────────────────────────────

def menu():
    while True:
        print("\n" + "═" * 50)
        print("   SHOPCONTROL — Gerenciamento de Ambientes")
        print("═" * 50)
        print("  1. Cadastrar ambiente")
        print("  2. Listar ambientes")
        print("  3. Buscar ambiente (ID ou nome)")
        print("  4. Atualizar ambiente")
        print("  5. Deletar ambiente")
        print("  6. Adicionar loja a um ambiente")
        print("  7. Ver estatísticas dos ambientes")
        print("  8. Inicializar ambientes padrão (4 shoppings)")
        print("  0. Sair")
        print("═" * 50)
        opcao = input("  Escolha: ").strip()

        if opcao == "1":
            nome     = input("Nome do ambiente: ")
            print(f"Shoppings: {SHOPPINGS_CADASTRADOS}")
            shopping = input("Shopping: ")
            print(f"Tipos: {TIPOS_AMBIENTE}")
            tipo     = input("Tipo: ")
            andar    = input("Andar (ex: Térreo, 1º, Subsolo): ")
            cap      = int(input("Capacidade máxima (pessoas): "))
            area     = float(input("Área em m²: "))
            try:
                criar_ambiente(nome, shopping, tipo, andar, cap, area)
            except ValueError as e:
                print(f"❌ {e}")

        elif opcao == "2":
            print(f"\nFiltrar por shopping? {SHOPPINGS_CADASTRADOS} (deixe em branco para todos)")
            shop = input("Shopping: ").strip() or None
            ambientes = listar_ambientes(filtro_shopping=shop)
            for a in ambientes:
                ocup = a["monitoramento"]["ocupacao_atual"]
                cap  = a["capacidade_max"]
                pct  = round(ocup / cap * 100) if cap else 0
                print(f"  [{a['id']}] {a['nome']} | {a['tipo']} | {a['status']} | Ocupação: {ocup}/{cap} ({pct}%)")

        elif opcao == "3":
            termo = input("ID ou nome: ")
            a = buscar_ambiente(termo)
            print(json.dumps(a, ensure_ascii=False, indent=2) if a else "❌ Não encontrado.")

        elif opcao == "4":
            id_a  = input("ID do ambiente: ").strip().upper()
            campo = input("Campo a editar: ").strip()
            valor = input("Novo valor: ").strip()
            try:
                atualizar_ambiente(id_a, **{campo: valor})
            except ValueError as e:
                print(f"❌ {e}")

        elif opcao == "5":
            id_a = input("ID do ambiente a deletar: ").strip().upper()
            if input(f"Confirma deletar {id_a}? (s/n): ").lower() == "s":
                deletar_ambiente(id_a)

        elif opcao == "6":
            id_a     = input("ID do ambiente: ").strip().upper()
            nome_l   = input("Nome da loja: ")
            segmento = input("Segmento (moda, alimentação, tecnologia...): ")
            area_l   = float(input("Área da loja em m²: "))
            try:
                adicionar_loja_ao_ambiente(id_a, nome_l, segmento, area_l)
            except ValueError as e:
                print(f"❌ {e}")

        elif opcao == "7":
            stats = obter_estatisticas_ambientes()
            print(json.dumps(stats, ensure_ascii=False, indent=2))

        elif opcao == "8":
            inicializar_ambientes_padrao()

        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
