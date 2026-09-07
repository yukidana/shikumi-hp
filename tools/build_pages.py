# -*- coding: utf-8 -*-
"""サービス・助成金・コラムページ生成スクリプト
使い方: python3 tools/build_pages.py （リポジトリルートで実行）
ページ追加時は PAGES に関数を足し、build_area.py の EXTRA_URLS にパスを追加して
build_area.py も再実行（sitemap更新）。
"""
import os, json
from build_area import head, footer, mailto, esc, BASE, ROOT, CASES

TODAY = "2026-09-06"


# ---------------------------------------------------------------- 汎用部品
def ld_breadcrumb(items):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": u}
            for i, (n, u) in enumerate(items)
        ],
    }


def ld_faq(faqs):
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    }


def ld_article(title, desc, url):
    return {
        "@type": "Article",
        "headline": title,
        "description": desc,
        "datePublished": TODAY,
        "dateModified": TODAY,
        "author": {"@type": "Organization", "name": "株式会社シクミ", "url": BASE + "/"},
        "publisher": {"@type": "Organization", "name": "株式会社シクミ"},
        "mainEntityOfPage": url,
    }


def graph(*nodes):
    return json.dumps({"@context": "https://schema.org", "@graph": list(nodes)}, ensure_ascii=False)


def faq_html(faqs):
    return '<div class="faqs">' + "".join(
        f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faqs
    ) + "</div>"


def crumbs(items):
    parts = [f'<a href="{u}">{esc(n)}</a>' for n, u in items[:-1]] + [f"<span>{esc(items[-1][0])}</span>"]
    return f'<nav class="crumbs" aria-label="パンくず">{" › ".join(parts)}</nav>'


def cta_block(subject, msg):
    return f"""
<section class="cta-box">
  <p class="eyebrow">CONTACT</p>
  <h2>まずは、無料の簡易診断から</h2>
  <p>{esc(msg)}</p>
  <a class="btn-main" href="{mailto(subject)}">無料簡易診断を申し込む →</a>
  <p class="cta-mail">メール: info@shikumi-co.jp（1営業日以内にご返信します）</p>
</section>
"""


def rel_cards(items):
    cards = "".join(
        f'<a class="card ward-card" href="{u}"><h3>{esc(t)}</h3><p>{esc(d)}</p><span class="more">読む →</span></a>'
        for t, d, u in items
    )
    return f'<div class="rel-cards">{cards}</div>'


def case_cards():
    return '<div class="grid2">' + "".join(
        f'<div class="card case"><h3>{esc(t)}</h3><p class="s-meta">{esc(sz)}</p><p><b>課題:</b> {esc(c)}</p><p><b>支援:</b> {esc(s)}</p><p class="result">{esc(r)}</p><p class="s-meta">{esc(m)}</p></div>'
        for t, sz, c, s, r, m in CASES
    ) + "</div>"


def write_page(path, html):
    outdir = os.path.join(ROOT, path.strip("/"))
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


# ================================================================ /subsidy/
def page_subsidy():
    path = "/subsidy/"
    url = BASE + path
    title = "AI研修に使える助成金【2026年度が最終】実質負担を1/4以下にする方法｜株式会社シクミ"
    desc = "AI研修・生成AI研修に使える助成金は人材開発支援助成金「事業展開等リスキリング支援コース」。中小企業は経費助成75%＋賃金助成1,000円/時で、実質負担は約1/4に。負担額シミュレーターと申請の流れを解説。2026年度（令和8年度）が最終年度です。"
    faqs = [
        ("AI研修の助成金はいつまで使えますか？", "事業展開等リスキリング支援コースは令和8年度（2027年3月末）までの時限措置で、2026年度が最終年度です。令和9年度以降の継続は未定のため、活用するなら年度内の訓練開始が確実です。訓練開始の1ヶ月前までに計画届の提出が必要な点にご注意ください。"),
        ("いくら戻ってきますか？", "中小企業の場合、経費助成75%（上限あり）に加えて、訓練中の賃金助成が1人1時間あたり1,000円支給されます。例えば5名が10時間の研修（受講料計150万円）を受けると、実質負担は約32.5万円です。"),
        ("「AI研修助成金」という制度があるのですか？", "いいえ。「AI研修専用の助成金」は存在せず、実務上は厚生労働省の人材開発支援助成金（主に事業展開等リスキリング支援コース）を指します。助成対象になるかは研修名ではなく、訓練の目的・内容・実施方法で判定されます。"),
        ("eラーニングでも対象になりますか？", "対象になり得ますが、eラーニング等は経費助成の上限が別に定められています（2026年度改正で1人あたり上限15万円）。対面・オンライン（同時双方向）形式の研修の方が上限に余裕があります。"),
        ("申請手続きは代行してもらえますか？", "支給申請の代行は社会保険労務士の業務領域のため当社では行いませんが、申請に必要なカリキュラム・時間数・実施記録などの書類はすべて当社がご用意し、手続きの流れも伴走します。顧問社労士がいない場合はご紹介も可能です。"),
    ]
    ld = graph(
        ld_article(title, desc, url),
        ld_breadcrumb([("株式会社シクミ", BASE + "/"), ("AI研修に使える助成金", url)]),
        ld_faq(faqs),
    )
    body = f"""<main class="article">
{crumbs([("トップ", "/"), ("AI研修に使える助成金", url)])}
<div class="hero">
  <p class="eyebrow">SUBSIDY GUIDE</p>
  <h1>AI研修に使える助成金<br class="sp">——実質負担を1/4以下にする方法</h1>
  <p class="meta-line">更新日 {TODAY} ／ 株式会社シクミ</p>
  <p class="lead">社員にAI研修を受けさせたいが、費用がネックになっている——その場合に必ず確認すべきなのが、厚生労働省の<b>人材開発支援助成金「事業展開等リスキリング支援コース」</b>です。このページでは、いくら戻るのかを試算できるシミュレーターと、申請の流れ・注意点をまとめました。</p>
</div>

<div class="conclusion">
  <p class="c-label">CONCLUSION</p>
  <p><b>結論:</b> AI研修に使える助成金は、実務上ほぼ「人材開発支援助成金（事業展開等リスキリング支援コース）」の一択です。中小企業なら<b>経費助成75%＋賃金助成1,000円/時</b>。ただしこのコースは<b>2026年度（令和8年度）が最終年度</b>で、令和9年度以降の継続は未定。訓練開始の<b>1ヶ月前まで</b>に計画届の提出が必要なため、検討は早いほど有利です。</p>
</div>

<section>
  <p class="eyebrow">SIMULATOR</p>
  <h2>負担額シミュレーター</h2>
  <p>当社のAI研修（30万円/名・10時間カリキュラム）を例に、実質負担額を試算できます。</p>
  <div class="sim" id="sim">
    <div class="sim-row">
      <label>企業規模</label>
      <span class="seg" role="group" aria-label="企業規模">
        <button type="button" id="btnChusho" class="on">中小企業</button><button type="button" id="btnDai">大企業</button>
      </span>
      <label for="simN">受講人数</label>
      <input type="number" id="simN" value="5" min="1" max="50"> 名
    </div>
    <div class="sim-out">
      <div class="o-row"><span>受講料総額（30万円 × 人数）</span><span id="oTotal">—</span></div>
      <div class="o-row"><span>経費助成（<span id="oRate">75</span>%）</span><span id="oKeihi">—</span></div>
      <div class="o-row"><span>賃金助成（<span id="oWage">1,000</span>円/時 × 10時間 × 人数）</span><span id="oChin">—</span></div>
      <div class="o-row total"><span>実質ご負担</span><b id="oJitsu">—</b></div>
    </div>
    <p class="fine">※ 経費助成の1人あたり上限（10時間以上100時間未満: 中小企業30万円・大企業20万円）を考慮した概算です。受給可否・金額は労働局の審査・申請結果により変動します。正式な金額は最新の支給要領・管轄労働局にご確認ください。</p>
  </div>
</section>

<section>
  <p class="eyebrow">ABOUT</p>
  <h2>制度の概要——事業展開等リスキリング支援コース</h2>
  <p>新規事業の立ち上げやDX化（デジタル・トランスフォーメーション）に伴い、新たな分野で必要となる知識・技能を習得させる訓練を支援するコースです。<b>生成AIの業務活用研修は、まさにこの「DX化に伴う人材育成」の典型例</b>として活用されています。</p>
  <div class="tbl-wrap"><table class="tbl">
    <thead><tr><th>項目</th><th>中小企業</th><th>大企業</th></tr></thead>
    <tbody>
      <tr class="hl"><td>経費助成率</td><td><b>75%</b></td><td>60%</td></tr>
      <tr><td>賃金助成（1人1時間あたり）</td><td><b>1,000円</b></td><td>500円</td></tr>
      <tr><td>経費助成の上限（1人あたり・10h以上100h未満）</td><td>30万円</td><td>20万円</td></tr>
      <tr><td>主な要件</td><td colspan="2">OFF-JT（業務を離れた訓練）10時間以上／事業展開・DX化等との関連／訓練開始1ヶ月前までの計画届提出</td></tr>
      <tr><td>実施期限</td><td colspan="2"><b>令和8年度（2027年3月末）まで</b>の時限措置。令和9年度以降は未定</td></tr>
    </tbody>
  </table></div>
  <div class="warn"><p><b>2026年度の改正点:</b> 設備投資加算（訓練に関連する設備導入費用の50%・上限150万円）が新設された一方、eラーニング等の経費助成上限は1人あたり15万円に見直されました。対面・同時双方向型の研修の方が助成枠を活かしやすくなっています。</p></div>
</section>

<section>
  <p class="eyebrow">FLOW</p>
  <h2>申請の流れ（5ステップ）</h2>
  <div class="flow">
    <div class="f-step"><h3>事業展開等実施計画・訓練実施計画届の作成</h3><p>「どんな事業展開・DX化のために、誰に、何を学ばせるか」を計画書にまとめます。研修カリキュラム・時間数は当社がご用意します。</p></div>
    <div class="f-step"><h3>訓練開始1ヶ月前までに労働局へ提出</h3><p>管轄の労働局（ハローワーク経由の場合あり）へ計画届を提出。余裕を持って<b>2ヶ月前のご相談</b>をおすすめしています。</p></div>
    <div class="f-step"><h3>研修の実施</h3><p>計画どおりに研修を実施し、出席記録・実施記録を残します（記録類は当社がフォーマットを提供）。</p></div>
    <div class="f-step"><h3>支給申請（訓練終了後2ヶ月以内）</h3><p>経費の支払い証憑・賃金台帳などを添えて支給申請します。</p></div>
    <div class="f-step"><h3>審査・受給</h3><p>労働局の審査を経て助成金が支給されます。</p></div>
  </div>
</section>

<section>
  <p class="eyebrow">SHIKUMI</p>
  <h2>シクミのAI研修は、助成金活用を前提に設計されています</h2>
  <ul>
    <li><b>10時間カリキュラム（4回×2.5時間）</b>——OFF-JT10時間以上の要件を満たす構成</li>
    <li><b>教材は「構築済みの貴社の業務フロー」</b>——一般論のAI講座ではなく、自社業務に直結した内容（事業展開・DX化との関連を示しやすい）</li>
    <li><b>申請書類のサポート</b>——カリキュラム・時間割・実施記録など、申請に必要な研修側の書類はすべて当社が用意</li>
  </ul>
  <p>研修の詳細は <a href="/service/training/">法人向けAI研修のページ</a> をご覧ください。</p>
</section>

<section>
  <p class="eyebrow">RELATED</p>
  <h2>AI「導入」の費用に使える補助金</h2>
  <p>研修（人への投資）は上記の助成金ですが、AIツールやシステムの<b>導入費用</b>には別の補助金が対応します。代表的なものは以下の通りです。</p>
  <div class="tbl-wrap"><table class="tbl">
    <thead><tr><th>制度</th><th>対象</th><th>ポイント</th></tr></thead>
    <tbody>
      <tr><td>IT導入補助金</td><td>ITツール・ソフトウェアの導入費</td><td>登録済みツールが対象。生成AI関連ツールの枠も拡充傾向</td></tr>
      <tr><td>ものづくり補助金</td><td>革新的な設備・システム投資</td><td>製造業のAI活用投資などで活用例</td></tr>
      <tr><td>中小企業省力化投資補助金</td><td>人手不足解消のための省力化投資</td><td>カタログ型で使いやすい</td></tr>
    </tbody>
  </table></div>
  <p>どの制度が使えるかは事業内容・投資内容によります。無料簡易診断の際に、活用できそうな制度もあわせてご案内しています。</p>
</section>

<section>
  <p class="eyebrow">FAQ</p>
  <h2>よくあるご質問</h2>
  {faq_html(faqs)}
  <p class="s-meta" style="margin-top:14px">※ 本ページは2026年9月時点の公開情報に基づく解説です。制度内容は改正される場合があるため、最新情報は厚生労働省の公式資料・管轄労働局でご確認ください。</p>
</section>

{cta_block("無料簡易診断の申込（助成金ページ）", "オンライン・約2時間で、貴社のAI化の期待効果と、活用できる助成金の目安をご提示します。助成金は訓練開始1ヶ月前までの申請が必要です。お早めにご相談ください。")}
</main>
<script>
(function(){{
  var chusho=true;
  var bC=document.getElementById('btnChusho'),bD=document.getElementById('btnDai'),n=document.getElementById('simN');
  function yen(v){{return v.toLocaleString('ja-JP')+'円'}}
  function calc(){{
    var num=Math.max(1,Math.min(50,parseInt(n.value||'1',10)));
    var price=300000,hours=10;
    var rate=chusho?0.75:0.6,cap=chusho?300000:200000,wage=chusho?1000:500;
    var total=price*num;
    var keihi=Math.min(price*rate,cap)*num;
    var chin=wage*hours*num;
    var jitsu=Math.max(0,total-keihi-chin);
    document.getElementById('oTotal').textContent=yen(total);
    document.getElementById('oKeihi').textContent='▲ '+yen(keihi);
    document.getElementById('oChin').textContent='▲ '+yen(chin);
    document.getElementById('oJitsu').textContent=yen(jitsu);
    document.getElementById('oRate').textContent=chusho?'75':'60';
    document.getElementById('oWage').textContent=chusho?'1,000':'500';
  }}
  bC.addEventListener('click',function(){{chusho=true;bC.classList.add('on');bD.classList.remove('on');calc()}});
  bD.addEventListener('click',function(){{chusho=false;bD.classList.add('on');bC.classList.remove('on');calc()}});
  n.addEventListener('input',calc);
  calc();
}})();
</script>
"""
    write_page(path, head(title, desc, url, ld) + body + footer())


