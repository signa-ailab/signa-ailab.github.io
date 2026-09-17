from pathlib import Path
import re

DATE = "2026-09-17"
SLUGS = [
    "can-you-tell-if-a-photo-was-edited",
    "image-metadata",
    "invisible-watermark",
    "photo-privacy-before-sharing",
    "what-happens-when-you-share-a-photo",
    "on-device-photo-processing-privacy",
]
LOCALES = {
    "en": "",
    "ko": "ko",
    "ja": "ja",
    "zh-hans": "zh-hans",
    "es": "es",
    "pt-br": "pt-br",
    "fr": "fr",
    "de": "de",
}

UI = {
"en": {"summary":"What to take from this guide","continue":"Continue reading","product":"Try the framework on your own photo","product_body":"SIGNA is designed to review supported image information on the Android device, so you can inspect the file you actually have before deciding what the evidence means.","product_link":"See how SIGNA works →","next":"Next layer","then":"Then"},
"ko": {"summary":"이 글에서 가져갈 핵심","continue":"다음으로 읽을 글","product":"내 사진에서도 같은 순서로 확인해 보기","product_body":"SIGNA는 지원되는 이미지 정보를 Android 기기에서 확인하도록 설계되어 있습니다. 실제로 가진 파일을 먼저 살펴본 뒤, 관찰된 정보가 무엇을 의미하는지 판단할 수 있습니다.","product_link":"SIGNA가 이미지를 확인하는 방식 보기 →","next":"다음 단계","then":"이어서"},
"ja": {"summary":"この記事で押さえるポイント","continue":"次に読む記事","product":"自分の写真でも同じ手順で確認する","product_body":"SIGNAは、対応する画像情報をAndroid端末上で確認できるよう設計されています。まず手元のファイルを見てから、観察結果が何を意味するのかを判断できます。","product_link":"SIGNAの確認フローを見る →","next":"次のレイヤー","then":"続いて"},
"zh-hans": {"summary":"这篇文章最值得带走的几点","continue":"继续阅读","product":"用自己的照片按同样思路检查","product_body":"SIGNA 的受支持图像检查流程以 Android 设备端处理为中心。先查看你手上的实际文件，再判断这些观察结果能够说明什么。","product_link":"查看 SIGNA 如何检查图像 →","next":"下一层","then":"接着读"},
"es": {"summary":"Qué conviene llevarse de esta guía","continue":"Sigue leyendo","product":"Prueba el mismo enfoque con tu propia foto","product_body":"SIGNA está diseñado para revisar en el dispositivo Android la información de imagen compatible, de modo que puedas observar el archivo que realmente tienes antes de decidir qué significan las señales.","product_link":"Ver cómo revisa imágenes SIGNA →","next":"Siguiente capa","then":"Después"},
"pt-br": {"summary":"O que vale levar deste guia","continue":"Continue lendo","product":"Aplique o mesmo raciocínio à sua própria foto","product_body":"O SIGNA foi projetado para revisar no próprio dispositivo Android as informações de imagem compatíveis, para que você observe o arquivo que realmente tem antes de decidir o que os sinais significam.","product_link":"Veja como o SIGNA revisa imagens →","next":"Próxima camada","then":"Depois"},
"fr": {"summary":"À retenir de ce guide","continue":"Poursuivre la lecture","product":"Appliquer la même méthode à votre propre photo","product_body":"SIGNA est conçu pour examiner sur l’appareil Android les informations d’image prises en charge, afin d’observer d’abord le fichier réellement disponible avant d’interpréter ce que les indices peuvent signifier.","product_link":"Voir comment SIGNA examine une image →","next":"Étape suivante","then":"Puis"},
"de": {"summary":"Das Wichtigste aus diesem Artikel","continue":"Weiterlesen","product":"Den gleichen Ansatz mit dem eigenen Foto ausprobieren","product_body":"SIGNA ist darauf ausgelegt, unterstützte Bildinformationen direkt auf dem Android-Gerät zu prüfen. So lässt sich zuerst die tatsächlich vorliegende Datei betrachten, bevor Beobachtungen interpretiert werden.","product_link":"So prüft SIGNA Bildinformationen →","next":"Nächste Ebene","then":"Danach"},
}

