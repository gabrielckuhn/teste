import streamlit as st
from config import credentials_configured, ADDON_PUBLIC_URL
from core.iptv_client import IPTVClient, IPTVError
from core.channel_manager import normalize_live, group_items

st.set_page_config(page_title="IPTV → Stremio", page_icon="📺", layout="wide")

st.title("📺 IPTV → Stremio")
st.caption("Painel de diagnóstico e organização da sua fonte IPTV autorizada.")

if not credentials_configured():
    st.error("Credenciais não configuradas.")
    st.markdown("Copie `.env.example` para `.env` e preencha servidor, usuário e senha. Não publique esse arquivo.")
    st.stop()

@st.cache_data(ttl=900, show_spinner=False)
def fetch_channels():
    client = IPTVClient()
    cats = client.live_categories()
    streams = client.live_streams()
    return normalize_live(streams, cats)

with st.sidebar:
    st.subheader("Conexão")
    st.write("Fonte configurada via variáveis de ambiente.")
    if st.button("🔄 Atualizar dados", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    st.divider()
    st.caption("A API do addon roda separadamente em api.py.")

try:
    with st.spinner("Consultando a fonte IPTV…"):
        channels = fetch_channels()
except IPTVError as exc:
    st.error(str(exc))
    st.stop()

groups = group_items(channels)
col1, col2, col3 = st.columns(3)
col1.metric("Canais ao vivo", len(channels))
col2.metric("Categorias", len(groups))
col3.metric("Com logotipo", sum(bool(c["logo"]) for c in channels))

st.subheader("Catálogos")
query = st.text_input("Pesquisar canal")
category_options = ["Todas"] + sorted(groups.keys(), key=str.casefold)
selected_category = st.selectbox("Categoria", category_options)

filtered = channels
if selected_category != "Todas":
    filtered = [c for c in filtered if c["category"] == selected_category]
if query.strip():
    filtered = [c for c in filtered if query.casefold() in c["name"].casefold()]

st.caption(f"Exibindo {len(filtered)} canal(is)")
for channel in filtered:
    with st.container(border=True):
        c1, c2 = st.columns([1, 5])
        with c1:
            if channel["logo"]:
                st.image(channel["logo"], width=72)
            else:
                st.write("📺")
        with c2:
            st.markdown(f"**{channel['name']}**")
            st.caption(channel["category"])
            if channel["epg_id"]:
                st.caption(f"EPG: {channel['epg_id']}")

st.divider()
st.subheader("Instalar no Stremio")
st.code(f"{ADDON_PUBLIC_URL}/manifest.json", language=None)
st.info("Hospede a API FastAPI em uma URL HTTPS pública antes de instalar no Stremio. O endereço local acima só funciona no seu computador.")