# ================================================================ /service/training/
def page_training():
    path = "/service/training/"
    url = BASE + path
    title = "法人向けAI研修｜自社業務が教材の10時間カリキュラム・助成金対応｜株式会社シクミ"
    desc = "非エンジニアの社員向けAI研修。教材は「構築済みの自社業務フロー」だから、翌日から仕事で使えます。4回×2.5時間の10時間カリキュラム・30万円/名。人材開発支援助成金対応で実質負担約1/4に。研修のみの単独依頼も可能。"
    faqs = [
        ("研修だけの依頼もできますか？", "できます。AI研修のみの単独依頼も承っています。その場合は貴社の既存業務に合わせて演習内容を設計します。駐在型AI化支援とセットの場合は、当社が構築した貴社の業務フローそのものを教材にするため、定着効果が最大になります。"),
        ("ITが苦手な社員ばかりでも大丈夫ですか？", "大丈夫です。対象は非エンジニアの方で、研修は「構築済みの自社業務フローの使い方・保守」に絞ります。代表の石井自身、文系出身・エンジニア未経験からAI活用を始めた実践者です。"),
        ("何名から実施できますか？", "1名から実施可能です。助成金の効果を考えると3〜10名程度でのご受講が多いです。"),
        ("オンラインでも受講できますか？", "対面・オンラインのどちらでも実施できます。ただしeラーニング（録画視聴型）ではなく同時双方向のライブ形式のため、助成金の経費助成上限を活かしやすい形式です。"),
        ("費用はいくらですか？助成金は使えますか？", "受講料は30万円/名（4回×2.5時間・計10時間）です。人材開発支援助成金「事業展開等リスキリング支援コース」の対象になる場合、中小企業なら実質負担は約1/4になります。詳しくは助成金ページをご覧ください。"),
    ]
    ld = graph(
        {
            "@type": "Service",
            "name": "法人向けAI研修",
            "provider": {"@type": "Organization", "name": "株式会社シクミ", "email": "info@shikumi-co.jp"},
            "serviceType": "AI研修・生成AI研修",
            "areaServed": "日本",
            "url": url,
            "description": desc,
        },
        ld_breadcrumb([("株式会社シクミ", BASE + "/"), ("法人向けAI研修", url)]),
        ld_faq(faqs),
    )
    body = f"""<main class="article">
{crumbs([("トップ", "/"), ("法人向けAI研修", url)])}
<div class="hero">
  <p class="eyebrow">AI TRAINING</p>
  <h1>法人向けAI研修<br class="sp">——教材は、貴社の業務そのもの</h1>
  <p class="lead">一般論のAI講座を受けても、翌日の仕事は変わりません。シクミのAI研修は<b>「構築済みの自社業務フロー」を教材</b>にするから、研修が終わった瞬間から現場で使えます。非エンジニアの社員さまが対象。人材開発支援助成金に対応した10時間カリキュラムです。</p>
  <a class="btn-main" href="{mailto('AI研修の相談')}">研修について相談する →</a>
  <p class="hero-meta">4回×2.5時間＝10時間／対面 or オンライン／研修のみの単独依頼も可能</p>
</div>

<section>
  <p class="eyebrow">FEATURES</p>
  <h2>選ばれる3つの理由</h2>
  <div class="three">
    <div class="card"><h3>自社業務が教材</h3><p>ChatGPTの一般的な使い方ではなく、貴社の実際の業務フロー・帳票・ルールを教材に演習。学んだことがそのまま月曜の仕事になります。</p></div>
    <div class="card"><h3>非エンジニア対象</h3><p>プログラミング知識は不要。「安全に・正しく・日常的に」使えることをゴールに設計しています。</p></div>
    <div class="card"><h3>助成金対応の設計</h3><p>OFF-JT10時間以上・カリキュラム明示・実施記録の提供など、人材開発支援助成金の活用を前提に設計。実質負担は約1/4になる場合も。</p></div>
  </div>
</section>

<section>
  <p class="eyebrow">CURRICULUM</p>
  <h2>カリキュラム（4回×2.5時間＝10時間）</h2>
  <div class="tbl-wrap"><table class="tbl">
    <thead><tr><th>回</th><th>テーマ</th><th>主な内容</th></tr></thead>
    <tbody>
      <tr><td>第1回</td><td><b>初期セットアップ編</b></td><td>アカウント・環境の整備／法人利用の設定（学習利用オフ等）／基本操作</td></tr>
      <tr><td>第2回</td><td><b>安全運用編</b></td><td>機密情報の扱い方／社内ルールづくり／やってはいけないことの線引き</td></tr>
      <tr><td>第3回</td><td><b>実務活用編</b></td><td>文書作成・要約・調査など日常業務での活用演習（自社の実データ形式で）</td></tr>
      <tr><td>第4回</td><td><b>自社適用編</b></td><td>構築済みの自社業務フローの操作・保守／改善アイデアの出し方</td></tr>
    </tbody>
  </table></div>
  <p class="s-meta">※ 単独依頼の場合、第4回は貴社の既存業務に合わせた適用演習に置き換えます。経営者向けセミナー形式のご依頼も承ります。</p>
</section>

<section>
  <p class="eyebrow">PRICE</p>
  <h2>料金と助成金</h2>
  <div class="grid2">
    <div class="card"><p class="k-label">PRICE</p><h3>受講料</h3><p class="s-price">30万円/名</p><p>4回×2.5時間・計10時間。対面またはオンライン（同時双方向）。</p></div>
    <div class="card"><p class="k-label">SUBSIDY</p><h3>助成金活用時（中小企業）</h3><p class="s-price">実質 約7.5万円/名〜</p><p>経費助成75%＋賃金助成1,000円/時。例: 5名受講・総額150万円→実質約32.5万円。</p></div>
  </div>
  <p><a href="/subsidy/">→ 助成金の詳細と負担額シミュレーターはこちら</a>（2026年度が最終年度です）</p>
</section>

<section>
  <p class="eyebrow">FLOW</p>
  <h2>ご依頼の流れ</h2>
  <div class="flow">
    <div class="f-step"><h3>無料相談（オンライン）</h3><p>目的・対象者・人数を伺い、カリキュラムと助成金活用の可否をご案内します。</p></div>
    <div class="f-step"><h3>助成金の計画届提出（活用する場合）</h3><p>訓練開始1ヶ月前までに労働局へ。書類は当社がサポートします。</p></div>
    <div class="f-step"><h3>研修実施（4回×2.5時間）</h3><p>週1回×4週などご都合に合わせて日程を設計します。</p></div>
    <div class="f-step"><h3>実施記録のお渡し・支給申請</h3><p>出席・実施記録をお渡しし、助成金の支給申請へ。</p></div>
  </div>
</section>

<section>
  <p class="eyebrow">FAQ</p>
  <h2>よくあるご質問</h2>
  {faq_html(faqs)}
</section>

<section>
  <p class="eyebrow">RELATED</p>
  <h2>あわせて読む</h2>
  {rel_cards([
    ("AI研修に使える助成金", "経費75%助成の制度解説と負担額シミュレーター。2026年度が最終年度。", "/subsidy/"),
    ("生成AI導入支援（駐在型AIコンサル）", "研修の前に「使える仕組み」を作る。実装から内製化までの本体サービス。", "/service/consulting/"),
  ])}
</section>

{cta_block("AI研修の相談", "オンライン・約2時間の無料簡易診断で、貴社に合う研修設計と助成金活用の目安をご提示します。研修のみのご相談も歓迎です。")}
</main>
"""
    write_page(path, head(title, desc, url, ld) + body + footer())


