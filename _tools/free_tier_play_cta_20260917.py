from pathlib import Path
from urllib.parse import urlencode
import html
import re

LOCALES = {
    'en': {
        'root': '', 'hl': 'en',
        'free': 'Free to install · 5 free uses every month without a subscription · Pro when you need more',
        'mid1_title': 'Try SIGNA with your own photo.',
        'mid1_body': 'You do not have to subscribe first. Install SIGNA, use the monthly free allowance, and decide from your own photos whether Pro is useful to you.',
        'mid2_title': 'See what SIGNA shows on a photo you already have.',
        'mid2_body': 'Watermark, SIGNA signal and supported image inspection are easier to judge on your own file than from a product description.',
        'button': 'Try SIGNA on Google Play',
        'article_title': 'Try SIGNA with a photo you already have',
        'article_body': 'Use the free monthly allowance to try SIGNA with a photo you already have before deciding whether Pro is useful for you.',
    },
    'ko': {
        'root': 'ko', 'hl': 'ko',
        'free': '무료 설치 · 구독 없이 매월 5회 무료 이용 · 더 필요할 때 Pro',
        'mid1_title': '내 사진으로 SIGNA를 직접 써보세요.',
        'mid1_body': '먼저 구독할 필요가 없습니다. 무료로 설치하고 매월 제공되는 5회 무료 이용으로 직접 확인한 뒤 Pro가 필요한지 판단하세요.',
        'mid2_title': '설명보다 내 사진으로 확인하는 편이 빠릅니다.',
        'mid2_body': '워터마크, SIGNA 신호, 지원되는 이미지 확인 기능을 실제로 가진 사진에서 직접 확인해 보세요.',
        'button': 'Google Play에서 SIGNA 사용해 보기',
        'article_title': '내 사진으로 SIGNA를 직접 써보기',
        'article_body': '먼저 가지고 있는 사진으로 SIGNA를 직접 써보세요. 구독 없이 매월 5회 무료로 이용한 뒤 Pro가 필요한지 판단할 수 있습니다.',
    },
    'ja': {
        'root': 'ja', 'hl': 'ja',
        'free': '無料インストール · サブスクなしで毎月5回まで無料 · もっと使うならPro',
        'mid1_title': '自分の写真でSIGNAを試してみる。',
        'mid1_body': '最初からサブスクする必要はありません。無料でインストールし、毎月5回まで試してからProが必要か判断できます。',
        'mid2_title': '説明を読むだけでなく、手元の写真で確かめる。',
        'mid2_body': 'ウォーターマーク、SIGNAシグナル、対応している画像チェックを実際の写真で試せます。',
        'button': 'Google PlayでSIGNAを試す',
        'article_title': '手元の写真でSIGNAを試す',
        'article_body': 'まずは手元の写真でSIGNAを試せます。サブスクなしで毎月5回まで無料で使ってから、Proが必要か判断できます。',
    },
    'zh-hans': {
        'root': 'zh-hans', 'hl': 'zh-CN',
        'free': '免费安装 · 无需订阅，每月可免费使用 5 次 · 需要更多时再升级 Pro',
        'mid1_title': '先用自己的照片试试 SIGNA。',
        'mid1_body': '不需要先订阅。免费安装后，每月可免费使用 5 次，再根据自己的照片决定是否需要 Pro。',
        'mid2_title': '与其只看介绍，不如直接用手头的照片验证。',
        'mid2_body': '可见水印、SIGNA 信号和当前支持的图片检查功能，都可以先在自己的照片上体验。',
        'button': '前往 Google Play 试用 SIGNA',
        'article_title': '用手头的照片试试 SIGNA',
        'article_body': '先用手头的照片试试 SIGNA。无需订阅，每月可免费使用 5 次，再决定是否需要 Pro。',
    },
    'es': {
        'root': 'es', 'hl': 'es-419',
        'free': 'Instalación gratuita · 5 usos gratis al mes sin suscripción · Pro si necesitas más',
        'mid1_title': 'Prueba SIGNA con una foto tuya.',
        'mid1_body': 'No necesitas suscribirte primero. Instálalo gratis, usa los 5 usos mensuales incluidos y decide con tus propias fotos si necesitas Pro.',
        'mid2_title': 'Compruébalo con una foto que ya tengas.',
        'mid2_body': 'La marca de agua, la señal SIGNA y la revisión de imagen compatible se entienden mejor al probarlas con tu propio archivo.',
        'button': 'Probar SIGNA en Google Play',
        'article_title': 'Prueba SIGNA con una foto que ya tengas',
        'article_body': 'Pruébalo primero con una foto que ya tengas. Tienes 5 usos gratis al mes sin suscripción y puedes decidir después si necesitas Pro.',
    },
    'pt-br': {
        'root': 'pt-br', 'hl': 'pt-BR',
        'free': 'Instalação gratuita · 5 usos grátis por mês sem assinatura · Pro se precisar de mais',
        'mid1_title': 'Teste o SIGNA com uma foto sua.',
        'mid1_body': 'Você não precisa assinar primeiro. Instale grátis, use as 5 utilizações mensais incluídas e decida com suas próprias fotos se precisa do Pro.',
        'mid2_title': 'Veja o SIGNA funcionando em uma foto que você já tem.',
        'mid2_body': 'Marca-d’água, sinal SIGNA e revisão de imagem compatível ficam mais claros quando você testa no próprio arquivo.',
        'button': 'Testar o SIGNA no Google Play',
        'article_title': 'Teste o SIGNA com uma foto que você já tem',
        'article_body': 'Teste primeiro com uma foto que você já tem. São 5 usos grátis por mês sem assinatura; depois você decide se precisa do Pro.',
    },
    'fr': {
        'root': 'fr', 'hl': 'fr',
        'free': 'Installation gratuite · 5 utilisations gratuites par mois sans abonnement · Pro si vous en avez besoin',
        'mid1_title': 'Essayez SIGNA avec l’une de vos photos.',
        'mid1_body': 'Aucun abonnement n’est nécessaire pour commencer. Installez SIGNA gratuitement, profitez de 5 utilisations par mois, puis décidez si Pro vous est utile.',
        'mid2_title': 'Voyez ce que SIGNA montre sur une photo que vous avez déjà.',
        'mid2_body': 'Le filigrane, le signal SIGNA et l’analyse d’image prise en charge sont plus faciles à évaluer sur votre propre fichier.',
        'button': 'Essayer SIGNA sur Google Play',
        'article_title': 'Essayez SIGNA avec une photo que vous avez déjà',
        'article_body': 'Essayez d’abord SIGNA avec une photo que vous avez déjà. Vous disposez de 5 utilisations gratuites par mois sans abonnement, puis vous décidez si Pro vous est utile.',
    },
    'de': {
        'root': 'de', 'hl': 'de',
        'free': 'Kostenlos installieren · 5 kostenlose Nutzungen pro Monat ohne Abo · Pro, wenn du mehr brauchst',
        'mid1_title': 'Teste SIGNA mit deinem eigenen Foto.',
        'mid1_body': 'Du musst nicht zuerst ein Abo abschließen. Installiere SIGNA kostenlos, nutze die 5 kostenlosen Anwendungen pro Monat und entscheide danach, ob du Pro brauchst.',
        'mid2_title': 'Probier es mit einem Foto aus, das du schon hast.',
        'mid2_body': 'Wasserzeichen, SIGNA-Signal und unterstützte Bildprüfung lassen sich am besten mit deiner eigenen Datei beurteilen.',
        'button': 'SIGNA bei Google Play ausprobieren',
        'article_title': 'Teste SIGNA mit einem Foto, das du schon hast',
        'article_body': 'Teste SIGNA zuerst mit einem Foto, das du bereits hast. Du kannst es ohne Abo fünfmal pro Monat kostenlos nutzen und danach entscheiden, ob du Pro brauchst.',
    },
}