SUMMARY = {
"en": {
"can-you-tell-if-a-photo-was-edited":["Start with the file state, not an edited/not-edited verdict.","Combine metadata, compression, geometry, watermark and provenance observations.","Keep observation, interpretation and proof limits separate."],
"image-metadata":["Identify the metadata container before interpreting a value.","A software or workflow declaration is context, not a complete history.","Missing metadata is also ambiguous."],
"invisible-watermark":["Invisible watermarks are image signals, not hidden EXIF.","Detection and payload recovery are different tasks.","Robustness claims need the exact test conditions."],
"photo-privacy-before-sharing":["Check both visible details and file-level information.","Decide whether the recipient needs the original or a sharing copy.","Make the privacy decision before the upload."],
"what-happens-when-you-share-a-photo":["A visually identical image can be a different digital file.","Compare file structure, metadata, pixels/signals and provenance separately.","Platform observations should always state route and date."],
"on-device-photo-processing-privacy":["Training and retention rules vary by service, account, settings and date.","Check the current official policy for the exact service you use.","Ask whether the photo needs to leave the device at all."],
},
"ko": {
"can-you-tell-if-a-photo-was-edited":["‘편집됨/안 됨’ 결론보다 현재 파일 상태부터 확인합니다.","메타데이터·압축·크기 변화·신호·출처 정보를 함께 봅니다.","관찰과 해석, 입증 가능한 범위를 분리합니다."],
"image-metadata":["값을 해석하기 전에 어떤 메타데이터 구조에서 나온 값인지 확인합니다.","소프트웨어·워크플로 선언은 맥락이지 전체 이력이 아닙니다.","메타데이터가 없다는 사실도 여러 원인이 있을 수 있습니다."],
"invisible-watermark":["보이지 않는 워터마크는 숨겨진 EXIF가 아니라 이미지 신호입니다.","신호 검출과 페이로드 복원은 다른 과제입니다.","강인성 수치는 반드시 시험 조건과 함께 읽어야 합니다."],
"photo-privacy-before-sharing":["사진에 보이는 정보와 파일 안의 정보를 둘 다 확인합니다.","원본이 필요한지, 공유용 사본이면 충분한지 결정합니다.","개인정보 판단은 업로드 전에 끝내는 것이 좋습니다."],
"what-happens-when-you-share-a-photo":["눈에 같아 보여도 디지털 파일은 달라질 수 있습니다.","파일 구조·메타데이터·픽셀/신호·출처 정보를 따로 비교합니다.","플랫폼 관찰은 경로와 날짜를 함께 기록해야 합니다."],
"on-device-photo-processing-privacy":["학습·보관 정책은 서비스·계정·설정·시점에 따라 달라집니다.","내가 쓰는 정확한 서비스의 최신 공식 정책을 확인합니다.","그 사진이 애초에 기기 밖으로 나갈 필요가 있는지 먼저 묻습니다."],
},
"ja": {
"can-you-tell-if-a-photo-was-edited":["「編集済みか」の二択より、まず現在のファイル状態を確認します。","メタデータ、圧縮、形状変化、信号、来歴を組み合わせて見ます。","観察・解釈・証明できる範囲を分けます。"],
"image-metadata":["値を読む前に、どのメタデータ構造から来たかを確認します。","ソフトウェアやワークフローの宣言は文脈であり、完全な履歴ではありません。","メタデータがないことにも複数の理由があります。"],
"invisible-watermark":["不可視ウォーターマークは隠れたEXIFではなく画像信号です。","検出とペイロード復元は別の課題です。","耐性の数値は必ず試験条件と一緒に読みます。"],
"photo-privacy-before-sharing":["画面に見える情報とファイル内の情報を両方確認します。","原本が必要か、共有用コピーで十分かを決めます。","プライバシー判断はアップロード前に行います。"],
"what-happens-when-you-share-a-photo":["見た目が同じでもデジタルファイルは変わり得ます。","ファイル構造、メタデータ、画素/信号、来歴を別々に比較します。","プラットフォームの観察には経路と日付を残します。"],
"on-device-photo-processing-privacy":["学習・保持のルールはサービス、アカウント、設定、時期で変わります。","利用するサービスの最新の公式ポリシーを確認します。","そもそも写真を端末外へ送る必要があるかを先に考えます。"],
},
"zh-hans": {
"can-you-tell-if-a-photo-was-edited":["先检查当前文件状态，而不是急着给出“编辑过/没编辑过”的结论。","把元数据、压缩、几何变化、信号和来源信息放在一起看。","区分观察、解释和真正能够证明的范围。"],
"image-metadata":["解释一个值之前，先确认它来自哪种元数据结构。","软件或工作流声明提供的是上下文，不是完整历史。","没有元数据同样可能有多种原因。"],
"invisible-watermark":["不可见水印是图像信号，不是隐藏的 EXIF。","信号检测和载荷恢复是不同任务。","任何鲁棒性数字都应与测试条件一起阅读。"],
"photo-privacy-before-sharing":["同时检查画面里看得见的信息和文件里的信息。","判断对方是否真的需要原文件，还是分享副本就足够。","隐私决定最好在上传之前完成。"],
"what-happens-when-you-share-a-photo":["看起来一样的图片，也可能已经是不同的数字文件。","分别比较文件结构、元数据、像素/信号和来源信息。","平台观察必须同时记录具体路径和日期。"],
"on-device-photo-processing-privacy":["训练和保留规则会随服务、账户、设置和时间变化。","查看你实际使用服务的最新官方政策。","先问一句：这张照片真的需要离开设备吗？"],
},
"es": {
"can-you-tell-if-a-photo-was-edited":["Empieza por el estado del archivo, no por un veredicto de “editada/no editada”.","Combina metadatos, compresión, geometría, señales y procedencia.","Separa observación, interpretación y lo que realmente puede demostrarse."],
"image-metadata":["Identifica el contenedor de metadatos antes de interpretar un valor.","Una declaración de software o flujo aporta contexto, no un historial completo.","La ausencia de metadatos también es ambigua."],
"invisible-watermark":["Una marca de agua invisible es una señal de imagen, no EXIF oculto.","Detectar una señal y recuperar una carga útil son tareas distintas.","Toda cifra de robustez necesita sus condiciones de prueba."],
"photo-privacy-before-sharing":["Revisa tanto lo visible en la escena como la información del archivo.","Decide si hace falta el original o basta una copia para compartir.","Toma la decisión de privacidad antes de subir la foto."],
"what-happens-when-you-share-a-photo":["Una imagen que se ve igual puede ser un archivo digital distinto.","Compara por separado estructura, metadatos, píxeles/señales y procedencia.","Toda observación de plataforma debe indicar ruta y fecha."],
"on-device-photo-processing-privacy":["Las reglas de entrenamiento y retención cambian según servicio, cuenta, ajustes y fecha.","Consulta la política oficial vigente del servicio exacto que utilizas.","Pregunta primero si esa foto necesita salir del dispositivo."],
},
"pt-br": {
"can-you-tell-if-a-photo-was-edited":["Comece pelo estado do arquivo, não por um veredito de “editada/não editada”.","Combine metadados, compressão, geometria, sinais e procedência.","Separe observação, interpretação e o que realmente pode ser provado."],
"image-metadata":["Identifique o contêiner de metadados antes de interpretar um valor.","Uma declaração de software ou fluxo traz contexto, não um histórico completo.","A ausência de metadados também é ambígua."],
"invisible-watermark":["Marca d’água invisível é um sinal na imagem, não EXIF escondido.","Detecção e recuperação de payload são tarefas diferentes.","Toda taxa de robustez precisa das condições de teste."],
"photo-privacy-before-sharing":["Revise tanto o que aparece na cena quanto as informações do arquivo.","Decida se o destinatário precisa do original ou de uma cópia para compartilhar.","Tome a decisão de privacidade antes do upload."],
"what-happens-when-you-share-a-photo":["Uma imagem visualmente igual pode ser um arquivo digital diferente.","Compare estrutura, metadados, pixels/sinais e procedência separadamente.","Observações sobre plataformas devem registrar rota e data."],
"on-device-photo-processing-privacy":["Regras de treinamento e retenção variam por serviço, conta, configuração e data.","Confira a política oficial atual do serviço exato que você usa.","Pergunte primeiro se a foto realmente precisa sair do dispositivo."],
},
"fr": {
"can-you-tell-if-a-photo-was-edited":["Commencez par l’état du fichier, pas par un verdict « retouchée/non retouchée ».","Croisez métadonnées, compression, géométrie, signaux et provenance.","Séparez observation, interprétation et ce qui peut réellement être prouvé."],
"image-metadata":["Identifiez le conteneur de métadonnées avant d’interpréter une valeur.","Une déclaration de logiciel ou de workflow donne du contexte, pas un historique complet.","L’absence de métadonnées reste elle aussi ambiguë."],
"invisible-watermark":["Un filigrane invisible est un signal d’image, pas un EXIF caché.","Détection et récupération de charge utile sont deux tâches différentes.","Tout chiffre de robustesse doit être accompagné de ses conditions de test."],
"photo-privacy-before-sharing":["Vérifiez à la fois les détails visibles et les informations du fichier.","Décidez si le destinataire a besoin de l’original ou d’une copie de partage.","Prenez la décision de confidentialité avant l’envoi."],
"what-happens-when-you-share-a-photo":["Une image visuellement identique peut être un fichier numérique différent.","Comparez séparément structure, métadonnées, pixels/signaux et provenance.","Toute observation de plateforme doit préciser le parcours et la date."],
"on-device-photo-processing-privacy":["Les règles d’entraînement et de conservation varient selon le service, le compte, les réglages et la date.","Consultez la politique officielle actuelle du service précis que vous utilisez.","Demandez d’abord si la photo doit réellement quitter l’appareil."],
},
"de": {
"can-you-tell-if-a-photo-was-edited":["Beginnen Sie mit dem Dateizustand statt mit einem Urteil „bearbeitet/unbearbeitet“.","Betrachten Sie Metadaten, Kompression, Geometrie, Signale und Provenienz zusammen.","Trennen Sie Beobachtung, Interpretation und tatsächlich belegbare Aussagen."],
"image-metadata":["Bestimmen Sie zuerst den Metadaten-Container, bevor Sie einen Wert deuten.","Software- oder Workflow-Angaben liefern Kontext, aber keine vollständige Historie.","Auch fehlende Metadaten sind mehrdeutig."],
"invisible-watermark":["Ein unsichtbares Wasserzeichen ist ein Bildsignal, kein verstecktes EXIF.","Detektion und Payload-Wiederherstellung sind unterschiedliche Aufgaben.","Robustheitswerte brauchen immer die genauen Testbedingungen."],
"photo-privacy-before-sharing":["Prüfen Sie sowohl sichtbare Details als auch Dateiinformationen.","Entscheiden Sie, ob das Original nötig ist oder eine Freigabekopie genügt.","Treffen Sie die Datenschutzentscheidung vor dem Upload."],
"what-happens-when-you-share-a-photo":["Ein optisch gleiches Bild kann eine andere digitale Datei sein.","Vergleichen Sie Dateistruktur, Metadaten, Pixel/Signale und Provenienz getrennt.","Plattformbeobachtungen sollten Route und Datum nennen."],
"on-device-photo-processing-privacy":["Regeln zu Training und Speicherung ändern sich je nach Dienst, Konto, Einstellung und Zeitpunkt.","Prüfen Sie die aktuelle offizielle Richtlinie des konkret genutzten Dienstes.","Fragen Sie zuerst, ob das Foto das Gerät überhaupt verlassen muss."],
},
}