# ================================================================ /service/consulting/
def page_consulting():
    path = "/service/consulting/"
    url = BASE + path
    title = "生成AI導入支援・駐在型AIコンサルティング｜実装から内製化まで｜株式会社シクミ"
    desc = "生成AIの導入支援なら駐在型の株式会社シクミ。AI人材が現場に入り、業務ヒアリングから実装・内製化まで一気通貫。提案書で終わるコンサルでも、ツールを売るベンダーでもありません。無料簡易診断（オンライン2時間）受付中。"
    faqs = [
        ("一般的なAIコンサルと何が違うのですか？", "一般的なコンサルは提案書・レポートの納品が中心で、手を動かすのは貴社側です。当社は現場に駐在し、当社のコンサルタント自身が実装まで実行します。ツールベンダーとも異なり、特定製品に縛られず、不要なツールの解約提案まで行う中立の立場です。"),
        ("費用はどのくらいかかりますか？", "無料簡易診断（0円）→実地調査50〜150万円→駐在型支援は月60時間稼働で参考100万円/月（3〜6ヶ月）→AI研修30万円/名です。各ステップの節目で「次に進むか」をご判断いただけます。納品後のサブスクリプション費用はありません。"),
        ("どんな業種・規模の会社が対象ですか？", "従業員10〜500名規模の企業を中心に、業種は問いません。書類・転記・例外処理の多い業務であれば、業種を問わず同じ型でAI化できます。不動産・製造業などの実績・提案例があります。"),
        ("対応エリアは？", "全国対応です。遠方の場合は交通費実費を別途申し受けます。東京都内は渋谷オフィスから直接伺います。"),
        ("機密情報の扱いが不安です。", "秘密保持契約（NDA）を締結の上、データは業務目的の範囲でのみ扱います。AIツールは入力データが学習に利用されない法人向けプラン・設定を前提に、貴社のセキュリティ方針に合わせて構成します。"),
        ("効果が出なかったら？途中でやめられますか？", "契約は月単位の準委任です。無料診断・実地調査の各段階で「次に進むか」をご判断いただけます。支援途中の見直し・中断もご相談ください。"),
    ]
    ld = graph(
        {
            "@type": "Service",
            "name": "生成AI導入支援・駐在型AIコンサルティング",
            "provider": {"@type": "Organization", "name": "株式会社シクミ", "email": "info@shikumi-co.jp",
                         "address": {"@type": "PostalAddress", "addressRegion": "東京都", "addressLocality": "渋谷区", "streetAddress": "桜丘町18-4 二宮ビル1F"}},
            "serviceType": "生成AI導入支援・AIコンサルティング",
            "areaServed": "日本",
            "url": url,
            "description": desc,
        },
        ld_breadcrumb([("株式会社シクミ", BASE + "/"), ("生成AI導入支援・駐在型AIコンサルティング", url)]),
        ld_faq(faqs),
    )
    body = f"""<main class="article">
{crumbs([("トップ", "/"), ("生成AI導入支援・駐在型AIコンサルティング", url)])}
<div class="hero">
  <p class="eyebrow">AI CONSULTING</p>
  <h1>生成AI導入支援<br class="sp">——AI人材が現場に駐在し、業務を作り変える</h1>
  <p class="lead">ツールを入れても、業務は変わりません。変わるのは、<b>業務プロセスそのものを組み替えたとき</b>です。シクミの生成AI導入支援は、AIを使いこなすコンサルタントが貴社の現場に入り、部門を問わず業務を1から10までヒアリング。どこにAIが効くかを見極め、現場で手を動かしながら実装し、社員の皆さまが自走できる状態まで作り切ります。</p>
  <a class="btn-main" href="{mailto('無料簡易診断の申込')}">無料簡易診断を申し込む →</a>
  <p class="hero-meta">オンライン・約2時間・0円／全国対応（東京都内は渋谷オフィスから直接訪問）</p>
</div>

<section>
  <p class="eyebrow">PROBLEM</p>
  <h2>AI導入が、止まる理由</h2>
  <div class="grid2">
    <div class="card"><h3>ツールは入れた。でも、使われていない</h3><p>生成AIを契約したものの、一部の社員が時々使うだけ。業務そのものは何も変わっていない。</p></div>
    <div class="card"><h3>チャットと調べ物止まり</h3><p>質問・要約・下書きには使えている。しかし請求書処理や報告書づくりなど、日々の業務の流れはそのまま。</p></div>
    <div class="card"><h3>個人では使っているが、会社の仕組みになっていない</h3><p>各自がバラバラに使い、工夫はその人の画面の中だけ。その人が休むと止まる——AIの属人化。</p></div>
    <div class="card"><h3>何から始めればいいか分からない</h3><p>AI化したい気持ちはある。しかし自社業務のどこにAIが効くのか、社内の誰も答えられない。</p></div>
  </div>
  <div class="conclusion"><p class="c-label">WHY</p><p>共通の原因はAIの性能ではありません。<b>「業務を作り変える人」が現場にいないこと</b>です。だから私たちは、業務の作り変えにコミットするAI人材を、外から現場に入れます。</p></div>
</section>

<section>
  <p class="eyebrow">DIFFERENCE</p>
  <h2>従来の支援との違い</h2>
  <div class="tbl-wrap"><table class="tbl">
    <thead><tr><th></th><th>一般的なコンサル</th><th>ツール導入ベンダー</th><th class="hl">シクミ（駐在型）</th></tr></thead>
    <tbody>
      <tr><td><b>関わり方</b></td><td>提案書・レポート中心</td><td>ツールの納品・設定</td><td class="hl">現場に入り込み、実装まで自ら実行</td></tr>
      <tr><td><b>誰が手を動かすか</b></td><td>貴社（宿題形式が多い）</td><td>ベンダー（自社製品の範囲のみ）</td><td class="hl">弊社コンサルタントが現場で実装</td></tr>
      <tr><td><b>対象範囲</b></td><td>特定テーマのみ</td><td>自社ツールの範囲のみ</td><td class="hl">部門横断・業務全体（解約提案も）</td></tr>
      <tr><td><b>契約形態</b></td><td>顧問契約が継続</td><td>ライセンス＋保守費が継続</td><td class="hl">プロジェクト型（納品後のサブスクなし）</td></tr>
      <tr><td><b>ゴール</b></td><td>提言の納品</td><td>導入完了</td><td class="hl">内製化して「卒業」</td></tr>
    </tbody>
  </table></div>
</section>

<section>
  <p class="eyebrow">WHAT WE DO</p>
  <h2>現場で行うこと</h2>
  <div class="flow">
    <div class="f-step"><h3>業務ヒアリング</h3><p>現場の方から業務を1から10まですべてヒアリングし、業務の全体像と課題を棚卸しします。マニュアルに載らない例外運用こそが工数の正体です。</p></div>
    <div class="f-step"><h3>AI化ポイントの見極め</h3><p>どの業務に・どんな形でAIを導入するのが最適かを、費用対効果とともに設計します。</p></div>
    <div class="f-step"><h3>実装・業務フローの再構築</h3><p>現場で手を動かしながらAI化を実行。ツールの選定・導入から、既存ツールの解約・見直しまで含めて最適化します。</p></div>
    <div class="f-step"><h3>コスト・工数の削減を数字で報告</h3><p>作業工数やSaaS・外注などのコストを削減し、効果を数字でご報告します。</p></div>
  </div>
  <p class="s-meta">適用範囲: バックオフィス全般（契約・経理・総務・人事）／営業・カスタマーサポート／各事業部の定型業務</p>
</section>

<section>
  <p class="eyebrow">FLOW / PRICE</p>
  <h2>進め方と料金（STEP 0〜3）</h2>
  <p>各ステップの節目で「続けるか」をご判断いただけます。実地調査のみのご利用も可能です。</p>
  <div class="tbl-wrap"><table class="tbl">
    <thead><tr><th>ステップ</th><th>内容</th><th>期間・工数</th><th>料金</th></tr></thead>
    <tbody>
      <tr><td><b>STEP 0</b></td><td>無料簡易診断——業務概要を伺い、AI化の期待効果の目安をその場でご提示</td><td>オンライン・約2時間</td><td><b>0円</b></td></tr>
      <tr><td><b>STEP 1</b></td><td>実地調査（AI化アセスメント）——業務棚卸し・ロードマップ・削減効果試算の納品</td><td>30〜90時間・約1〜3ヶ月</td><td>50〜150万円</td></tr>
      <tr class="hl"><td><b>STEP 2</b></td><td>駐在型AI化支援——現場で手を動かしながら実装（現地30h＋リモート30hの月60h稼働例）</td><td>月60時間・3〜6ヶ月</td><td>参考 100万円/月</td></tr>
      <tr><td><b>STEP 3</b></td><td>内製化（AI研修）——構築済みの自社業務フローを教材に保守運用を習得</td><td>4回×2.5時間</td><td>30万円/名<br><span class="s-meta">助成金で実質1/4以下も</span></td></tr>
    </tbody>
  </table></div>
  <p>研修費用は<a href="/subsidy/">人材開発支援助成金</a>で実質負担を大きく下げられます（2026年度が最終年度）。</p>
</section>

<section>
  <p class="eyebrow">CASE</p>
  <h2>導入事例</h2>
  {case_cards()}
</section>

<section>
  <p class="eyebrow">TARGET</p>
  <h2>対象となる企業</h2>
  <p>従業員<b>10〜500名規模</b>の企業を中心に、<b>業種を問わず</b>ご支援します。紙・FAX・転記・属人化——「書類と例外処理の多い業務」であれば、業種が違っても同じ型でAI化できます。規模外の企業さまもご相談ください。</p>
  <div class="pill-row"><span>不動産・賃貸管理</span><span>製造業</span><span>建設業</span><span>卸売・商社</span><span>物流</span><span>医療・福祉</span><span>士業</span><span>小売・サービス</span></div>
  <p>東京都内の企業さまは、<a href="/area/tokyo/">エリア別の支援内容</a>もご覧ください。</p>
</section>

<section>
  <p class="eyebrow">FAQ</p>
  <h2>よくあるご質問</h2>
  {faq_html(faqs)}
</section>

{cta_block("無料簡易診断の申込", "オンライン・約2時間で、貴社のAI化の期待効果の目安をご提示します。診断だけのご利用も歓迎です。")}
</main>
"""
    write_page(path, head(title, desc, url, ld) + body + footer())


