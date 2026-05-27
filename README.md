# Auto Sing-Box Config Builder

Автоматическая генерация sing-box конфигов из публичной подписки VLESS/VMess/Trojan через GitHub Actions.

Проект создавался для слабых роутеров, где:
- TUN сильно грузит CPU
- сотни routing rules превращают роутер в тостер
- половина публичных ключей мёртвые
- интернет в некоторых регионах внезапно стал “по списку разрешённых сайтов”

Поэтому здесь всё максимально просто:
- фильтрация ключей
- ограничение количества серверов
- автоматическая сборка JSON
- автообновление через GitHub Actions

---

# Что генерируется

## config.json
Конфиг с 5 серверами.

Оптимальный вариант для слабых роутеров типа Keenetic на базе MIPS, MIPSEL

---

## config10.json
Конфиг с 10 серверами.

Более живучий, но тяжелее для CPU.

---

# Как это работает

text TXT subscription       ↓ GitHub Actions       ↓ filter proxies       ↓ POST → api.web2core.workers.dev       ↓ готовый config.json       ↓ роутер скачивает конфиг       ↓ sing-box restart 

---

# Используемая подписка

По умолчанию используется:

text https://raw.githack.com/igareck/vpn-configs-for-russia/main/Vless-Reality-White-Lists-Rus-Mobile.txt 

---

# Фильтрация

Оставляются только строки:

- vless://
- vmess://
- trojan://

И дополнительно:
- содержащие russia

---

# GitHub Actions

Workflow:
text .github/workflows/build.yml 

Запускается:
- каждый час
- вручную через Run workflow

---

# Роутер

На роутере нужен:
- curl
- sing-box
- cron/Entware

---

# Пример обновления на роутере

bash curl -fL -o /opt/etc/sing-box/config.json \ https://raw.githubusercontent.com/USER/REPO/main/config.json \ && /opt/etc/init.d/S99sing-box restart 

Готовый скрипт находится в update.sh

---

# Cron пример

cron 0 */6 * * * /opt/bin/update.sh 

---

# Важно

Для слабых роутеров НЕ рекомендуется:
- большое количество outbounds
- огромные geosite базы
- regex routing
- сложный split tunneling
- десятки urltest узлов

Embedded железо любит:
text простую маршрутизацию минимум правил минимум логики 

---

# Используемое API

text https://api.web2core.workers.dev/ 

Используется для:
- конвертации proxy links
- генерации sing-box JSON

---

# Disclaimer

Проект предоставляется как есть.

Публичные ключи:
- могут перестать работать
- могут быть перегружены
- могут исчезнуть в любой момент

Никакой стабильности не гарантируется.

Потому что публичные VPN-листы живут по законам дикой природы.