NEXT = {
"can-you-tell-if-a-photo-was-edited":["image-metadata","what-happens-when-you-share-a-photo"],
"image-metadata":["can-you-tell-if-a-photo-was-edited","what-happens-when-you-share-a-photo"],
"invisible-watermark":["what-happens-when-you-share-a-photo","can-you-tell-if-a-photo-was-edited"],
"photo-privacy-before-sharing":["on-device-photo-processing-privacy","what-happens-when-you-share-a-photo"],
"what-happens-when-you-share-a-photo":["invisible-watermark","image-metadata"],
"on-device-photo-processing-privacy":["photo-privacy-before-sharing","can-you-tell-if-a-photo-was-edited"],
}

DEST_DESC = {
"en":{"image-metadata":"See what metadata can reveal and where its limits begin.","what-happens-when-you-share-a-photo":"Follow the file through resizing, recompression, screenshots and other sharing transformations.","can-you-tell-if-a-photo-was-edited":"Combine several evidence layers instead of relying on one clue.","invisible-watermark":"Understand the signal engineering behind survival and failure.","photo-privacy-before-sharing":"Run a practical privacy check before the file leaves your device.","on-device-photo-processing-privacy":"Understand what changes when photo processing stays local."},
"ko":{"image-metadata":"메타데이터가 무엇을 알려주고 어디서 한계가 시작되는지 확인합니다.","what-happens-when-you-share-a-photo":"리사이즈·재압축·스크린샷 등 공유 과정에서 파일이 어떻게 달라질 수 있는지 봅니다.","can-you-tell-if-a-photo-was-edited":"한 가지 단서가 아니라 여러 증거 층을 함께 해석하는 방법을 봅니다.","invisible-watermark":"보이지 않는 신호가 살아남거나 실패하는 기술적 이유를 이해합니다.","photo-privacy-before-sharing":"사진이 기기 밖으로 나가기 전에 개인정보를 점검합니다.","on-device-photo-processing-privacy":"사진 처리를 로컬에 두면 무엇이 달라지는지 확인합니다."},
"ja":{"image-metadata":"メタデータが何を示し、どこから限界が始まるかを確認します。","what-happens-when-you-share-a-photo":"リサイズ、再圧縮、スクリーンショットなど共有時の変化を追います。","can-you-tell-if-a-photo-was-edited":"一つの手掛かりではなく複数の証拠レイヤーを組み合わせます。","invisible-watermark":"不可視信号が残る・失われる技術的な理由を理解します。","photo-privacy-before-sharing":"写真が端末を離れる前にプライバシーを確認します。","on-device-photo-processing-privacy":"写真処理を端末内に保つと何が変わるかを確認します。"},
"zh-hans":{"image-metadata":"看看元数据能说明什么，以及它的边界在哪里。","what-happens-when-you-share-a-photo":"跟踪缩放、重压缩、截图等分享过程对文件的影响。","can-you-tell-if-a-photo-was-edited":"不要依赖单一线索，而是组合多个证据层。","invisible-watermark":"理解不可见信号为什么能保留、又为什么会失效。","photo-privacy-before-sharing":"在文件离开设备之前做一次实际的隐私检查。","on-device-photo-processing-privacy":"了解把照片处理留在设备端会改变什么。"},
"es":{"image-metadata":"Mira qué puede revelar un metadato y dónde empiezan sus límites.","what-happens-when-you-share-a-photo":"Sigue el archivo a través de redimensionado, recompresión, capturas y otras transformaciones.","can-you-tell-if-a-photo-was-edited":"Combina varias capas de evidencia en vez de depender de una sola pista.","invisible-watermark":"Entiende por qué una señal invisible puede sobrevivir o fallar.","photo-privacy-before-sharing":"Haz una revisión práctica de privacidad antes de que el archivo salga del dispositivo.","on-device-photo-processing-privacy":"Entiende qué cambia cuando el procesamiento de la foto se mantiene local."},
"pt-br":{"image-metadata":"Veja o que os metadados podem revelar e onde começam os limites.","what-happens-when-you-share-a-photo":"Acompanhe o arquivo por redimensionamento, recompressão, capturas de tela e outras transformações.","can-you-tell-if-a-photo-was-edited":"Combine várias camadas de evidência em vez de depender de uma única pista.","invisible-watermark":"Entenda por que um sinal invisível pode sobreviver ou falhar.","photo-privacy-before-sharing":"Faça uma revisão prática de privacidade antes de o arquivo sair do dispositivo.","on-device-photo-processing-privacy":"Entenda o que muda quando o processamento da foto permanece local."},
"fr":{"image-metadata":"Voyez ce que les métadonnées peuvent révéler et où commencent leurs limites.","what-happens-when-you-share-a-photo":"Suivez le fichier à travers redimensionnement, recompression, captures d’écran et autres transformations.","can-you-tell-if-a-photo-was-edited":"Croisez plusieurs couches d’indices plutôt que de dépendre d’un seul signal.","invisible-watermark":"Comprenez pourquoi un signal invisible peut survivre ou échouer.","photo-privacy-before-sharing":"Faites un contrôle de confidentialité avant que le fichier ne quitte l’appareil.","on-device-photo-processing-privacy":"Voyez ce qui change lorsque le traitement de la photo reste local."},
"de":{"image-metadata":"Sehen Sie, was Metadaten zeigen können und wo ihre Grenzen beginnen.","what-happens-when-you-share-a-photo":"Verfolgen Sie die Datei durch Größenänderung, Neukompression, Screenshots und weitere Transformationen.","can-you-tell-if-a-photo-was-edited":"Kombinieren Sie mehrere Evidenzebenen statt nur einem Hinweis zu vertrauen.","invisible-watermark":"Verstehen Sie, warum ein unsichtbares Signal bestehen oder ausfallen kann.","photo-privacy-before-sharing":"Prüfen Sie die Privatsphäre, bevor die Datei das Gerät verlässt.","on-device-photo-processing-privacy":"Verstehen Sie, was sich ändert, wenn die Fotoverarbeitung lokal bleibt."},
}