# ================================================================ /column/ ハブ
ARTICLES = [
    ("ai-consulting-cost", "AIコンサルの費用相場【2026年】", "顧問型・プロジェクト型・駐在型…4つの料金体系と適正価格の見極め方。当社の料金も実名で公開しています。"),
    ("ai-consulting-firms", "AI導入支援会社の選び方【中小企業向け】", "総合コンサル・AI開発・研修・伴走実装——4タイプの違いと、失敗しない5つのチェックポイント。"),
    ("ai-gijiroku", "AI議事録の始め方と定着のコツ", "ツールの3タイプ比較と選び方。「文字起こしで終わらせない」社内フォーマット化までの実務。"),
    ("browser-automation", "ブラウザ操作を自動化する3つの方法", "マクロ・RPA・AIエージェントの使い分け。向く業務・向かない業務と導入の注意点。"),
    ("excel-tenki", "Excel転記を自動化する3つの方法", "関数・RPA・AI-OCR×生成AI。手作業の転記をなくす選択肢と、転記そのものを消す業務再設計。"),
]


def page_column_hub():
    path = "/column/"
    url = BASE + path
    title = "コラム｜中小企業のAI業務改善 実践ガイド｜株式会社シクミ"
    desc = "AIコンサルの費用相場、AI議事録、Excel転記の自動化など、中小企業のAI業務改善に役立つ実践知識を、現場で実装しているコンサルタントが解説します。"
    ld = graph(ld_breadcrumb([("株式会社シクミ", BASE + "/"), ("コラム", url)]))
    cards = "".join(
        f'<a class="card ward-card" href="/column/{slug}/"><h3>{esc(t)}</h3><p>{esc(d)}</p><span class="more">読む →</span></a>'
        for slug, t, d in ARTICLES
    )
    body = f"""<main>
{crumbs([("トップ", "/"), ("コラム", url)])}
<div class="hero">
  <p class="eyebrow">COLUMN</p>
  <h1>AI業務改善の実践ガイド</h1>
  <p class="lead">評論ではなく、現場で実装している者の実務知識を。中小企業のAI活用・業務自動化について、駐在型AIコンサルタントが解説します。</p>
</div>
<section>
  <div class="three" style="grid-template-columns:repeat(2,1fr)">{cards}</div>
</section>
{cta_block("無料簡易診断の申込（コラム）", "記事の内容を自社でやってみたい方へ。オンライン・約2時間の無料簡易診断で、貴社のAI化の期待効果の目安をご提示します。")}
</main>
"""
    write_page(path, head(title, desc, url, ld) + body + footer())


def article_head(slug, title, desc, faqs):
    url = f"{BASE}/column/{slug}/"
    ld = graph(
        ld_article(title, desc, url),
        ld_breadcrumb([("株式会社シクミ", BASE + "/"), ("コラム", BASE + "/column/"), (title, url)]),
        ld_faq(faqs),
    )
    return url, head(title, desc, url, ld)


