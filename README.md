# IPTV → Stremio (Streamlit + FastAPI)

Projeto-base para visualizar e organizar canais ao vivo de uma conta IPTV autorizada e expor catálogos por meio do protocolo de add-ons do Stremio.

## Arquitetura
- **Streamlit (`app.py`)**: painel para listar, pesquisar e filtrar canais.
- **FastAPI (`api.py`)**: endpoints do add-on Stremio (`manifest`, `catalog`, `meta`, `stream`).
- **Xtream Codes API (`core/iptv_client.py`)**: consulta categorias e canais ao vivo.
- **Credenciais**: variáveis de ambiente em `.env`; nunca faça commit desse arquivo.

Este template implementa **TV ao vivo**. Não implementa VOD/filmes/séries. O formato de catálogo `tv` e o comportamento de reprodução podem variar entre versões e clientes Stremio; valide com a versão do Stremio que você usa antes de considerar pronto para produção.

## Configuração local

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
```

Edite `.env` com os dados do seu provedor autorizado:
- `IPTV_BASE_URL`: origem do servidor, sem `/get.php` ou `/player_api.php`
- `IPTV_USERNAME`
- `IPTV_PASSWORD`
- `ADDON_PUBLIC_URL`: URL pública da API quando implantada

### Executar painel
```bash
streamlit run app.py
```

### Executar API do addon
Em outro terminal:
```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

Teste:
- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/manifest.json`

No Stremio, adicione a URL pública HTTPS terminada em `/manifest.json`.

## Implantação
O Streamlit Community Cloud pode hospedar o painel, mas o addon precisa de um serviço que mantenha a API FastAPI disponível publicamente por HTTPS. Você pode implantar a API em um serviço de aplicações Python compatível com ASGI e configurar as variáveis de ambiente no painel desse serviço. Não publique `.env`.

## Segurança
- A URL de origem com usuário/senha é credencial sensível.
- Se credenciais já foram compartilhadas, rotacione-as no painel do provedor.
- Não salve URLs de reprodução nem credenciais em `channels.json`, no GitHub ou em logs.
- O addon retorna links de reprodução ao Stremio; quem tiver acesso à URL do addon poderá solicitar catálogos e streams. Para uso privado, adicione autenticação ou restrinja o acesso no proxy/host.
- Use somente conteúdo e serviços para os quais você tenha autorização de acesso e redistribuição.
