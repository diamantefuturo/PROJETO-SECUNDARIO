"""
=============================================================
  SHOPCONTROL — Interface Streamlit
  Arquivo: streamlit_app.py
  Descrição: Interface web do Módulo 1 usando Streamlit
  
  Como rodar:
    pip install streamlit
    streamlit run streamlit_app.py
=============================================================
"""

import streamlit as st
import json
import os
import sys

# ── Garante que o Python encontra os módulos ────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from usuarios                           import (criar_usuario, listar_usuarios,
                                                 buscar_usuario, atualizar_usuario,
                                                 deletar_usuario, obter_estatisticas,
                                                 PERFIS_USUARIO, FAIXAS_ETARIAS,
                                                 STATUS_USUARIO, SHOPPINGS, GENEROS)
from modulos_sistema                    import (listar_modulos, buscar_modulo,
                                                 verificar_acesso, criar_modulo,
                                                 inicializar_modulos_padrao,
                                                 PERFIS_COM_ACESSO, STATUS_MODULO)
from ambientes                          import (listar_ambientes, buscar_ambiente,
                                                 criar_ambiente, atualizar_ambiente,
                                                 obter_estatisticas_ambientes,
                                                 inicializar_ambientes_padrao,
                                                 TIPOS_AMBIENTE, STATUS_AMBIENTE,
                                                 SHOPPINGS_CADASTRADOS)