def article_frame(url, h1, lead, inner, subject, related):
    name = h1.replace("<br class=\"sp\">", "")
    return f"""<main class="article">
{crumbs([("トップ", "/"), ("コラム", "/column/"), (name, url)])}
<div class="hero">
  <p class="eyebrow">COLUMN</p>
  <h1>{h1}</h1>
  <p class="meta-line">更新日 {TODAY} ／ 執筆: 株式会社シクミ（駐在型AIコンサルティング）</p>
  <p class="lead">{lead}</p>
</div>
{inner}
<section>
  <p class="eyebrow">RELATED</p>
  <h2>あわせて読む</h2>
  {rel_cards(related)}
</section>
{cta_block(subject, "オンライン・約2時間の無料簡易診断で、貴社のAI化の期待効果の目安をご提示します。診断だけのご利用も歓迎です。")}
</main>
"""


# ================================================================ 記事1: 費用相場
def page_cost():
    slug = "ai-consulting-cost"
    title = "AIコンサルの費用相場【2026年】4つの料金体系と適正価格の見極め方｜株式会社シクミ"
    desc = "AIコンサルの費用相場を契約形態別に解説。顧問型は月10〜50万円、プロジェクト型は100万円〜、駐在・常駐型は月100〜300万円が目安。料金表を公開しない会社が多い中、当社の料金も実名で公開。見積もりで確認すべきポイントも紹介します。"
    faqs = [
        ("AIコンサルの費用相場はいくらですか？", "契約形態によって大きく異なります。目安は、スポット相談・顧問型が月10〜50万円、研修型が1回または1名あたり10〜50万円、調査から実装まで行うプロジェクト型が100万〜1,000万円、常駐・駐在型が月100〜300万円です（当社調べ・2026年時点の一般的なレンジ）。"),
        ("中小企業には高すぎませんか？", "「削減できる工数・コスト」との比較で判断するのが正解です。例えば月40時間の工数削減と月額SaaSの解約が実現できれば、年間で数百万円規模の効果になります。効果試算を先に出してくれる会社を選ぶと、投資判断を誤りません。"),
        ("安いAIコンサルには問題がありますか？", "安さ自体は問題ではありませんが、「助言だけで実装は自社任せ」「特定ツールの販売が目的」のケースがあります。誰が手を動かすのか、成果物は何か、契約が永続しないかの3点を確認してください。"),
        ("費用を抑える方法はありますか？", "研修部分に人材開発支援助成金（中小企業は経費75%助成）を使う、調査フェーズだけ切り出して発注する、無料診断で効果目安を見てから判断する、の3つが有効です。"),
    ]
    url, hd = article_head(slug, title, desc, faqs)
    inner = f"""
<div class="conclusion">
  <p class="c-label">CONCLUSION</p>
  <p><b>結論:</b> AIコンサルの費用は契約形態で決まります。目安は<b>顧問型 月10〜50万円／研修型 10〜50万円／プロジェクト型 100万〜1,000万円／常駐・駐在型 月100〜300万円</b>。金額の高低ではなく「誰が手を動かすか」「効果試算があるか」「契約に終わりがあるか」で見極めるのが失敗しないコツです。</p>
</div>

<section>
  <h2>契約形態別の費用相場</h2>
  <div class="tbl-wrap"><table class="tbl">
    <thead><tr><th>形態</th><th>費用の目安</th><th>内容</th><th>向いている会社</th></tr></thead>
    <tbody>
      <tr><td><b>スポット相談・顧問型</b></td><td>月10〜50万円</td><td>定例MTGでの助言・壁打ち。実装は自社</td><td>社内に手を動かせる人がいる会社</td></tr>
      <tr><td><b>研修型</b></td><td>10〜50万円/回・名</td><td>社員向けのAIリテラシー・活用研修</td><td>まず全社の底上げをしたい会社</td></tr>
      <tr><td><b>プロジェクト型</b></td><td>100万〜1,000万円</td><td>業務調査〜設計〜実装を期間で区切って実行</td><td>特定業務を確実に変えたい会社</td></tr>
      <tr class="hl"><td><b>常駐・駐在型</b></td><td>月100〜300万円</td><td>コンサルタントが現場に入り、部門横断で実装まで実行</td><td>IT担当が不在で「丸ごと任せたい」会社</td></tr>
    </tbody>
  </table></div>
  <p class="s-meta">※ 当社調べ。公開情報および商談での聞き取りに基づく2026年時点の一般的なレンジです。</p>
</section>

<section>
  <h2>費用が変わる4つの要因</h2>
  <ul>
    <li><b>対象範囲</b>——1業務だけか、部門横断か。範囲が広いほど高くなる一方、共通の仕組みで効率化できるため費用対効果は上がりやすい</li>
    <li><b>誰が手を動かすか</b>——助言のみは安く、実装まで任せると高い。ただし自社実装は担当者の人件費と挫折リスクを見込む必要がある</li>
    <li><b>期間と体制</b>——常駐日数・アサイン人数で変動</li>
    <li><b>内製化するか</b>——「卒業」まで設計すると初期は高く見えるが、保守費・顧問料が続かないため総額では安くなることが多い</li>
  </ul>
</section>

<section>
  <h2>参考: シクミの料金（実名公開）</h2>
  <p>相場記事は多くても、自社の料金を明示する会社は多くありません。判断材料として当社の料金を公開します。</p>
  <div class="tbl-wrap"><table class="tbl">
    <thead><tr><th>ステップ</th><th>内容</th><th>料金</th></tr></thead>
    <tbody>
      <tr><td>STEP 0</td><td>無料簡易診断（オンライン・約2時間）</td><td><b>0円</b></td></tr>
      <tr><td>STEP 1</td><td>実地調査・AI化アセスメント（30〜90時間）</td><td>50〜150万円</td></tr>
      <tr><td>STEP 2</td><td>駐在型AI化支援（月60時間・現地＋リモート）</td><td>参考 100万円/月</td></tr>
      <tr><td>STEP 3</td><td>AI研修（4回×2.5時間）</td><td>30万円/名（<a href="/subsidy/">助成金</a>で実質1/4以下も）</td></tr>
    </tbody>
  </table></div>
  <p>相場でいえば「常駐・駐在型」のレンジ下限です。納品後のサブスクリプション費用がなく、不要なSaaSの解約提案まで行うため、トータルの固定費はむしろ下がるケースがあります。詳細は<a href="/service/consulting/">サービスページ</a>をご覧ください。</p>
</section>

<section>
  <h2>見積もりで確認すべき5つのポイント</h2>
  <ol>
    <li><b>成果物は何か</b>——「報告書」なのか「動く仕組み」なのか</li>
    <li><b>誰が手を動かすか</b>——宿題形式なら、社内の実行力を冷静に見積もる</li>
    <li><b>効果試算が先にあるか</b>——削減工数・コストの試算なしの見積もりは判断できない</li>
    <li><b>契約に終わりがあるか</b>——顧問料・保守費が永続する設計になっていないか</li>
    <li><b>ツール中立か</b>——特定製品の販売が目的だと、不要な導入を勧められることがある</li>
  </ol>
</section>

<section>
  <h2>よくある質問</h2>
  {faq_html(faqs)}
</section>
"""
    related = [
        ("AI導入支援会社の選び方", "4タイプの違いと5つのチェックポイント。", "/column/ai-consulting-firms/"),
        ("AI研修に使える助成金", "経費75%助成＋シミュレーター。研修費用はここまで下がります。", "/subsidy/"),
    ]
    write_page(f"/column/{slug}/", hd + article_frame(url, 'AIコンサルの費用相場<br class="sp">——4つの料金体系と見極め方', "AIコンサルを検討して最初に困るのが「料金の目安が公開されていない」こと。この記事では、契約形態別の費用相場と、金額の高低よりも大事な見極めポイントを、実際に支援を行っている当社が解説します。当社の料金も実名で公開します。", inner, "無料簡易診断の申込（費用相場記事）", related) + footer())


