# VIPABONENT Happ Routing

Автоматический профиль раздельной маршрутизации для Happ и 3x-ui.

## Логика

- российские домены (`geosite:category-ru` и `geosite:ru-available-only-inside`) → **DIRECT**, то есть напрямую через интернет пользователя;
- российские IP (`geoip:ru`) → **DIRECT**;
- локальные/служебные сети → **DIRECT**;
- всё остальное → **VPN / VLESS NL** благодаря `GlobalProxy: true`.

Это именно клиентская маршрутизация Happ: российский трафик не доходит до NL-сервера вообще.

## DNS

- зарубежный трафик: Cloudflare DoH — `https://cloudflare-dns.com/dns-query` / `1.1.1.1`;
- российский direct-трафик: Yandex DoH — `https://common.dot.dns.yandex.net/dns-query` / `77.88.8.8`.

## Geo-базы

Workflow ежедневно проверяет свежие базы:

- `geoip.dat` — официальный `v2fly/geoip`;
- `geosite.dat` — `runetfreedom/russia-v2ray-rules-dat`, который содержит категории v2fly и дополнительные российские категории.

Если базы изменились, GitHub Actions копирует их в `release/`, пересобирает Happ-профиль и обновляет `LastUpdated`.

Happ получает наши стабильные CDN-адреса:

- `https://cdn.jsdelivr.net/gh/Alexbubis0709/vipabonent-happ-routing@main/release/geoip.dat`
- `https://cdn.jsdelivr.net/gh/Alexbubis0709/vipabonent-happ-routing@main/release/geosite.dat`

## Что генерируется автоматически

После успешного workflow появятся:

- `HAPP/ROUTING.JSON` — итоговый профиль;
- `HAPP/ROUTING.DEEPLINK` — ручное добавление профиля;
- `HAPP/ROUTING.ONADD.DEEPLINK` — добавление + автоматическая активация;
- `HAPP/ROUTING.QR.png` — QR профиля;
- `release/geoip.dat`;
- `release/geosite.dat`.

## Подключение к 3x-ui

Для 3x-ui v3.10.2 можно использовать постоянный HTTPS URL вместо копирования длинного deeplink:

`https://raw.githubusercontent.com/Alexbubis0709/vipabonent-happ-routing/main/HAPP/ROUTING.JSON`

В панели:

1. **Настройки панели → Подписка → Happ**.
2. Включить **маршрутизацию**.
3. В поле **Правила маршрутизации** вставить URL выше.
4. Сохранить и перезапустить панель.
5. В Happ удалить старую тестовую подписку либо обновить подписку и переподключиться.

3x-ui скачает JSON, преобразует его в `happ://routing/onadd/...` и передаст Happ вместе с подпиской. Конечному пользователю достаточно одного QR-кода подписки — вручную правила не вводятся.

## Свои исключения

Можно добавлять исключения без изменения Python-кода:

- `custom/direct-domains.txt` — домены принудительно DIRECT;
- `custom/direct-cidr.txt` — IP/CIDR принудительно DIRECT;
- `custom/proxy-domains.txt` — домены принудительно через VPN;
- `custom/proxy-cidr.txt` — IP/CIDR принудительно через VPN.

После изменения этих файлов workflow автоматически пересоберёт профиль.
