# NotebookLM × Claude Code — MCP Kurulumu

Bu repo, NotebookLM'i Claude Code'a bağlamak için
[`jacob-bd/notebooklm-mcp-cli`](https://github.com/jacob-bd/notebooklm-mcp-cli)
topluluk projesini kullanır. Repodaki kökteki [`.mcp.json`](../.mcp.json) sunucuyu
proje kapsamında otomatik tanıtır; geri kalan adımlar (paket kurulumu + Google girişi)
**yerel makinende** yapılır.

> Kaynak: "NotebookLM x Claude Code Kurulum Rehberi" — Defne İncekara (Mayıs 2026),
> + bu ortamda yapılan gerçek kurulum doğrulaması.

---

## ⚠️ Önce dürüst uyarı

- **NotebookLM'in resmi API'si yok.** Tüm "NotebookLM MCP" çözümleri Google'ın dahili
  (undocumented) API'lerini çerez tabanlı kimlik doğrulamayla çağırır.
- Google bunu istediği zaman değiştirebilir/kapatabilir → entegrasyon bir gün kırılabilir.
- Otomatik erişim **Google ToS açısından gri alandır**; kurumsal SLA için uygun değildir.
- Proje README'sinde "vibe coding" ile yazıldığı belirtilir; çalışır ve aktif bakımlıdır,
  ama kurumsal garanti standartları beklenmemeli.
- **Hassas veri koyma:** müşteri PII'sı, sözleşme, KVKK kapsamındaki belgeler NotebookLM'e
  atılmamalı. Çerez tabanlı kimlik = Google hesabının erişim anahtarı; disk şifrelemen açık olsun.

Güvenli kullanım: kendi araştırma kütüphanen, public web kaynakları, eğitim/atölye demoları,
içerik üretimi (Substack, LinkedIn, slayt).

---

## Ön koşullar

- Python 3.10+
- `uv` paket yöneticisi (önerilen) veya `pip`
- Aktif NotebookLM hesabı (Google Workspace veya kişisel Gmail)
- Yerel Claude Code kurulu ve çalışır durumda
- **Tarayıcı** (Chrome / Brave / Edge / Arc / Chromium) — Google girişi için zorunlu

---

## Kurulum (yerel makine — 5 adım)

```bash
# 1) uv (zaten varsa atla)
#    Mac/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh
#    Windows (PowerShell):
#    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2) CLI (nlm) + MCP sunucusu (notebooklm-mcp) — tek komut
uv tool install notebooklm-mcp-cli
nlm --version                       # doğrulama

# 3) Google ile kimlik doğrula (tarayıcı açılır, cookie'ler yerelde saklanır)
nlm login
#    Çoklu hesap:
#    nlm login --profile work
#    nlm login --profile personal

# 4) MCP'yi Claude Code'a tanıt (manuel JSON yok)
nlm setup add claude-code
nlm setup list                      # durum

# 5) Claude Code'u tamamen kapat-aç, yeni oturum başlat ve test et:
#    "NotebookLM'deki tüm notebook'larımı listele."
```

Hata alırsan teşhis: `nlm doctor`

### `.mcp.json` ile proje kapsamı (bu repo)

Bu repoyu yerel Claude Code'da açtığında, kökteki `.mcp.json` sayesinde sunucu **proje
kapsamında** otomatik önerilir (Claude Code bir kez onay ister). Bu durumda 4. adımdaki
`nlm setup add claude-code` (kullanıcı kapsamı) opsiyoneldir — ikisinden biri yeterlidir.
Her hâlükârda `uv tool install` (2) ve `nlm login` (3) yine gereklidir; kimlik doğrulama makineye bağlıdır.

```json
{
  "mcpServers": {
    "notebooklm-mcp": { "type": "stdio", "command": "notebooklm-mcp", "args": [], "env": {} }
  }
}
```

İsteğe bağlı env değişkenleri: `NOTEBOOKLM_HL=tr` (arayüz/üretim dili), `NOTEBOOKLM_QUERY_TIMEOUT=120`.

---

## ⛔ Uzak / web oturumunda (Claude Code on the web) durum

Bu repo bir bulut/headless konteynırda açıldığında entegrasyon **varsayılan olarak işlevsel
değildir**:

| Adım | Web/uzak oturumda durum |
|------|--------------------------|
| `uv tool install notebooklm-mcp-cli` | ✅ Çalışır (PyPI erişilebilir) |
| MCP sunucusunun başlaması (`stdio`) | ✅ "Connected" — süreç ayağa kalkar, araçlar yüklenir |
| `nlm login` (Chrome ile auth) | ❌ Tarayıcı yok (`DISPLAY` boş, browser kurulu değil) |
| Notebook listeleme / sorgu | ❌ Kayıtlı profil/cookie yok → `No authentication found` |
| Kalıcılık | ❌ Konteynır geçici; oturum bitince kurulum & cookie silinir |
| Google erişimi | ⚠️ Ağ politikası bazı Google uçlarını kısıtlıyor olabilir |

### Tarayıcısız (web) auth seçeneği — `NOTEBOOKLM_COOKIES`

Sunucu, `nlm login` dışında ikinci bir yol sunar: NotebookLM çerezlerini `NOTEBOOKLM_COOKIES`
ortam değişkeni ile manuel vermek. Yani **yerel** makinende `nlm login` yapıp çerezleri
çıkarır, web ortamının yapılandırmasında `NOTEBOOKLM_COOKIES` olarak ayarlarsan headless
oturumda da çalışabilir.

> 🔐 **Güvenlik uyarısı:** Bu çerezler Google hesabının erişim anahtarıdır. Bir bulut
> konteynırının ortam değişkenine koymak, o anahtarı orada açığa çıkarmak demektir. Sadece
> riski kabul ediyorsan ve hassas veri içermeyen bir hesapla yap. Kurumsal/müşteri verisi için **yapma**.

---

## Yaygın sorunlar

- **AUTHENTICATION FAILED / No authentication found** → cookie yok veya süresi dolmuş (2–4 hafta). `nlm login` (tekrar).
- **Claude Code MCP'yi görmüyor** → uygulamayı tamamen kapat-aç; `nlm doctor` çalıştır.
- **RATE LIMIT EXCEEDED** → Free tier ~50 sorgu/gün. Soruları birleştir; Pro/Ultra'ya geç.
- **Tarayıcı açılmıyor** → `nlm config set auth.browser chrome` (veya brave/edge/arc/chromium).
- **Studio üretimi takılıyor** → audio/video 2–5 dk sürer; "durumunu kontrol et" diye tekrar sor.

---

## Hazır prompt'lar

1. "NotebookLM'deki tüm notebook'larımı listele. Her birinin kaç kaynak içerdiğini de göster."
2. "\"AI Strateji Araştırması\" notebook'umdaki ana bulguları özetle. Her bulgu için kaynak göster."
3. "Şu URL'yi \"Pazarlama Trendleri\" notebook'uma ekle: <url>"
4. "\"Müşteri Görüşmeleri\" ve \"Ürün Geri Bildirimleri\" notebook'larındaki ortak temaları çıkar."
5. "\"Q1 Strateji\" notebook'undan deep dive formatında podcast üret; bitince indirme linkini ver."
6. "\"AI-First Index Araştırması\" notebook'undaki kaynakları araştır, marka kimliğine uygun Türkçe slayt taslağı çıkar."

---

## Bu repoda doğrulanan durum

- `notebooklm-mcp-cli` **v0.6.13** PyPI'den temiz kuruldu (`nlm`, `notebooklm-mcp`).
- MCP sunucusu `stdio` ile başlıyor ve protokol el sıkışmasını geçiyor (`✓ Connected`); araçlar Claude Code oturumuna yüklendi.
- `nlm doctor`: `Profiles: none`, `Browser: not found`.
- Canlı test → `notebook_list` çağrısı: `No authentication found` (beklenen davranış; yerelde `nlm login` ile çözülür).