# ================================================================ 記事2: 会社の選び方
def page_firms():
    slug = "ai-consulting-firms"
    title = "AI導入支援会社の選び方【中小企業向け】4タイプの違いと5つのチェックポイント｜株式会社シクミ"
    desc = "AI導入支援会社・AIコンサルは「総合コンサル型」「AI開発型」「研修型」「伴走実装型」の4タイプ。中小企業に合うのはどれか、タイプ別の代表的な会社と、発注前に確認すべき5つのチェックポイント・商談で聞くべき質問を解説します。"
    faqs = [
        ("中小企業にはどのタイプのAI導入支援会社が合いますか？", "IT専任者がいない会社なら「伴走実装型」が第一候補です。助言だけの顧問型は社内に実行できる人がいることが前提、AI開発型は数百万円規模の開発予算が前提になるためです。まず研修で底上げしたい場合は研修型も選択肢になります。"),
        ("大手コンサルと中小向け支援会社の違いは何ですか？", "大手総合コンサルは全社DX戦略・大規模開発が主戦場で、費用も数千万円規模になりがちです。中小向けの支援会社は既存ツールの活用と業務再設計が中心で、費用規模が1〜2桁小さく、現場との距離が近いのが特徴です。"),
        ("比較検討では何社くらい話を聞くべきですか？", "2〜3社が現実的です。その際、同じ業務課題を伝えて「効果試算の出し方」「誰が手を動かすか」「契約の終わり方」の回答を比べると、タイプの違いがはっきり見えます。"),
        ("無料相談で何を聞けばいいですか？", "①この業務はAI化できるか、②削減効果の目安、③実装は誰がやるのか、④契約終了後に何が残るのか、⑤総額はいくらか——の5つです。回答が具体的な会社ほど、実務経験が豊富だと判断できます。"),
    ]
    url, hd = article_head(slug, title, desc, faqs)
    inner = f"""
<div class="conclusion">
  <p class="c-label">CONCLUSION</p>
  <p><b>結論:</b> AI導入支援会社は<b>「総合コンサル型」「AI開発型」「研修型」「伴走実装型」の4タイプ</b>に分かれます。IT専任者のいない中小企業に合うのは、現場に入って実装までやる<b>伴走実装型</b>。選ぶときは「誰が手を動かすか」「効果試算があるか」「契約に終わりがあるか」「ツール中立か」「料金が明示されているか」の5点を確認してください。</p>
</div>

<section>
  <h2>AI導入支援会社の4タイプ</h2>
  <div class="tbl-wrap"><table class="tbl">
    <thead><tr><th>タイプ</th><th>代表的な会社の例</th><th>得意領域</th><th>費用感</th><th>向いている会社</th></tr></thead>
    <tbody>
      <tr><td><b>総合コンサル型</b></td><td>アクセンチュア、デロイト トーマツ など</td><td>全社DX戦略・大規模システム</td><td>数千万円〜</td><td>大企業・グループ全体の変革</td></tr>
      <tr><td><b>AI開発型</b></td><td>ブレインパッド、ABEJA、Laboro.AI など</td><td>機械学習モデル開発・データ分析・PoC</td><td>数百万〜数千万円</td><td>独自AIを作りたい・データが豊富な会社</td></tr>
      <tr><td><b>研修型</b></td><td>SHIFT AI、キカガク、スキルアップNeXt など</td><td>AIリテラシー教育・生成AI研修</td><td>数十万円〜</td><td>まず社員の底上げをしたい会社</td></tr>
      <tr class="hl"><td><b>伴走実装型</b></td><td>当社（シクミ）を含む中小向け支援会社</td><td>既存業務のAI化を現場で実装・内製化</td><td>数十万〜数百万円</td><td>IT専任者がおらず「業務を実際に変えたい」中小企業</td></tr>
    </tbody>
  </table></div>
  <p class="s-meta">※ 会社例は各社の公開情報に基づく分類の一例です（2026年9月時点）。各社のサービス詳細は公式サイトでご確認ください。</p>
  <p>重要なのは、<b>タイプが違う会社を並べて相見積もりしても比較にならない</b>ということです。「戦略提言」と「動く仕組み」は別の商品です。まず自社が欲しいものがどれかを決めてから、同じタイプの中で比べてください。</p>
</section>

<section>
  <h2>中小企業の5つのチェックポイント</h2>
  <ol>
    <li><b>誰が手を動かすか</b>——「ご提案します」ではなく「私たちが作ります」と言えるか。宿題形式は、IT担当のいない会社ではほぼ止まります</li>
    <li><b>効果試算が先に出るか</b>——削減工数・コストの試算なしに大きな契約を迫る会社は避ける。無料診断や小さな調査から始められる会社が安全です</li>
    <li><b>契約に終わりがあるか</b>——顧問料・保守費・ライセンス費が永続する設計だと、削減した工数がコストに化けます。「内製化して卒業」をゴールに掲げているかを確認</li>
    <li><b>ツール中立か</b>——自社製品ありきの会社は、不要な導入を勧める構造的な動機を持ちます。既存ツールの解約提案までしてくれるかは中立性の試金石です</li>
    <li><b>料金が明示されているか</b>——「要問い合わせ」だけの会社より、料金体系を公開している会社の方が予算計画を立てやすく、価格の妥当性も検証できます</li>
  </ol>
</section>

<section>
  <h2>商談でそのまま使える質問テンプレート</h2>
  <ul>
    <li>「この業務、御社ならどうAI化しますか？」——具体的な手段が即答できるかで実務経験が分かります</li>
    <li>「削減効果の試算はいつ・どの精度で出ますか？」</li>
    <li>「実装は御社と当社、どちらが手を動かしますか？」</li>
    <li>「契約が終わったあと、社内に何が残りますか？」</li>
    <li>「不要だと分かったツールの解約も提案してもらえますか？」</li>
  </ul>
</section>

<section>
  <h2>参考: 当社（伴走実装型）の場合</h2>
  <p>株式会社シクミは伴走実装型の中でも、コンサルタントが現場に駐在して部門横断で実装まで行う「駐在型」です。無料簡易診断（0円）で効果目安を提示し、実地調査50〜150万円→駐在支援 参考100万円/月→研修30万円/名（<a href="/subsidy/">助成金</a>対応）と、各段階で継続判断できる設計にしています。詳しくは<a href="/service/consulting/">サービスページ</a>へ。</p>
</section>

<section>
  <h2>よくある質問</h2>
  {faq_html(faqs)}
</section>
"""
    related = [
        ("AIコンサルの費用相場", "4つの料金体系と適正価格の見極め方。当社料金も実名公開。", "/column/ai-consulting-cost/"),
        ("生成AI導入支援（駐在型AIコンサル）", "伴走実装型の実際のサービス内容・事例・料金。", "/service/consulting/"),
    ]
    write_page(f"/column/{slug}/", hd + article_frame(url, 'AI導入支援会社の選び方<br class="sp">——4タイプの違いと5つのチェックポイント', "「AIコンサル」と一口に言っても、戦略提言の会社、AIを開発する会社、研修の会社、現場で実装する会社ではまったくの別物です。タイプを間違えて発注すると、高い費用で欲しくないものが届きます。この記事では4タイプの見分け方と、発注前のチェックポイントを解説します。", inner, "無料簡易診断の申込（選び方記事）", related) + footer())