def play_url(locale, campaign, content):
    cfg = LOCALES[locale]
    params = {
        'id': 'com.signa.app',
        'hl': cfg['hl'],
        'utm_source': 'signa_website',
        'utm_medium': 'website',
        'utm_campaign': campaign,
        'utm_content': content,
    }
    return 'https://play.google.com/store/apps/details?' + html.escape(urlencode(params), quote=True)


def home_path(cfg):
    return Path(cfg['root']) / 'index.html' if cfg['root'] else Path('index.html')


def home_strip(locale, placement, title, body):
    cfg = LOCALES[locale]
    href = play_url(locale, f'homepage_{locale}', placement)
    return (
        f'<section class="conversion-strip" data-conversion-placement="{placement}"><div class="container conversion-card">'
        f'<div class="conversion-copy"><h3>{title}</h3><p>{body}</p><div class="free-access-note">{cfg["free"]}</div></div>'
        f'<a class="btn-secondary conversion-link" href="{href}" target="_blank" rel="noopener" '
        f'data-umami-event="google-play-click" data-umami-event-source="homepage" data-umami-event-placement="{placement}" '
        f'data-umami-event-locale="{locale}" data-umami-event-campaign="homepage_{locale}">{cfg["button"]} →</a>'
        f'</div></section>'
    )