def path_for(locale, slug):
    prefix = LOCALES[locale]
    return Path(prefix) / "articles" / slug / "index.html" if prefix else Path("articles") / slug / "index.html"

def href_for(locale, slug):
    prefix = LOCALES[locale]
    return f"/{prefix}/articles/{slug}/" if prefix else f"/articles/{slug}/"

def title_of(locale, slug):
    text = path_for(locale, slug).read_text(encoding="utf-8")
    m = re.search(r"<h1>(.*?)</h1>", text, re.S)
    return re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else slug.replace("-", " ").title()

def summary_block(locale, slug):
    u = UI[locale]
    lis = "".join(f"<li>{x}</li>" for x in SUMMARY[locale][slug])
    return f'<div class="article-summary"><strong>{u["summary"]}</strong><ul>{lis}</ul></div>'

def product_block(locale, slug):
    u = UI[locale]
    home = f'/{LOCALES[locale]}/' if LOCALES[locale] else '/'
    return (f'<div class="micro-cta"><strong>{u["product"]}</strong>'
            f'<p>{u["product_body"]}</p>'
            f'<a href="{home}" data-umami-event="article-product-interest" data-umami-event-source="article" '
            f'data-umami-event-placement="mid-article" data-umami-event-locale="{locale}" data-umami-event-article="{slug}">{u["product_link"]}</a></div>')