# ─────────────────────────────────────────
#  CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────
st.set_page_config(
    page_title="ShopControl — Módulo 1",
    page_icon="🏬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS customizado ─────────────────────────────────────────
st.markdown("""
<style>
    /* Fundo e cores gerais */
    .stApp { background-color: #0f1117; }
    section[data-testid="stSidebar"] { background-color: #1a1d27; border-right: 1px solid #2d3148; }

    /* Cards de métrica */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #1e2235, #252840);
        border: 1px solid #3d4166;
        border-radius: 12px;
        padding: 16px;
    }

    /* Títulos */
    h1, h2, h3 { color: #e8eaf6; }

    /* Badges coloridos */
    .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    .badge-ativo    { background: #1b4332; color: #52b788; }
    .badge-inativo  { background: #3d1a1a; color: #e07a7a; }
    .badge-bloqueado{ background: #4a2800; color: #f4a261; }
    .badge-pendente { background: #1a2e4a; color: #74b9ff; }

    /* Botão primário */
    .stButton > button {
        background: linear-gradient(135deg, #4361ee, #3a0ca3);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
    }
    .stButton > button:hover { opacity: 0.85; }

    /* Tabelas */
    .stDataFrame { border-radius: 10px; overflow: hidden; }

    /* Alertas */
    .success-box {
        background: #1b4332; border-left: 4px solid #52b788;
        padding: 12px 16px; border-radius: 6px; margin: 8px 0;
    }
    .error-box {
        background: #3d1a1a; border-left: 4px solid #e07a7a;
        padding: 12px 16px; border-radius: 6px; margin: 8px 0;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
#  SIDEBAR — NAVEGAÇÃO
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏬 ShopControl")
    st.markdown("**Módulo 1 — Controle de Acesso**")
    st.divider()

    pagina = st.radio(
        "Navegação",
        options=[
            "📊 Dashboard Geral",
            "👥 Usuários",
            "📦 Módulos do Sistema",
            "🏢 Ambientes",
            "⚙️ Inicializar Sistema",
        ],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("ShopControl v1.0 — SENAC")
    st.caption("Técnico em Inteligência Artificial")


# ─────────────────────────────────────────
#  PÁGINA: DASHBOARD GERAL
# ─────────────────────────────────────────
if pagina == "📊 Dashboard Geral":
    st.title("📊 Dashboard Geral — Módulo 1")
    st.caption("Visão geral do Controle de Acesso dos 4 Shoppings")
    st.divider()

    stats_u = obter_estatisticas()
    stats_a = obter_estatisticas_ambientes()
    modulos  = listar_modulos()

    # ── Métricas principais ─────────────────
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👥 Total Usuários",   stats_u.get("total", 0))
    col2.metric("✅ Usuários Ativos",  stats_u.get("por_status", {}).get("ativo", 0))
    col3.metric("🏢 Ambientes",        stats_a.get("total", 0))
    col4.metric("📦 Módulos Ativos",   sum(1 for m in modulos if m["status"] == "ativo"))

    st.divider()
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("👥 Usuários por Perfil")
        por_perfil = stats_u.get("por_perfil", {})
        if por_perfil:
            st.bar_chart(por_perfil)
        else:
            st.info("Nenhum usuário cadastrado.")

        st.subheader("📅 Usuários por Faixa Etária")
        por_faixa = stats_u.get("por_faixa_etaria", {})
        if por_faixa:
            st.bar_chart(por_faixa)

    with col_b:
        st.subheader("🏬 Usuários por Shopping")
        por_shop = stats_u.get("por_shopping", {})
        if por_shop:
            st.bar_chart(por_shop)

        st.subheader("🏢 Ambientes por Shopping")
        por_shop_a = stats_a.get("por_shopping", {})
        if por_shop_a:
            st.bar_chart(por_shop_a)

    st.divider()
    st.subheader("📦 Módulos do Sistema")
    for m in modulos:
        cor = "🟢" if m["status"] == "ativo" else "🔴"
        st.markdown(f"{cor} **{m['icone']} {m['nome']}** — `{m['codigo']}` — perfis: {', '.join(m['perfis_autorizados'])}")


# ─────────────────────────────────────────
#  PÁGINA: USUÁRIOS
# ─────────────────────────────────────────
elif pagina == "👥 Usuários":
    st.title("👥 Gerenciamento de Usuários")
    st.divider()

    aba = st.tabs(["📋 Lista", "➕ Cadastrar", "🔍 Buscar / Editar"])

    # ── ABA: Lista ───────────────────────────
    with aba[0]:
        st.subheader("Todos os Usuários Cadastrados")

        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            f_perfil  = st.selectbox("Filtrar por Perfil",  ["Todos"] + PERFIS_USUARIO)
        with col_f2:
            f_status  = st.selectbox("Filtrar por Status",  ["Todos"] + STATUS_USUARIO)
        with col_f3:
            f_shop    = st.selectbox("Filtrar por Shopping", ["Todos"] + SHOPPINGS)

        usuarios = listar_usuarios(
            filtro_perfil   = None if f_perfil == "Todos" else f_perfil,
            filtro_status   = None if f_status == "Todos" else f_status,
            filtro_shopping = None if f_shop   == "Todos" else f_shop,
        )

        if not usuarios:
            st.warning("Nenhum usuário encontrado com esses filtros.")
        else:
            st.caption(f"Exibindo {len(usuarios)} usuário(s)")
            for u in usuarios:
                with st.expander(f"**{u['nome']}** | {u['perfil']} | {u['faixa_etaria']} | {u['shopping_principal']}"):
                    c1, c2, c3 = st.columns(3)
                    c1.write(f"**ID:** `{u['id']}`")
                    c1.write(f"**CPF:** {u['cpf']}")
                    c1.write(f"**E-mail:** {u['email']}")
                    c2.write(f"**Perfil:** {u['perfil']}")
                    c2.write(f"**Idade:** {u['idade']} anos ({u['faixa_etaria']})")
                    c2.write(f"**Gênero:** {u['genero']}")
                    c3.write(f"**Shopping:** {u['shopping_principal']}")
                    c3.write(f"**Status:** {u['status']}")
                    c3.write(f"**Loja:** {u.get('loja') or '—'}")
                    if u.get("observacoes"):
                        st.caption(f"📝 {u['observacoes']}")

    # ── ABA: Cadastrar ───────────────────────
    with aba[1]:
        st.subheader("Cadastrar Novo Usuário")
        with st.form("form_cadastro"):
            c1, c2 = st.columns(2)
            nome     = c1.text_input("Nome Completo *")
            cpf      = c2.text_input("CPF (só números) *")
            email    = c1.text_input("E-mail *")
            senha    = c2.text_input("Senha *", type="password")
            perfil   = c1.selectbox("Perfil *", PERFIS_USUARIO)
            genero   = c2.selectbox("Gênero *", GENEROS)
            idade    = c1.number_input("Idade *", min_value=1, max_value=110, value=25)
            shopping = c2.selectbox("Shopping Principal *", SHOPPINGS)
            loja     = c1.text_input("Loja (se funcionário/dono)")
            telefone = c2.text_input("Telefone")
            obs      = st.text_area("Observações")

            enviado = st.form_submit_button("💾 Cadastrar Usuário", use_container_width=True)

        if enviado:
            if not all([nome, cpf, email, senha]):
                st.error("Preencha todos os campos obrigatórios (*)")
            else:
                try:
                    u = criar_usuario(
                        nome=nome, cpf=cpf, email=email, senha=senha,
                        perfil=perfil, idade=int(idade), genero=genero,
                        shopping_principal=shopping,
                        loja=loja or None, telefone=telefone or None,
                        observacoes=obs or None,
                    )
                    st.success(f"✅ Usuário **{nome}** cadastrado! ID: `{u['id']}`")
                except ValueError as e:
                    st.error(f"❌ {e}")

    # ── ABA: Buscar / Editar ─────────────────
    with aba[2]:
        st.subheader("Buscar Usuário")
        termo = st.text_input("Digite ID, CPF ou e-mail")
        if termo:
            u = buscar_usuario(termo)
            if u:
                st.success(f"✅ Encontrado: **{u['nome']}** | ID: `{u['id']}`")
                with st.expander("Ver dados completos (JSON)"):
                    st.json(u)

                st.subheader("Editar Status")
                novo_status = st.selectbox("Novo status", STATUS_USUARIO, index=STATUS_USUARIO.index(u["status"]))
                if st.button("💾 Salvar Status"):
                    try:
                        atualizar_usuario(u["id"], status=novo_status)
                        st.success("Status atualizado!")
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))

                st.subheader("⚠️ Zona de Perigo")
                if st.button("🗑️ Deletar este usuário", type="secondary"):
                    deletar_usuario(u["id"])
                    st.success("Usuário deletado.")
                    st.rerun()
            else:
                st.warning("Nenhum usuário encontrado.")


# ─────────────────────────────────────────
#  PÁGINA: MÓDULOS DO SISTEMA
# ─────────────────────────────────────────
elif pagina == "📦 Módulos do Sistema":
    st.title("📦 Módulos do Sistema")
    st.divider()

    aba = st.tabs(["📋 Lista", "🔐 Verificar Acesso", "➕ Criar Módulo"])

    with aba[0]:
        modulos = listar_modulos()
        if not modulos:
            st.warning("Nenhum módulo cadastrado. Use a aba Inicializar.")
        for m in modulos:
            cor = "🟢" if m["status"] == "ativo" else ("🟡" if m["status"] == "em_manutencao" else "🔴")
            with st.expander(f"{cor} {m['icone']} **{m['nome']}** — `{m['codigo']}`"):
                c1, c2 = st.columns(2)
                c1.write(f"**ID:** `{m['id']}`")
                c1.write(f"**Status:** {m['status']}")
                c1.write(f"**Versão:** {m['versao_modulo']}")
                c2.write(f"**Descrição:** {m['descricao']}")
                c2.write(f"**Perfis autorizados:** {', '.join(m['perfis_autorizados'])}")

    with aba[1]:
        st.subheader("🔐 Verificar Acesso")
        st.caption("Simule se um perfil de usuário tem acesso a um módulo")
        modulos = listar_modulos()
        codigos = [m["codigo"] for m in modulos]
        col1, col2 = st.columns(2)
        cod    = col1.selectbox("Módulo", codigos)
        perfil = col2.selectbox("Perfil do usuário", PERFIS_COM_ACESSO)
        if st.button("🔍 Verificar"):
            ok = verificar_acesso(cod, perfil)
            if ok:
                st.success(f"✅ Perfil **{perfil}** tem ACESSO ao módulo **{cod}**")
            else:
                st.error(f"❌ Perfil **{perfil}** NÃO tem acesso ao módulo **{cod}**")

    with aba[2]:
        st.subheader("➕ Criar Novo Módulo")
        with st.form("form_modulo"):
            nome_m  = st.text_input("Nome do módulo *")
            codigo_m = st.text_input("Código único (ex: MOD_MAPA) *")
            desc_m  = st.text_area("Descrição *")
            perfis_m = st.multiselect("Perfis autorizados *", PERFIS_COM_ACESSO)
            icone_m  = st.text_input("Ícone (emoji)", value="📦")
            enviar_m = st.form_submit_button("💾 Criar Módulo", use_container_width=True)
        if enviar_m:
            try:
                criar_modulo(nome_m, codigo_m, desc_m, perfis_m, icone_m)
                st.success(f"✅ Módulo **{nome_m}** criado!")
            except ValueError as e:
                st.error(f"❌ {e}")


# ─────────────────────────────────────────
#  PÁGINA: AMBIENTES
# ─────────────────────────────────────────
elif pagina == "🏢 Ambientes":
    st.title("🏢 Gerenciamento de Ambientes")
    st.divider()

    aba = st.tabs(["📋 Lista", "➕ Cadastrar Ambiente", "📊 Estatísticas"])

    with aba[0]:
        col_f1, col_f2 = st.columns(2)
        f_shop_a = col_f1.selectbox("Filtrar por Shopping", ["Todos"] + SHOPPINGS_CADASTRADOS)
        f_tipo_a = col_f2.selectbox("Filtrar por Tipo",     ["Todos"] + TIPOS_AMBIENTE)

        ambientes = listar_ambientes(
            filtro_shopping = None if f_shop_a == "Todos" else f_shop_a,
            filtro_tipo     = None if f_tipo_a == "Todos" else f_tipo_a,
        )
        st.caption(f"Exibindo {len(ambientes)} ambiente(s)")
        for a in ambientes:
            ocup = a["monitoramento"]["ocupacao_atual"]
            cap  = a["capacidade_max"]
            pct  = round(ocup / cap * 100) if cap else 0
            with st.expander(f"🏢 **{a['nome']}** | {a['tipo']} | {a['status']}"):
                c1, c2, c3 = st.columns(3)
                c1.write(f"**ID:** `{a['id']}`")
                c1.write(f"**Shopping:** {a['shopping']}")
                c1.write(f"**Tipo:** {a['tipo']}")
                c2.write(f"**Andar:** {a['andar']}")
                c2.write(f"**Área:** {a['area_m2']} m²")
                c2.write(f"**Capacidade:** {cap} pessoas")
                c3.write(f"**Ocupação atual:** {ocup} ({pct}%)")
                c3.write(f"**Fluxo hoje:** {a['monitoramento']['fluxo_hoje']}")
                if a.get("lojas"):
                    st.write(f"**Lojas:** {', '.join(l['nome'] for l in a['lojas'])}")

    with aba[1]:
        st.subheader("Cadastrar Novo Ambiente")
        with st.form("form_ambiente"):
            c1, c2 = st.columns(2)
            nome_a    = c1.text_input("Nome do ambiente *")
            shopping_a = c2.selectbox("Shopping *", SHOPPINGS_CADASTRADOS)
            tipo_a    = c1.selectbox("Tipo *", TIPOS_AMBIENTE)
            andar_a   = c2.text_input("Andar (ex: Térreo, 1º) *")
            cap_a     = c1.number_input("Capacidade máxima (pessoas) *", min_value=1, value=100)
            area_a    = c2.number_input("Área em m² *", min_value=1.0, value=500.0)
            desc_a    = st.text_area("Descrição (opcional)")
            enviar_a  = st.form_submit_button("💾 Cadastrar Ambiente", use_container_width=True)
        if enviar_a:
            try:
                amb = criar_ambiente(nome_a, shopping_a, tipo_a, andar_a, int(cap_a), float(area_a), desc_a or None)
                st.success(f"✅ Ambiente **{nome_a}** cadastrado! ID: `{amb['id']}`")
            except ValueError as e:
                st.error(f"❌ {e}")

    with aba[2]:
        stats_a = obter_estatisticas_ambientes()
        if stats_a:
            c1, c2, c3 = st.columns(3)
            c1.metric("Total de Ambientes",   stats_a["total"])
            c2.metric("Capacidade Total",     f"{stats_a['capacidade_total']:,} pessoas")
            c3.metric("Área Total",           f"{stats_a['area_total_m2']:,.0f} m²")
            st.divider()
            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("Por Shopping")
                st.bar_chart(stats_a["por_shopping"])
            with col_b:
                st.subheader("Por Tipo")
                st.bar_chart(stats_a["por_tipo"])
        else:
            st.warning("Nenhum ambiente cadastrado ainda.")


# ─────────────────────────────────────────
#  PÁGINA: INICIALIZAR SISTEMA
# ─────────────────────────────────────────
elif pagina == "⚙️ Inicializar Sistema":
    st.title("⚙️ Inicializar Sistema")
    st.warning("⚠️ Use estas opções apenas na primeira execução ou para resetar o banco de dados.")
    st.divider()

    st.subheader("1. Inicializar Módulos Padrão")
    st.caption("Cria os 8 módulos do sistema (MOD_ACESSO, MOD_EQUIP, MOD_MONITOR...)")
    if st.button("📦 Criar Módulos Padrão"):
        try:
            inicializar_modulos_padrao()
            st.success("✅ Módulos criados!")
        except Exception as e:
            st.error(str(e))

    st.divider()
    st.subheader("2. Inicializar Ambientes Padrão")
    st.caption("Cria os 12 setores dos 4 shoppings")
    if st.button("🏢 Criar Ambientes Padrão"):
        try:
            inicializar_ambientes_padrao()
            st.success("✅ Ambientes criados!")
        except Exception as e:
            st.error(str(e))

    st.divider()
    st.subheader("📁 Status dos Arquivos JSON")
    dados_dir = os.path.join(os.path.dirname(__file__), "dados")
    for arquivo in ["usuarios.json", "modulos_sistema.json", "ambientes.json"]:
        caminho = os.path.join(dados_dir, arquivo)
        if os.path.exists(caminho):
            with open(caminho, encoding="utf-8") as f:
                dados = json.load(f)
            total = list(dados.values())[1]
            st.success(f"✅ `{arquivo}` — {len(total) if isinstance(total, list) else '?'} registros")
        else:
            st.error(f"❌ `{arquivo}` — não encontrado")