def upgrade_home(locale, cfg):
    p = home_path(cfg)
    t = p.read_text(encoding='utf-8')
    original = t
    assert 'data-conversion-placement="after-intro"' not in t, p
    assert 'data-conversion-placement="after-analysis"' not in t, p
    assert t.count('data-umami-event="google-play-click"') == 2, (p, t.count('data-umami-event="google-play-click"'))

    t = t.replace('<div class="hero-meta">', f'<div class="free-access-note free-access-note--hero">{cfg["free"]}</div><div class="hero-meta">', 1)

    anchor1 = '</section>\n<section class="story" id="watermark">'
    assert anchor1 in t, p
    t = t.replace(anchor1, '</section>\n' + home_strip(locale, 'after-intro', cfg['mid1_title'], cfg['mid1_body']) + '\n<section class="story" id="watermark">', 1)

    anchor2 = '</section>\n<section class="report" id="report">'
    assert anchor2 in t, p
    t = t.replace(anchor2, '</section>\n' + home_strip(locale, 'after-analysis', cfg['mid2_title'], cfg['mid2_body']) + '\n<section class="report" id="report">', 1)

    final_start = t.index('<section class="final">')
    final_end = t.index('</section>', final_start)
    final = t[final_start:final_end]
    badge = '<a class="official-play-badge"'
    assert badge in final, p
    final = final.replace(badge, f'<div class="free-access-note free-access-note--final">{cfg["free"]}</div>{badge}', 1)
    t = t[:final_start] + final + t[final_end:]

    assert t.count('data-umami-event="google-play-click"') == 4, p
    assert t.count(cfg['free']) == 4, (p, t.count(cfg['free']))
    p.write_text(t, encoding='utf-8')
    return original != t


def locale_for_article(p):
    parts = p.as_posix().split('/')
    if parts[0] == 'articles':
        return 'en'
    return parts[0]


def article_mid(locale, slug):
    cfg = LOCALES[locale]
    campaign = f'article_{slug}_{locale}'
    href = play_url(locale, campaign, 'mid-article-free')
    return (
        f'<div class="micro-cta"><strong>{cfg["article_title"]}</strong><p>{cfg["article_body"]}</p>'
        f'<div class="free-access-note">{cfg["free"]}</div>'
        f'<a href="{href}" target="_blank" rel="noopener" data-umami-event="google-play-click" '
        f'data-umami-event-source="article" data-umami-event-placement="mid-article-free" '
        f'data-umami-event-locale="{locale}" data-umami-event-campaign="{campaign}" data-umami-event-article="{slug}">{cfg["button"]} →</a></div>'
    )


def upgrade_article(p):
    locale = locale_for_article(p)
    cfg = LOCALES[locale]
    slug = p.parent.name
    t = p.read_text(encoding='utf-8')
    original = t
    assert t.count('class="micro-cta"') == 1, p
    assert t.count('data-umami-event="google-play-click"') == 1, (p, t.count('data-umami-event="google-play-click"'))

    t, n = re.subn(r'<div class="micro-cta">.*?</div>', article_mid(locale, slug), t, count=1, flags=re.S)
    assert n == 1, p

    start = t.index('<section class="article-cta">')
    end = t.index('</section>', start)
    sec = t[start:end]
    badge = '<a class="official-play-badge"'
    assert badge in sec, p
    sec = sec.replace(badge, f'<div class="free-access-note free-access-note--article-final">{cfg["free"]}</div>{badge}', 1)
    t = t[:start] + sec + t[end:]

    assert t.count('data-umami-event="google-play-click"') == 2, p
    assert t.count(cfg['free']) == 2, (p, t.count(cfg['free']))
    assert 'data-umami-event="article-product-interest"' not in t, p
    p.write_text(t, encoding='utf-8')
    return original != t


def normalize_german_tone():
    paths = [Path('de/index.html')] + list(Path('de/articles').glob('*/index.html'))
    replacements = {
        'Prüfen Sie': 'Prüfe',
        'Fragen Sie': 'Frag',
        'Kombinieren Sie': 'Kombiniere',
        'Nutzen Sie': 'Nutze',
        'Lesen Sie': 'Lies',
        'Vergleichen Sie': 'Vergleiche',
        'Beachten Sie': 'Beachte',
        'Sehen Sie': 'Sieh',
        'Öffnen Sie': 'Öffne',
        'Schauen Sie': 'Schau',
        'Testen Sie': 'Teste',
        'Überprüfen Sie': 'Überprüfe',
        'Bewerten Sie': 'Bewerte',
        'Stellen Sie': 'Stell',
        'Speichern Sie': 'Speichere',
        'Verwenden Sie': 'Verwende',
        'Denken Sie': 'Denk',
    }
    changed = 0
    for p in paths:
        t = p.read_text(encoding='utf-8')
        o = t
        for a, b in replacements.items():
            t = t.replace(a, b)
        if t != o:
            p.write_text(t, encoding='utf-8')
            changed += 1
    return changed