def next_block(locale, slug):
    u = UI[locale]
    cards=[]
    for i,dest in enumerate(NEXT[slug]):
        label = u["next"] if i == 0 else u["then"]
        cards.append(f'<a class="next-card" href="{href_for(locale,dest)}" data-umami-event="article-next-click" '
                     f'data-umami-event-locale="{locale}" data-umami-event-article="{slug}" data-umami-event-next="{dest}">'
                     f'<span class="next-label">{label}</span><strong>{title_of(locale,dest)}</strong><span>{DEST_DESC[locale][dest]}</span></a>')
    return f'<section class="next-reads"><h2>{u["continue"]}</h2><div class="next-grid">{"".join(cards)}</div></section>'

def insert_after_nth_paragraph(text, start, block, n=4):
    pos=start
    for _ in range(n):
        pos=text.find("</p>", pos)
        if pos < 0: return text
        pos += 4
    return text[:pos] + block + text[pos:]

def add_ai_policy_protocol(text):
    if 'class="policy-check-protocol"' in text:
        return text
    marker='<div class="article-body">'
    start=text.find(marker)
    if start<0: return text
    insert_at=start+len(marker)
    summary=summary_block("en","on-device-photo-processing-privacy")
    protocol='''<div class="policy-check-protocol"><h2>How to check an AI photo service without relying on rumors</h2><p>A useful policy answer has at least four coordinates: <strong>which product, which account type, which setting and which date</strong>. “Company X trains on photos” is usually too broad to be dependable.</p><div class="protocol"><div class="protocol-step"><div class="num">1</div><div><strong>Name the exact service surface</strong><p>Consumer chat, image editor, API and business product can have different defaults.</p></div></div><div class="protocol-step"><div class="num">2</div><div><strong>Read the current first-party policy</strong><p>Prefer the provider’s privacy/help documentation over screenshots or second-hand summaries.</p></div></div><div class="protocol-step"><div class="num">3</div><div><strong>Check your setting</strong><p>Model-improvement, activity-history and privacy controls can change how submitted content is handled.</p></div></div><div class="protocol-step"><div class="num">4</div><div><strong>Look beyond training</strong><p>Retention, human review, subprocessors and deletion controls are separate questions.</p></div></div><div class="protocol-step"><div class="num">5</div><div><strong>Record the date</strong><p>Policies change. A responsible article tells readers when the policy was checked instead of presenting it as timeless.</p></div></div></div><div class="lab-note"><span class="lab-label">PRIVACY READING RULE</span><h3>“May be used” and “always used” are not the same statement.</h3><p>The safest comparison keeps the provider’s exact scope and settings visible. SIGNA’s local-first point is narrower: when a supported photo operation can be done on the device, that operation does not require an extra image upload to SIGNA AI Lab.</p></div></div>'''
    return text[:insert_at]+summary+protocol+text[insert_at:]