# ================================================================ 記事3: AI議事録
def page_gijiroku():
    slug = "ai-gijiroku"
    title = "AI議事録の始め方——ツールの選び方と「文字起こしで終わらせない」定着のコツ｜株式会社シクミ"
    desc = "AI議事録はツールの3タイプ（会議ツール内蔵・専用SaaS・汎用AI活用）から選ぶのが基本。比較表と選び方、セキュリティ設定、そして文字起こしで終わらせず社内フォーマットの議事録・報告書まで自動化する実務ノウハウを、現場で実装しているコンサルタントが解説します。"
    faqs = [
        ("AI議事録とは何ですか？", "会議の音声をAIが文字起こしし、発言者の識別・要約・決定事項やタスクの抽出までを自動で行う仕組みのことです。会議ツールの内蔵機能、専用SaaS、汎用AIの組み合わせという3つの実現方法があります。"),
        ("無料で始める方法はありますか？", "すでにGoogle Workspace・Microsoft 365・Zoomの有料プランを使っていれば、追加費用なしで会議の文字起こし・要約機能を使える場合があります。まず契約中のプランの機能を確認するのが最短です。"),
        ("精度はどのくらい期待できますか？", "静かな環境のオンライン会議なら実用レベルです。専門用語や固有名詞は誤変換が起きるため、用語集の登録や、生成AIでの後処理（用語統一・整形）を組み合わせると精度が安定します。"),
        ("機密性の高い会議で使っても大丈夫ですか？", "入力データが学習に利用されない法人向けプラン・設定を使うことが大前提です。加えて、録音の同意取得、保存場所と保持期間のルール、社外参加者がいる会議での扱いを社内ルールとして決めておくべきです。"),
    ]
    url, hd = article_head(slug, title, desc, faqs)
    inner = f"""
<div class="conclusion">
  <p class="c-label">CONCLUSION</p>
  <p><b>結論:</b> AI議事録は<b>①会議ツール内蔵機能 → ②専用SaaS → ③汎用AI活用</b>の順に検討するのが合理的です。すでに使っている会議ツールの機能で足りるなら追加費用ゼロ。ただし本当の効果は文字起こしではなく、<b>「社内フォーマットの議事録・報告書が自動で出てくる」状態</b>まで作り込んだときに出ます。</p>
</div>

<section>
  <h2>AI議事録を実現する3つの方法</h2>
  <div class="tbl-wrap"><table class="tbl">
    <thead><tr><th>方法</th><th>例</th><th>費用感</th><th>強み</th><th>弱み</th></tr></thead>
    <tbody>
      <tr><td><b>① 会議ツール内蔵</b></td><td>Google Meet／Microsoft Teams／Zoom の文字起こし・要約機能</td><td>既存プラン内〜</td><td>追加契約不要・導入が一瞬</td><td>フォーマットの自由度が低い・対面会議に弱い</td></tr>
      <tr><td><b>② 専用SaaS</b></td><td>Notta、スマート書記 などの議事録特化ツール</td><td>月数千〜数万円</td><td>話者識別・対面録音・共有機能が充実</td><td>ランニング費用・ツールが1つ増える</td></tr>
      <tr><td><b>③ 汎用AI活用</b></td><td>文字起こし＋ChatGPT/Gemini等で要約・整形</td><td>既存AI契約内〜</td><td>フォーマット自由自在・応用が利く</td><td>仕組みづくりに一手間必要</td></tr>
    </tbody>
  </table></div>
  <p>選び方はシンプルです。<b>今契約しているツールの機能をまず確認</b>し、足りない点（対面会議・話者識別・フォーマット）だけを②③で補ってください。いきなり専用SaaSを契約して、実は会議ツールの標準機能で足りていた——は本当によくある無駄です。</p>
</section>

<section>
  <h2>「文字起こし」で終わらせない——定着の3ステップ</h2>
  <p>多くの会社が「文字起こしはできたが、結局使っていない」で止まります。原因は、出てくるのが<b>長い文字列</b>であって、<b>いつもの議事録</b>ではないからです。</p>
  <div class="flow">
    <div class="f-step"><h3>自社フォーマットを固定する</h3><p>「決定事項／担当／期限／背景」など、貴社の議事録の型をテンプレート化します。既存の議事録3〜5件があれば型は作れます。</p></div>
    <div class="f-step"><h3>文字起こし→型への整形を自動化する</h3><p>生成AIに型と用語集を渡し、文字起こしを流し込むと社内フォーマットの議事録が出てくる仕組みを作ります。ここまでやると「使われるAI議事録」になります。</p></div>
    <div class="f-step"><h3>議事録の先へつなげる</h3><p>抽出したタスクの一覧化、週次報告書への転記、顧客向け報告書のドラフト生成——議事録を起点に後工程まで自動化すると、削減時間が数倍になります。</p></div>
  </div>
</section>

<section>
  <h2>セキュリティと社内ルール</h2>
  <ul>
    <li><b>学習利用オフの法人設定</b>を必ず使う（無料個人アカウントで機密会議を扱わない）</li>
    <li><b>録音の同意</b>——社外参加者がいる会議は事前に一言。議事録AIの利用を明示する</li>
    <li><b>保存ルール</b>——音声データ・文字起こしの保存場所と保持期間を決める</li>
    <li><b>会議の機密区分</b>——役員会議など、AI利用対象外とする会議を先に決めておく</li>
  </ul>
</section>

<section>
  <h2>現場での実例</h2>
  <p>当社の駐在型支援では、議事録・報告書の自動生成は「文書を探す・読む・整える」型の定番として最初期に構築することが多い仕組みです。会議後30分かかっていた議事録作成が数分のチェック作業になり、打ち合わせの多い会社ほど効果が累積します。仕組みの全体像は<a href="/service/consulting/">生成AI導入支援のページ</a>をご覧ください。</p>
</section>

<section>
  <h2>よくある質問</h2>
  {faq_html(faqs)}
</section>
"""
    related = [
        ("Excel転記を自動化する3つの方法", "議事録の次はデータ入力。転記をなくす選択肢を解説。", "/column/excel-tenki/"),
        ("生成AI導入支援（駐在型AIコンサル）", "議事録から業務全体へ。現場で実装するAI化支援。", "/service/consulting/"),
    ]
    write_page(f"/column/{slug}/", hd + article_frame(url, 'AI議事録の始め方<br class="sp">——文字起こしで終わらせない定着のコツ', "AI議事録は今いちばん手軽に効果が出るAI活用です。ただし「文字起こしができた」で止まると、長い文字列が増えるだけで仕事は楽になりません。この記事では、ツールの3タイプの選び方と、社内フォーマットの議事録が自動で出てくる状態までの作り込みを解説します。", inner, "無料簡易診断の申込（AI議事録記事）", related) + footer())


# ================================================================ 記事4: ブラウザ自動化
def page_browser():
    slug = "browser-automation"
    title = "ブラウザ操作を自動化する3つの方法——マクロ・RPA・AIエージェントの使い分け｜株式会社シクミ"
    desc = "ブラウザ操作の自動化は「マクロ・拡張機能」「RPA」「AIエージェント」の3つから選ぶ時代に。それぞれの得意・不得意の比較表、向いている業務、画面変更に強いAIエージェントの新しい選択肢、導入時の注意点を実務目線で解説します。"
    faqs = [
        ("ブラウザ操作の自動化にはどんな方法がありますか？", "大きく3つあります。①ブラウザ拡張・マクロ（単純な繰り返し向け）、②RPA（複数システムをまたぐ定型業務向け）、③AIエージェント（手順を自然言語で指示でき、画面変更に比較的強い新しい選択肢）です。業務の複雑さと変更頻度で選びます。"),
        ("RPAとAIエージェントの違いは何ですか？", "RPAは操作手順を1ステップずつ固定的に記録・実行するため、画面レイアウトの変更に弱い一方、動作は安定しています。AIエージェントは目的を自然言語で指示し、AIが画面を認識して操作するため柔軟ですが、確実性が求められる処理には人の確認ステップを挟む設計が必要です。"),
        ("どんな業務が自動化に向いていますか？", "ルールが明確で、繰り返し回数が多い業務です。例えば、管理画面からのデータダウンロード、複数サイトの情報収集、基幹システムへの定型入力など。逆に、判断が毎回異なる業務や、失敗が許されない送金・承認操作は自動化の対象から外すか、必ず人の確認を挟みます。"),
        ("自動化してはいけないケースはありますか？", "対象サイトの利用規約で自動アクセスが禁止されている場合は行ってはいけません。また、ログイン情報の扱い（平文保存の禁止）、失敗時に業務が止まらない設計、誤操作時の影響範囲の限定は、導入前に必ず設計すべき項目です。"),
    ]
    url, hd = article_head(slug, title, desc, faqs)
    inner = f"""
<div class="conclusion">
  <p class="c-label">CONCLUSION</p>
  <p><b>結論:</b> ブラウザ操作の自動化は<b>①マクロ・拡張機能（単純繰り返し）②RPA（固定的な定型業務）③AIエージェント（変化に強い柔軟な自動化）</b>の3択です。2026年時点の実務では、まず対象業務の「手順の固定度」と「画面の変更頻度」を見て選ぶのが失敗しない順序。確実性が要る処理には、どの方式でも人の確認ステップを挟みます。</p>
</div>

<section>
  <h2>3つの方法の比較</h2>
  <div class="tbl-wrap"><table class="tbl">
    <thead><tr><th></th><th>① マクロ・拡張機能</th><th>② RPA</th><th>③ AIエージェント</th></tr></thead>
    <tbody>
      <tr><td><b>仕組み</b></td><td>操作の記録・再生</td><td>手順をフローとして構築</td><td>目的を自然言語で指示し、AIが画面を認識して操作</td></tr>
      <tr><td><b>得意</b></td><td>同一ページでの単純な繰り返し</td><td>複数システムをまたぐ定型処理</td><td>レイアウト変更への追従・例外の多い作業</td></tr>
      <tr><td><b>弱点</b></td><td>少し複雑になると破綻</td><td>画面変更のたびに改修が必要</td><td>動作の確実性は設計次第・実行コスト</td></tr>
      <tr><td><b>費用感</b></td><td>無料〜数千円</td><td>月数万〜数十万円</td><td>AI利用料（従量）＋構築の一手間</td></tr>
      <tr><td><b>作れる人</b></td><td>現場担当者</td><td>専任担当 or 外部</td><td>プロンプト設計ができる人</td></tr>
    </tbody>
  </table></div>
</section>

<section>
  <h2>AIエージェントで何が変わったか</h2>
  <p>従来のRPA最大の弱点は「画面が変わると壊れる」ことでした。ボタンの位置が変わっただけでエラーが出て、保守担当が直すまで業務が止まる——RPAが「野良ロボット」と揶揄された理由です。</p>
  <p>AIエージェントは画面を人間のように認識して操作するため、<b>レイアウト変更に比較的強く、「この管理画面から先月分の明細をダウンロードして、いつものフォルダに保存して」という粒度の指示</b>で動かせます。一方で、毎回まったく同じ動作をする保証はないため、<b>金額や送信を伴う操作には人の確認を挟む設計</b>が実務の標準です。</p>
  <p>使い分けの目安は次の通りです。</p>
  <ul>
    <li>手順が完全に固定・大量反復 → RPAか、可能ならシステム連携（API）</li>
    <li>手順は決まっているが画面や例外が変わりやすい → AIエージェント</li>
    <li>ダウンロード・情報収集など読み取り中心 → AIエージェントが最も手軽</li>
  </ul>
</section>

<section>
  <h2>導入前チェックリスト</h2>
  <ol>
    <li>対象サイト・システムの<b>利用規約</b>で自動アクセスが許容されているか</li>
    <li><b>ログイン情報の管理</b>——平文でスクリプトに書かない・権限を絞ったアカウントを使う</li>
    <li><b>失敗時の設計</b>——止まったら誰が気づくか・手作業に戻せるか</li>
    <li><b>確認ステップ</b>——送信・登録・支払いを伴う操作は人の承認を挟む</li>
    <li><b>効果測定</b>——削減時間を記録し、保守の手間と比較する</li>
  </ol>
</section>

<section>
  <h2>現場での実例</h2>
  <p>当社の駐在型支援では、ブラウザ上の業務の半自動化は「業務を自動で動かす」型として構築しています。ポイントは、自動化の前に<b>不要な手順そのものを削る</b>こと。10ステップの業務をそのまま自動化するより、3ステップに再設計してから自動化する方が、速くて壊れにくい仕組みになります。詳しくは<a href="/service/consulting/">生成AI導入支援のページ</a>へ。</p>
</section>

<section>
  <h2>よくある質問</h2>
  {faq_html(faqs)}
</section>
"""
    related = [
        ("Excel転記を自動化する3つの方法", "ブラウザの次はExcel。転記作業をなくす選択肢。", "/column/excel-tenki/"),
        ("生成AI導入支援（駐在型AIコンサル）", "自動化の前に業務を再設計。現場で実装するAI化支援。", "/service/consulting/"),
    ]
    write_page(f"/column/{slug}/", hd + article_frame(url, 'ブラウザ操作を自動化する3つの方法<br class="sp">——RPA・マクロ・AIエージェントの使い分け', "管理画面からのダウンロード、複数サイトからの情報収集、基幹システムへの入力——ブラウザの中の繰り返し作業は、いま3つの方法で自動化できます。従来のRPAとAIエージェントの違い、選び方、導入時の注意点を実務目線で解説します。", inner, "無料簡易診断の申込（ブラウザ自動化記事）", related) + footer())