def append_css():
    p = Path('styles-live.css')
    t = p.read_text(encoding='utf-8')
    marker = '/* FREE_TIER_PLAY_CTA_20260917 */'
    if marker not in t:
        t += '''\n/* FREE_TIER_PLAY_CTA_20260917 */\n.free-access-note{margin-top:10px;font-size:13px;line-height:1.55;font-weight:700;opacity:.78}.free-access-note--hero{margin-top:12px}.free-access-note--final{margin:10px 0 14px}.conversion-strip{padding:8px 0 22px}.conversion-card{display:flex;align-items:center;justify-content:space-between;gap:28px;padding:22px 24px;border:1px solid rgba(127,127,127,.22);border-radius:18px;background:rgba(127,127,127,.055)}.conversion-copy{max-width:760px}.conversion-copy h3{margin:0 0 7px;font-size:clamp(20px,2.2vw,28px);line-height:1.2}.conversion-copy p{margin:0;line-height:1.65}.conversion-link{flex:0 0 auto;text-align:center;white-space:nowrap}@media(max-width:760px){.conversion-card{align-items:flex-start;flex-direction:column;gap:16px}.conversion-link{width:100%;white-space:normal}}\n'''
        p.write_text(t, encoding='utf-8')

    ap = Path('articles/articles.css')
    a = ap.read_text(encoding='utf-8')
    amarker = '/* FREE_TIER_ARTICLE_CTA_20260917 */'
    if amarker not in a:
        a += '''\n/* FREE_TIER_ARTICLE_CTA_20260917 */\n.article .micro-cta .free-access-note{margin:8px 0 10px}.article-cta .free-access-note{margin:8px 0 14px}\n'''
        ap.write_text(a, encoding='utf-8')


def validate():
    for locale, cfg in LOCALES.items():
        p = home_path(cfg)
        t = p.read_text(encoding='utf-8')
        assert '\ufffd' not in t, p
        assert t.count('data-umami-event="google-play-click"') == 4, p
        assert t.count(cfg['free']) == 4, p
        assert t.count('data-conversion-placement="after-intro"') == 1, p
        assert t.count('data-conversion-placement="after-analysis"') == 1, p

    article_paths = list(Path('articles').glob('*/index.html'))
    for loc in ['ko','ja','zh-hans','es','pt-br','fr','de']:
        article_paths += list(Path(loc, 'articles').glob('*/index.html'))
    assert len(article_paths) == 48, len(article_paths)
    for p in article_paths:
        locale = locale_for_article(p)
        t = p.read_text(encoding='utf-8')
        assert '\ufffd' not in t, p
        assert t.count('data-umami-event="google-play-click"') == 2, p
        assert t.count(LOCALES[locale]['free']) == 2, p
        assert 'data-umami-event="article-product-interest"' not in t, p
        assert t.count('class="next-reads"') == 1, p

    # German site uses informal du/dein consistently. If formal second-person forms remain,
    # print contexts and stop instead of silently shipping mixed tone.
    german_paths = [Path('de/index.html')] + list(Path('de/articles').glob('*/index.html'))
    bad = []
    formal = re.compile(r'\b(?:Sie|Ihnen|Ihr|Ihre|Ihren|Ihrem|Ihrer|Ihres)\b')
    for p in german_paths:
        t = p.read_text(encoding='utf-8')
        for m in formal.finditer(t):
            bad.append((p.as_posix(), t[max(0,m.start()-55):m.end()+55]))
    if bad:
        for item in bad[:30]:
            print('GERMAN_FORMAL_REMAINS:', item)
        raise AssertionError(f'German formal forms remain: {len(bad)}')

    print('validated 8 homepages: 4 Play touchpoints each')
    print('validated 48 article pages: 2 Play touchpoints each')
    print('validated free-tier copy and German informal tone')


changed = 0
for locale, cfg in LOCALES.items():
    changed += int(upgrade_home(locale, cfg))

article_paths = list(Path('articles').glob('*/index.html'))
for loc in ['ko','ja','zh-hans','es','pt-br','fr','de']:
    article_paths += list(Path(loc, 'articles').glob('*/index.html'))
assert len(article_paths) == 48, len(article_paths)
for p in article_paths:
    changed += int(upgrade_article(p))

german_changed = normalize_german_tone()
append_css()
validate()
print(f'changed content pages: {changed}; German tone pages adjusted: {german_changed}')