def process(locale, slug):
    p=path_for(locale,slug)
    if not p.exists(): return False
    text=p.read_text(encoding="utf-8")
    original=text
    # English five core articles are already deeply rewritten by hand.
    if locale == "en" and slug != "on-device-photo-processing-privacy":
        return False
    text=re.sub(r'"dateModified":"\d{4}-\d{2}-\d{2}"', f'"dateModified":"{DATE}"', text, count=1)
    if locale == "en" and slug == "on-device-photo-processing-privacy":
        text=add_ai_policy_protocol(text)
    elif 'class="article-summary"' not in text:
        marker='<div class="article-body">'
        text=text.replace(marker, marker+summary_block(locale,slug), 1)
    if 'data-umami-event="article-product-interest"' not in text:
        start=text.find('<div class="article-body">')
        if start>=0:
            text=insert_after_nth_paragraph(text,start,product_block(locale,slug),4)
    if 'class="next-reads"' not in text:
        nb=next_block(locale,slug)
        anchor='<section class="refs">'
        if anchor in text:
            text=text.replace(anchor, nb+anchor, 1)
        elif '<section class="article-cta">' in text:
            text=text.replace('<section class="article-cta">', nb+'<section class="article-cta">', 1)
        else:
            back='<a class="back-articles"'
            idx=text.find(back)
            if idx>=0: text=text[:idx]+nb+text[idx:]
    if text != original:
        p.write_text(text, encoding="utf-8")
        return True
    return False

def validate():
    count=0
    for locale in LOCALES:
        for slug in SLUGS:
            p=path_for(locale,slug)
            t=p.read_text(encoding="utf-8")
            assert t.count('<h1') == 1, p
            assert '<html' in t and '</html>' in t, p
            assert 'class="next-reads"' in t, p
            assert 'article-next-click' in t, p
            assert 'google-play-click' in t, p
            assert 'data-website-id=' in t, p
            count += 1
    print(f"validated {count} article pages")

changed=[]
for locale in LOCALES:
    for slug in SLUGS:
        if process(locale,slug): changed.append(str(path_for(locale,slug)))
validate()
print(f"changed {len(changed)} pages")
for p in changed: print(p)