# ================================================================ 記事5: Excel転記
def page_excel():
    slug = "excel-tenki"
    title = "Excel転記を自動化する3つの方法——手作業の転記をなくす実務ガイド｜株式会社シクミ"
    desc = "Excelへの転記作業は「関数・Power Query」「RPA」「AI-OCR×生成AI」の3つで自動化できます。それぞれの向き不向きの比較、選び方の判断フロー、そして転記そのものを消す業務再設計まで。月40時間の転記工数を削減した実例も紹介。"
    faqs = [
        ("Excel転記の自動化にはどんな方法がありますか？", "①Excel内・Excel間の転記なら関数やPower Query、②システム画面からExcelへの転記ならRPA、③紙・PDF・メールからExcelへの転記ならAI-OCRと生成AIの組み合わせ、が基本の3択です。転記元が何かで選びます。"),
        ("プログラミングができなくても自動化できますか？", "できます。Power Queryはマウス操作中心で構築でき、生成AIを使った整形は日本語の指示で作れます。ただし「壊れたときに直せる人」を社内に用意するか、内製化支援まで行う外部パートナーと組むのが長続きのコツです。"),
        ("AI-OCRの精度はどのくらいですか？", "活字の帳票なら実用レベルに達しています。手書きや低品質なFAXは誤読が残るため、読み取り結果を人が確認する画面（チェック工程）を挟む設計が実務では標準です。それでも入力そのものより大幅に速くなります。"),
        ("転記ミスをなくすにはどうすればいいですか？", "最も効果的なのは転記の回数自体を減らすことです。同じ情報を2回入力している箇所を洗い出し、入口で一度だけデータ化して各システムへ流す形に再設計すると、ミスは構造的に発生しなくなります。"),
    ]
    url, hd = article_head(slug, title, desc, faqs)
    inner = f"""
<div class="conclusion">
  <p class="c-label">CONCLUSION</p>
  <p><b>結論:</b> Excel転記の自動化は転記元で選びます。<b>Excel→Excelは「関数・Power Query」、システム画面→Excelは「RPA」、紙・PDF・メール→Excelは「AI-OCR×生成AI」</b>。そして最大の成果は、転記を速くすることではなく<b>転記そのものを業務から消す再設計</b>から生まれます。</p>
</div>

<section>
  <h2>なぜ転記作業はなくならないのか</h2>
  <p>転記は「システムとシステムの分断」から生まれます。FAXで届いた注文をExcelの管理表へ、Excelの管理表から基幹システムへ、基幹システムから報告用Excelへ——<b>同じ情報が形を変えて何度も入力されている</b>のが典型パターンです。1回5分でも、月に数百回あれば数十時間。当社が現場で業務を棚卸しすると、転記は最も頻出する「工数泥棒」です。</p>
</section>

<section>
  <h2>自動化の3つの方法</h2>
  <div class="tbl-wrap"><table class="tbl">
    <thead><tr><th></th><th>① 関数・Power Query</th><th>② RPA</th><th>③ AI-OCR × 生成AI</th></tr></thead>
    <tbody>
      <tr><td><b>向いている転記元</b></td><td>別のExcel・CSV</td><td>システムの画面</td><td>紙・PDF・FAX・メール本文</td></tr>
      <tr><td><b>費用感</b></td><td>0円（Excel標準機能）</td><td>月数万〜数十万円</td><td>AI利用料（月数千円〜）</td></tr>
      <tr><td><b>構築難易度</b></td><td>低〜中</td><td>中</td><td>中（生成AIへの指示設計）</td></tr>
      <tr><td><b>保守性</b></td><td>高い</td><td>画面変更に弱い</td><td>フォーマット変化に比較的強い</td></tr>
      <tr><td><b>まず試すべき人</b></td><td>Excel間の集計・統合がある</td><td>基幹システムへの定型入力がある</td><td>紙・PDFの入力作業がある</td></tr>
    </tbody>
  </table></div>
  <h3>判断フロー</h3>
  <ol>
    <li>転記元がExcel/CSV → <b>Power Query</b>で取得・整形を自動化（追加費用ゼロ）</li>
    <li>転記元がシステム画面 → まず<b>CSVエクスポート機能やAPI</b>を探す。なければRPA</li>
    <li>転記元が紙・PDF・メール → <b>AI-OCR＋生成AI</b>で読み取り、基幹システム取込用の形式に自動変換</li>
  </ol>
</section>

<section>
  <h2>実例: 転記工数を月40時間削減した不動産管理会社</h2>
  <p>当社が支援した東京都の不動産管理会社では、物件書類の検索・転記が手作業で、表記揺れによる重複登録が運用工数を約1.2倍に膨らませていました。書類の自動リネーム・名寄せ・1物件1ページ帳票の自動生成・基幹システム入力データの自動生成を構築した結果、<b>書類検索・転記の工数を月40時間削減</b>。さらに「転記先」だった月額基幹システム自体が不要と判明し、解約で固定費も削減しました（契約金額150万円・約2ヶ月）。</p>
  <p>この事例が示す通り、転記の自動化を進めると<b>「そもそもこの転記先は必要か？」</b>という問いに行き着きます。ここまで踏み込むのが業務再設計です。</p>
</section>

<section>
  <h2>長続きさせる3つのコツ</h2>
  <ul>
    <li><b>入口で一度だけデータ化する</b>——紙・FAX・メールで届いた情報は、届いた瞬間に構造化し、以降は流用する</li>
    <li><b>チェック工程を残す</b>——AI読み取りは「人が確認して確定」を挟むと、精度不安なく運用に乗ります</li>
    <li><b>直せる人を社内に作る</b>——仕組みは必ずメンテナンスが発生します。作って終わりの外注ではなく、内製化までを設計してください</li>
  </ul>
</section>

<section>
  <h2>よくある質問</h2>
  {faq_html(faqs)}
</section>
"""
    related = [
        ("ブラウザ操作を自動化する3つの方法", "転記の相棒、画面操作の自動化。RPAとAIエージェントの使い分け。", "/column/browser-automation/"),
        ("生成AI導入支援（駐在型AIコンサル）", "転記を消す業務再設計を、現場に入って実装します。", "/service/consulting/"),
    ]
    write_page(f"/column/{slug}/", hd + article_frame(url, 'Excel転記を自動化する3つの方法<br class="sp">——手作業の転記をなくす実務ガイド', "システムからExcelへ、ExcelからExcelへ、紙からExcelへ——転記は中小企業の現場で最も多く見つかる「工数泥棒」です。この記事では転記元別の自動化手段3つと選び方、そして転記そのものを業務から消す再設計を、実例つきで解説します。", inner, "無料簡易診断の申込（Excel転記記事）", related) + footer())


# ================================================================ main
if __name__ == "__main__":
    page_subsidy()
    page_training()
    page_consulting()
    page_column_hub()
    page_cost()
    page_firms()
    page_gijiroku()
    page_browser()
    page_excel()
    print("generated: subsidy, training, consulting, column hub + 5 articles (9 pages)")
