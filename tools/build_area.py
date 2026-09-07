# -*- coding: utf-8 -*-
"""エリアページ生成スクリプト
使い方: python3 tools/build_area.py  （リポジトリルートで実行）
/area/tokyo/ 配下の区別ページ・東京都ハブページ・sitemap.xml を生成する。
区を追加するときは WARDS に1エントリ足して再実行。
"""
import os, datetime, json
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://shikumi-co.jp"
# 経済センサス(令和3年・第24表)と住民基本台帳(令和8年)の23区データ。tools/data/census_tokyo23.json
_CENSUS = json.load(open(os.path.join(ROOT, "tools", "data", "census_tokyo23.json"), encoding="utf-8"))
CENSUS, POP = _CENSUS["census"], _CENSUS["population"]
INDUSTRY_LINKS = {"不動産業，物品賃貸業": "real-estate", "製造業": "manufacturing", "建設業": "construction", "卸売業，小売業": "wholesale", "運輸業，郵便業": "logistics", "医療，福祉": "healthcare", "学術研究，専門・技術サービス業": "professional"}
FOCUS_INDUSTRIES = ["卸売業，小売業", "製造業", "建設業", "不動産業，物品賃貸業", "医療，福祉", "学術研究，専門・技術サービス業", "情報通信業", "運輸業，郵便業"]
TODAY = datetime.date.today().isoformat()

# ---------------------------------------------------------------- 区データ
# points: (見出し, 本文) ×3 = その区の産業構成に合わせた「AI化の効きどころ」
WARDS = {
    "shibuya": {
        "name": "渋谷区", "en": "SHIBUYA",
        "lead": "渋谷は当社のオフィス所在地です。IT・Web・クリエイティブから商業・サービスまで、少人数で事業を伸ばす会社が集まる街。だからこそ「人を増やさずに業務を回す仕組み」が最も効きます。",
        "industry": "渋谷区はIT・Webサービス、広告・クリエイティブ、スタートアップの集積地であると同時に、商業・飲食・美容などのサービス事業者も多いエリアです。共通するのは、少人数のバックオフィスで契約・経理・労務を兼務しながら回している点。SaaSの契約だけが増えて使いこなせていない、という相談も渋谷の会社から多くいただきます。",
        "points": [
            ("増え続けるSaaSの整理と解約", "ツールを足す前に業務を整えるのが当社の流儀です。重複したSaaSの棚卸しと解約提案まで行い、固定費そのものを下げます。"),
            ("提案書・議事録・レポートの自動化", "打ち合わせの多いクリエイティブ・受託業では、議事録作成と社内フォーマットへの整形をAI化するだけで担当者の残業が目に見えて減ります。"),
            ("少人数バックオフィスの属人化解消", "経理・総務が1〜2名の会社では「その人が休むと止まる」が最大のリスク。業務フローを仕組みに埋め込み、誰でも回せる状態にします。"),
        ],
        "access": "オフィスは渋谷区桜丘町。区内の現場へは最短即日でお伺いできます。",
        "ward_faq": ("渋谷区内ならすぐ来てもらえますか？", "はい。当社オフィスが渋谷区桜丘町にあるため、区内は最も柔軟に日程調整できます。無料簡易診断はオンラインでも対面でも承ります。"),
        "desc": "渋谷区のAI導入支援・AIコンサルティングなら株式会社シクミ。渋谷・桜丘町拠点の駐在型AIコンサルが現場に入り、実装から内製化まで支援。無料簡易診断受付中。",
        "neighbors": ["shinjuku", "minato", "meguro", "setagaya"],
        "area_note": "渋谷・道玄坂・神南のIT／クリエイティブ企業、恵比寿・代官山・広尾のサービス業、幡ヶ谷・笹塚・初台の小規模事業者まで",
        "areas": ["渋谷", "道玄坂", "神南", "宇田川町", "桜丘町", "南平台町", "鶯谷町", "代官山町", "猿楽町", "鉢山町", "恵比寿", "恵比寿西", "恵比寿南", "広尾", "東", "神宮前", "千駄ヶ谷", "代々木", "上原", "西原", "大山町", "初台", "本町", "幡ヶ谷", "笹塚", "松濤", "神山町", "富ヶ谷", "元代々木町", "円山町", "神泉町"],
    },
    "shinjuku": {
        "name": "新宿区", "en": "SHINJUKU",
        "lead": "都内有数の事業所密度を誇る新宿区。商業・サービス業から不動産管理、医療関連まで、書類と転記に追われる現場の「作り変え」を、渋谷から直接伺って支援します。",
        "industry": "新宿区は大規模商業地であると同時に、不動産管理会社・士業事務所・クリニック・専門サービスの中小事業者が高密度に集まるエリアです。物件資料や契約書類、複数システムへの転記など「紙とExcelの往復」が業務時間を圧迫している会社が少なくありません。当社は東京都内の不動産管理会社で書類自動整理・名寄せ・帳票自動生成を構築した実績があり、同種の業務構造にそのまま型を適用できます。",
        "points": [
            ("不動産・管理業務の書類自動化", "物件資料の自動リネーム・表記揺れの名寄せ・1物件1ページ帳票の自動生成など、実績のある「仕組みの型」を導入できます。"),
            ("多店舗・多拠点の報告集約", "店舗ごとにバラバラな日報・売上報告をAIが集約し、社内フォーマットへ自動整形。本部の取りまとめ工数をなくします。"),
            ("問い合わせ対応の即答化", "よくある質問への回答を社内ナレッジから即答するQAボットで、電話・メール対応の負担を軽減します。"),
        ],
        "access": "渋谷オフィスから新宿区内へは電車で1本。訪問頻度も柔軟に設計できます。",
        "ward_faq": ("不動産管理会社ですが、同業の支援実績はありますか？", "あります。東京都内の不動産管理会社で、書類検索・転記工数を月40時間削減し、月額基幹システムの解約まで実現した事例があります（現地訪問5回・約2ヶ月）。"),
        "desc": "新宿区のAI導入支援・AIコンサルティングなら株式会社シクミ。不動産管理の書類自動化など実績のある駐在型AIコンサルが新宿の現場に入り、実装から内製化まで支援します。",
        "neighbors": ["shibuya", "chiyoda", "toshima", "minato"],
        "area_note": "西新宿のオフィス街、新宿・歌舞伎町の商業、高田馬場・早稲田・四谷・神楽坂の事業所、落合・中井の住宅地まで",
        "areas": ["新宿", "西新宿", "歌舞伎町", "北新宿", "百人町", "大久保", "高田馬場", "西早稲田", "早稲田鶴巻町", "戸山", "上落合", "中落合", "下落合", "中井", "市谷本村町", "市谷田町", "市谷八幡町", "四谷", "荒木町", "舟町", "左門町", "信濃町", "須賀町", "若葉", "南元町", "内藤町", "大京町", "富久町", "余丁町", "河田町", "若松町", "原町", "弁天町", "榎町", "矢来町", "神楽坂", "袋町", "揚場町", "新小川町", "津久戸町", "白銀町", "山吹町", "天神町", "赤城元町", "北町", "中町", "南町", "箪笥町", "納戸町", "市谷加賀町", "市谷柳町", "住吉町", "愛住町", "坂町", "本塩町", "三栄町"],
    },
    "minato": {
        "name": "港区", "en": "MINATO",
        "lead": "本社機能・外資系・コンサルティング・広告と、知的生産の密度が高い港区。資料づくりと契約書類に費やす時間を、AIで事業の時間へ返します。",
        "industry": "港区は大手・外資の本社機能に加え、広告・IT・士業・コンサルティングなどプロフェッショナルサービスの事業者が集積するエリアです。提案書・契約書・レポートといった「文書をつくる・確認する」業務の比重が高く、ここをAI化したときの削減効果が大きいのが特徴。営業部門とバックオフィスを部門横断で見て、会社全体の文書フローを再設計します。",
        "points": [
            ("提案書・営業資料のドラフト自動化", "過去資料と商談メモから提案書の下書きをAIが生成。営業は仕上げに集中でき、提案の量と速度が上がります。"),
            ("契約書の抽出・整理・検索", "大量の契約書PDFから期日や条件を自動抽出して一覧化。「あの契約どこ？」を探す時間をなくします。"),
            ("英日ドキュメントの変換・要約", "外資取引で発生する英文資料の要約・社内フォーマット化を自動化し、報告業務を軽くします。"),
        ],
        "access": "渋谷オフィスから港区内へは電車・タクシーですぐ。頻度の高い駐在にも対応しやすいエリアです。",
        "ward_faq": ("セキュリティ要件が厳しいのですが対応できますか？", "NDA締結の上、入力データが学習に利用されない法人向けプラン・設定を前提に、貴社のセキュリティ方針に合わせてツールを構成します。情報システム部門との調整も当社が行います。"),
        "desc": "港区のAI導入支援・AIコンサルティングなら株式会社シクミ。提案書・契約書などの文書業務を駐在型AIコンサルが現場で自動化。実装から内製化まで一気通貫で支援します。",
        "neighbors": ["shibuya", "shinjuku", "chiyoda", "shinagawa"],
        "area_note": "六本木・赤坂・虎ノ門の本社／外資系、新橋・浜松町・芝の中小オフィス、芝浦・港南の物流／メーカー、青山・麻布のクリエイティブまで",
        "areas": ["赤坂", "北青山", "南青山", "麻布十番", "元麻布", "西麻布", "東麻布", "麻布台", "南麻布", "六本木", "虎ノ門", "新橋", "西新橋", "東新橋", "浜松町", "芝", "芝公園", "芝大門", "芝浦", "海岸", "港南", "高輪", "白金", "白金台", "三田", "愛宕", "台場"],
    },
    "chiyoda": {
        "name": "千代田区", "en": "CHIYODA",
        "lead": "大手町・丸の内・神田。日本有数のビジネス街である千代田区は、歴史ある企業ほど「紙と稟議の文化」が残る街でもあります。その文化を壊さず、業務だけを作り変えます。",
        "industry": "千代田区には金融・出版・士業・老舗企業の本社が集まり、規程や稟議、紙の帳票といった「文書ガバナンス」がしっかりしている分、作業が重くなりがちです。既存のルールを尊重したまま、探す・転記する・整形するの3工程をAIに置き換えるのが当社のアプローチ。神田エリアの中小企業から大手の一部門まで、規模を問わず対応します。",
        "points": [
            ("規程・マニュアルの即答化", "社内規程やマニュアルに基づいて質問に即答するQAボットを構築。「誰に聞けばいい？」で止まる時間をなくします。"),
            ("稟議・帳票の下書き自動化", "定型の稟議書・報告書をAIが下書きし、人は確認と判断に集中。書式はそのまま、作業だけを軽くします。"),
            ("紙書類のデータ化と横断検索", "紙・PDFで保管された書類をスキャンから一覧化まで半自動化。過去書類を探す時間を数秒に短縮します。"),
        ],
        "access": "渋谷オフィスから千代田区内へは電車で1本。定例訪問の設計もしやすいエリアです。",
        "ward_faq": ("紙の書類が大量にあるのですが、データ化から頼めますか？", "はい。紙契約書を全件スキャンし、相手先・開始日・種別を一覧化して横断検索できる状態まで構築した実績があります（埼玉県・不動産会社／現地訪問7回・約3ヶ月）。"),
        "desc": "千代田区のAI導入支援・AIコンサルティングなら株式会社シクミ。規程・稟議・紙書類の多い現場を駐在型AIコンサルが作り変え、実装から内製化まで支援します。",
        "neighbors": ["chuo", "minato", "shinjuku", "taito"],
        "area_note": "大手町・丸の内・有楽町の大手本社、霞が関・永田町、神田・秋葉原の中小企業／専門商社、麹町・九段・飯田橋のオフィスまで",
        "areas": ["大手町", "丸の内", "有楽町", "霞が関", "永田町", "隼町", "平河町", "麹町", "一番町", "二番町", "三番町", "四番町", "五番町", "六番町", "九段北", "九段南", "飯田橋", "富士見", "紀尾井町", "内幸町", "内神田", "外神田", "神田錦町", "神田小川町", "神田駿河台", "神田神保町", "神田淡路町", "神田須田町", "神田多町", "神田司町", "神田美土代町", "神田鍛冶町", "神田紺屋町", "神田佐久間町", "神田和泉町", "神田岩本町", "神田練塀町", "神田花岡町", "神田松永町", "神田猿楽町", "神田三崎町", "西神田", "東神田", "岩本町", "鍛冶町"],
    },
    "chuo": {
        "name": "中央区", "en": "CHUO",
        "lead": "日本橋・京橋・築地。商社・卸売・老舗企業が集まる中央区では、今もFAXと電話で受発注が動いています。その入口をAIで受け止め、後工程をまるごと自動化します。",
        "industry": "中央区は卸売・商社・金融の集積地で、取引先との受発注がFAX・メール添付・電話といったアナログな入口から始まる会社が多いエリアです。入口がアナログでも、その先の照合・転記・帳票作成はAI化できます。取扱商品数が多い卸売業では、商品マスタとの照合や顧客別の掛率計算など「人の記憶に頼っていた業務」を仕組みに変えることで、属人化と残業を同時に解消できます。",
        "points": [
            ("FAX・メール受注の自動データ化", "届いた注文書をAIが読み取り、基幹システム入力用のデータへ自動変換。転記作業と入力ミスをなくします。"),
            ("見積業務の半自動化", "商品マスタ・顧客別条件との照合をAIが行い、見積書ドラフトまで自動生成。属人化した見積業務を誰でも回せる形にします（製造業での提案実績あり）。"),
            ("帳票・請求処理の整流化", "取引先ごとにバラバラな帳票を社内フォーマットへ自動整形。月末月初の事務集中を平準化します。"),
        ],
        "access": "渋谷オフィスから中央区内へは電車で1本。日本橋・築地方面もまとめて対応します。",
        "ward_faq": ("FAXでの受注が多いのですが、本当にAI化できますか？", "できます。FAXやメール添付で届く書類をAIが読み取り、後工程を自動化する構成は当社の得意分野です。取引先にやり方を変えてもらう必要はありません。"),
        "desc": "中央区のAI導入支援・AIコンサルティングなら株式会社シクミ。FAX受発注・見積・帳票処理の自動化を駐在型AIコンサルが現場で実装。内製化まで一気通貫で支援します。",
        "neighbors": ["chiyoda", "minato", "koto", "taito"],
        "area_note": "日本橋・京橋の商社／老舗企業、八重洲・銀座の商業、兜町の金融、築地・月島・勝どき・晴海の食品／物流まで",
        "areas": ["日本橋", "日本橋本町", "日本橋室町", "日本橋本石町", "日本橋小舟町", "日本橋堀留町", "日本橋人形町", "日本橋小伝馬町", "日本橋大伝馬町", "日本橋横山町", "日本橋馬喰町", "日本橋久松町", "日本橋浜町", "日本橋蛎殻町", "日本橋箱崎町", "日本橋中洲", "日本橋兜町", "日本橋茅場町", "日本橋小網町", "日本橋富沢町", "東日本橋", "八重洲", "京橋", "銀座", "築地", "新富", "入船", "湊", "明石町", "八丁堀", "新川", "佃", "月島", "勝どき", "晴海", "豊海町"],
    },
    "shinagawa": {
        "name": "品川区", "en": "SHINAGAWA",
        "lead": "メーカー本社と物流、オフィスと町場が同居する品川区。複数システムをまたぐ転記と月次レポートづくりを、AIで「流れる業務」に変えます。",
        "industry": "品川区は大崎・五反田のIT企業、天王洲・港南のメーカー本社、そして区南部の物流・製造まで、業態の幅が広いエリアです。共通課題は、販売管理・会計・Excelと複数のシステムに同じ情報を入れ直す転記業務と、月次の報告資料づくり。AIの出力が業務ソフトまでまっすぐ流れる形に組み替えることで、部門をまたぐ「二重入力」を根本からなくします。",
        "points": [
            ("システム間転記の自動化", "受注情報や経費データを複数システムへ入れ直す作業を自動化。入力ミスと確認工数を同時に減らします。"),
            ("月次レポートの自動生成", "売上・稼働のデータからレポートを自動生成し、社内フォーマットで出力。月初の資料づくりから解放します。"),
            ("倉庫・現場帳票のデジタル化", "紙の入出庫記録や検品記録をAIでデータ化し、在庫や進捗をリアルタイムに見える化します。"),
        ],
        "access": "渋谷オフィスから品川区内へは電車で1本。大崎・五反田エリアはすぐに伺えます。",
        "ward_faq": ("既存の基幹システムはそのままで導入できますか？", "はい。新システムの導入ありきではなく、既存システムを活かしたままAIで前後の工程をつなぐのが当社の基本方針です。逆に不要なシステムが見つかれば解約もご提案します。"),
        "desc": "品川区のAI導入支援・AIコンサルティングなら株式会社シクミ。システム間転記や月次レポートを駐在型AIコンサルが自動化。実装から内製化まで現場で支援します。",
        "neighbors": ["minato", "meguro", "ota", "shibuya"],
        "area_note": "大崎・五反田のIT企業、品川駅周辺の本社群、大井・勝島・八潮の物流／製造、戸越・中延・武蔵小山の商店街まで",
        "areas": ["大崎", "西五反田", "東五反田", "上大崎", "北品川", "南品川", "東品川", "西品川", "広町", "荏原", "旗の台", "中延", "東中延", "西中延", "戸越", "豊町", "二葉", "平塚", "小山", "小山台", "西大井", "大井", "東大井", "南大井", "勝島", "八潮", "東八潮"],
    },
    "meguro": {
        "name": "目黒区", "en": "MEGURO",
        "lead": "デザイン・クリエイティブから医療・生活サービスまで、少数精鋭の事業者が多い目黒区。「専任のIT担当がいない」会社にこそ、駐在型のAI導入が効きます。",
        "industry": "目黒区は中目黒・自由が丘を中心にデザイン事務所や小規模な専門サービス、クリニック・介護などの医療福祉事業者が多いエリアです。数名〜数十名の組織では、経理も労務も広報も一人が兼務しているのが普通で、新しいツールを検討する時間そのものがありません。当社のコンサルタントが「社内のAI担当」として現場に入り、検討から実装・定着までを肩代わりします。",
        "points": [
            ("兼務バックオフィスの負担軽減", "請求書処理・経費整理・書類作成といった定常業務をAI化し、兼務担当者の時間を本業へ返します。"),
            ("予約・問い合わせ対応の効率化", "よくある問い合わせへの返信下書きや、予約情報の台帳整理を自動化。応対品質を保ちながら手間を減らします。"),
            ("記録・報告業務の自動化", "サービス記録や日報を音声・メモからAIが整形。現場スタッフの残業時間を削ります。"),
        ],
        "access": "渋谷オフィスから目黒区内へは電車ですぐ。小規模なご相談も歓迎です。",
        "ward_faq": ("従業員10名未満でも依頼できますか？", "ご相談ください。対象は従業員10〜500名規模が中心ですが、業務にAI化の余地があれば規模を問わずお力になれます。まずは無料簡易診断で効果の目安をご確認いただくのがおすすめです。"),
        "desc": "目黒区のAI導入支援・AIコンサルティングなら株式会社シクミ。IT担当のいない少人数の会社にこそ効く駐在型AIコンサル。実装から内製化まで現場で支援します。",
        "neighbors": ["shibuya", "setagaya", "shinagawa", "ota"],
        "area_note": "中目黒・目黒のクリエイティブ／オフィス、自由が丘・都立大学の商業、碑文谷・洗足・大岡山の住宅地の医療福祉まで",
        "areas": ["中目黒", "上目黒", "東山", "青葉台", "大橋", "駒場", "目黒", "下目黒", "三田", "中町", "五本木", "祐天寺", "中央町", "鷹番", "碑文谷", "目黒本町", "原町", "洗足", "南", "平町", "大岡山", "緑が丘", "自由が丘", "中根", "柿の木坂", "八雲", "東が丘"],
    },
    "setagaya": {
        "name": "世田谷区", "en": "SETAGAYA",
        "lead": "23区最大級の人口を抱える世田谷区は、医療福祉・建設・不動産・生活サービスの中小事業者が地域を支える街。現場仕事の裏側にある事務作業を、AIで軽くします。",
        "industry": "世田谷区には訪問介護・クリニックなどの医療福祉、工務店・リフォームなどの建設、賃貸管理・仲介の不動産と、「現場+事務」の二重構造を持つ事業者が多く集まります。現場は忙しく、事務所に戻ってからの報告書・請求・シフト調整が残業の原因になりがちです。現場の動きを変えずに、事務側をAIで作り変えるのが当社の支援スタイルです。",
        "points": [
            ("現場報告・記録の自動整形", "写真やメモ、音声から報告書・介護記録・工事記録を自動生成。事務所に戻ってからの書き物をなくします。"),
            ("請求・保険関連書類の効率化", "サービス実績から請求データを自動作成し、チェック作業に集中できる形へ。月初の締め作業を短縮します。"),
            ("賃貸管理業務の書類自動化", "物件書類の自動整理・名寄せ・帳票生成など、東京都内の不動産管理会社で実証済みの型を適用できます。"),
        ],
        "access": "渋谷オフィスから世田谷区内へは電車・車でスムーズに伺えます。",
        "ward_faq": ("現場スタッフはパソコンが得意ではありませんが大丈夫ですか？", "大丈夫です。現場の方の操作は「写真を撮る」「いつも通り入力する」程度に抑えた設計にします。研修も非エンジニアの方を対象に、構築済みの自社業務フローを教材として行います。"),
        "desc": "世田谷区のAI導入支援・AIコンサルティングなら株式会社シクミ。医療福祉・建設・不動産の事務作業を駐在型AIコンサルが自動化。実装から内製化まで支援します。",
        "neighbors": ["shibuya", "meguro", "ota", "shinjuku"],
        "area_note": "三軒茶屋・下北沢の商業、用賀・二子玉川のオフィス／商業、成城・経堂・祖師谷・千歳烏山の医療福祉・建設・不動産事業者まで",
        "areas": ["三軒茶屋", "太子堂", "池尻", "三宿", "下馬", "野沢", "上馬", "駒沢", "新町", "桜新町", "弦巻", "世田谷", "桜", "経堂", "宮坂", "豪徳寺", "梅丘", "松原", "赤堤", "代田", "代沢", "北沢", "大原", "羽根木", "上北沢", "桜上水", "船橋", "千歳台", "祖師谷", "砧", "大蔵", "岡本", "鎌田", "喜多見", "成城", "上祖師谷", "粕谷", "南烏山", "北烏山", "給田", "八幡山", "深沢", "等々力", "玉川", "上野毛", "野毛", "中町", "玉川台", "瀬田", "用賀", "玉堤", "尾山台", "奥沢", "東玉川", "玉川田園調布"],
    },
    "ota": {
        "name": "大田区", "en": "OTA",
        "lead": "町工場の集積地・大田区。図面と見積、FAXと検査記録——ものづくりの現場を支える紙の業務を、技術を持つ人が本業に集中できる仕組みへ作り変えます。",
        "industry": "大田区は都内最大級の製造業集積地であり、羽田を擁する物流の要衝でもあります。機械・金属加工の町工場では、見積依頼がFAXやメールでバラバラに届き、図面の確認や過去実績の照合がベテランの記憶に依存しがちです。当社は製造業の見積業務で作業時間50〜60%削減を目標とする支援を設計した実績があり（実施前のご提案例）、「職人の時間を事務から守る」AI化を得意としています。",
        "points": [
            ("見積・受注業務の半自動化", "FAX・メールで届く依頼をAIが読み取り、過去実績や単価表と照合して見積ドラフトを自動生成。ベテラン依存を解消します。"),
            ("検査記録・作業日報のデータ化", "紙の検査表や日報をAIでデータ化し、集計・報告を自動化。品質記録の検索も一瞬になります。"),
            ("入出荷・物流帳票の自動処理", "納品書・送り状などの帳票作成と照合を自動化し、出荷前後の事務作業を圧縮します。"),
        ],
        "access": "渋谷オフィスから大田区内へは電車で1本。工場への訪問時間も柔軟に合わせます。",
        "ward_faq": ("製造業の支援実績はありますか？", "製造業の見積業務について、月1,500時間規模の業務で作業時間50〜60%削減を目標とする支援を設計したご提案実績があります（実施前のご提案例）。既存のGoogle Workspace上に構築する、内製化しやすい構成です。"),
        "desc": "大田区のAI導入支援・AIコンサルティングなら株式会社シクミ。町工場・製造業の見積や検査記録を駐在型AIコンサルが自動化。実装から内製化まで現場で支援します。",
        "neighbors": ["shinagawa", "meguro", "setagaya", "koto"],
        "area_note": "蒲田・大森の商業／オフィス、京浜島・城南島・昭和島・羽田の工業／物流、馬込・池上・矢口の町工場、田園調布・雪谷・久が原の住宅地サービスまで",
        "areas": ["池上", "石川町", "鵜の木", "大森中", "大森本町", "大森東", "大森西", "大森南", "大森北", "蒲田", "蒲田本町", "上池台", "北糀谷", "北千束", "北馬込", "北嶺町", "久が原", "京浜島", "山王", "下丸子", "城南島", "昭和島", "新蒲田", "多摩川", "千鳥", "中央", "田園調布", "田園調布本町", "田園調布南", "東海", "仲池上", "中馬込", "仲六郷", "西蒲田", "西糀谷", "西馬込", "西嶺町", "西六郷", "萩中", "羽田", "羽田旭町", "羽田空港", "東蒲田", "東糀谷", "東馬込", "東嶺町", "東矢口", "東雪谷", "東六郷", "平和島", "本羽田", "南蒲田", "南久が原", "南千束", "南馬込", "南雪谷", "南六郷", "矢口", "雪谷大塚町", "令和島"],
    },
    "toshima": {
        "name": "豊島区", "en": "TOSHIMA",
        "lead": "池袋を中心に商業・サービス・不動産が集まる豊島区。店舗と本部、現場と事務所のあいだで発生する「報告と転記」を、AIでまっすぐ流します。",
        "industry": "豊島区は池袋の大規模商業に加え、飲食・小売の多店舗事業者、不動産仲介・管理会社が多いエリアです。店舗ごとの売上報告や勤怠、物件資料の作成など、フォーマットの揃わない情報を人手で集約する業務が積み重なりがちです。情報の入口から社内フォーマットへの整形までをAIに任せ、本部・事務所は判断に集中できる体制を作ります。",
        "points": [
            ("多店舗の報告・集計の自動化", "各店舗の売上・勤怠・日報をAIが集約して自動集計。本部のとりまとめ作業をなくします。"),
            ("物件資料・募集図面の自動生成", "物件情報から募集資料や帳票を自動生成し、表記揺れも名寄せ。不動産実務の書類時間を短縮します。"),
            ("求人・シフト業務の効率化", "応募対応の下書きやシフト表の下案作成をAI化し、店長・管理者の管理業務を軽くします。"),
        ],
        "access": "渋谷オフィスから豊島区内へは電車で1本。池袋エリアはすぐに伺えます。",
        "ward_faq": ("店舗スタッフの運用が定着するか不安です。", "運用が現場に定着するまでが当社の仕事です。ヒアリングは業務をしながら横で見せていただく観察が中心で、現場の負担を最小限に。面倒な作業から先に引き受け、「ラクになる」実感から定着させます。"),
        "desc": "豊島区のAI導入支援・AIコンサルティングなら株式会社シクミ。多店舗の報告集約や不動産書類を駐在型AIコンサルが自動化。実装から内製化まで支援します。",
        "neighbors": ["shinjuku", "chiyoda", "taito", "sumida"],
        "area_note": "池袋のオフィス／商業、巣鴨・駒込の商店街と医療福祉、目白・雑司が谷、要町・千川・長崎の小規模事業者まで",
        "areas": ["池袋", "東池袋", "西池袋", "南池袋", "上池袋", "池袋本町", "北大塚", "南大塚", "巣鴨", "西巣鴨", "駒込", "目白", "雑司が谷", "南長崎", "長崎", "千早", "要町", "高松", "千川", "高田"],
    },
    "taito": {
        "name": "台東区", "en": "TAITO",
        "lead": "蔵前・浅草橋の問屋街、浅草・上野の観光商業。伝統ある商いが息づく台東区で、紙伝票と商品台帳の業務をAIで次の代へつなぎます。",
        "industry": "台東区は皮革・雑貨・玩具などの卸問屋が集まる商いの街であり、観光関連の店舗・宿泊事業者も多いエリアです。長く続く会社ほど、手書き伝票・FAX注文・紙の商品台帳といった業務資産が残っており、それが若手への引き継ぎの壁にもなっています。業務のやり方を尊重しながら、伝票・台帳・在庫の情報をデジタルの仕組みへ移し替え、事業承継にも耐える形を作ります。",
        "points": [
            ("紙伝票・手書き書類のデータ化", "手書き伝票やFAX注文書をAIが読み取ってデータ化。入力作業をなくし、過去の取引も検索できるようにします。"),
            ("商品台帳・在庫情報の一元化", "紙とExcelに分かれた商品情報を名寄せして一元化。「あの品番どれ？」の確認時間をなくします。"),
            ("多言語対応・案内業務の自動化", "観光客向けの案内文・メール返信の多言語ドラフトをAIが生成。人手を増やさずに対応品質を上げます。"),
        ],
        "access": "渋谷オフィスから台東区内へは電車で1本。問屋街への定期訪問も設計できます。",
        "ward_faq": ("高齢の社員が多くても使いこなせますか？", "使いこなせる形に作ります。操作を覚えるのではなく「いつもの業務のやり方はそのまま、裏側だけ自動化する」設計が基本です。研修は構築済みの自社業務フローを教材に、非エンジニアの方向けに行います。"),
        "desc": "台東区のAI導入支援・AIコンサルティングなら株式会社シクミ。問屋・卸の紙伝票や商品台帳を駐在型AIコンサルがデータ化・自動化。内製化まで現場で支援します。",
        "neighbors": ["chiyoda", "chuo", "sumida", "toshima"],
        "area_note": "上野・秋葉原の商業／卸、浅草の観光・飲食、蔵前・浅草橋・鳥越の問屋街、入谷・三ノ輪・橋場の製造業まで",
        "areas": ["上野", "東上野", "上野公園", "上野桜木", "池之端", "谷中", "根岸", "下谷", "入谷", "竜泉", "千束", "浅草", "西浅草", "東浅草", "花川戸", "雷門", "駒形", "寿", "蔵前", "柳橋", "浅草橋", "鳥越", "三筋", "小島", "元浅草", "松が谷", "北上野", "台東", "秋葉原", "清川", "日本堤", "橋場", "今戸", "三ノ輪"],
    },
    "sumida": {
        "name": "墨田区", "en": "SUMIDA",
        "lead": "ものづくりの伝統が息づく墨田区。職人の技はそのままに、受発注・日報・請求といった周辺業務をAIで軽くし、小さなチームの生産性を最大化します。",
        "industry": "墨田区は金属・ガラス・革製品など、多品種少量のものづくり中小企業が集まるエリアです。数名規模の工場では、社長や職人自身が見積・請求・納期管理まで担っているケースが多く、事務作業が製造時間を侵食しています。事務所に人を増やすのではなく、AIの仕組みで事務を圧縮するのが当社のアプローチ。既存のパソコンとGoogle Workspace等の汎用ツールの上に、内製化しやすい形で構築します。",
        "points": [
            ("受発注・納期管理の自動化", "メール・FAXで届く注文をAIが台帳へ自動登録し、納期一覧を自動更新。抜け漏れと確認電話を減らします。"),
            ("請求・支払業務の効率化", "納品実績から請求書を自動生成し、支払照合も半自動化。月末の事務負担を数分の一にします。"),
            ("作業記録・図面情報の整理", "作業日報や図面・仕様書をAIで整理・検索可能にし、「前回どう作ったか」を一瞬で呼び出せます。"),
        ],
        "access": "渋谷オフィスから墨田区内へは電車で1本。工場の稼働に合わせた訪問時間で伺います。",
        "ward_faq": ("ITにかけられる予算が大きくありません。", "まず無料簡易診断（オンライン・約2時間）で効果の目安をご確認ください。当社は納品後のサブスクリプション費用を頂かないプロジェクト型で、不要なSaaSの解約提案も行うため、トータルの固定費はむしろ下がるケースがあります。"),
        "desc": "墨田区のAI導入支援・AIコンサルティングなら株式会社シクミ。ものづくり中小企業の受発注・請求・日報を駐在型AIコンサルが自動化。内製化まで支援します。",
        "neighbors": ["taito", "koto", "toshima", "chuo"],
        "area_note": "錦糸町・両国のオフィス／商業、押上・向島の観光、八広・京島・立花・東墨田のものづくり事業者まで",
        "areas": ["錦糸", "太平", "江東橋", "亀沢", "緑", "立川", "菊川", "両国", "千歳", "石原", "本所", "東駒形", "吾妻橋", "業平", "横川", "押上", "向島", "東向島", "堤通", "墨田", "八広", "京島", "文花", "立花", "東墨田"],
    },
    "koto": {
        "name": "江東区", "en": "KOTO",
        "lead": "湾岸の物流拠点と建設業、豊洲・門前仲町のオフィス。モノと書類が大量に動く江東区で、帳票と安全書類の処理をAIに任せ、現場を前へ進めます。",
        "industry": "江東区は湾岸部に物流倉庫が集積し、建設業・運送業の事業者も多いエリアです。入出庫帳票、配送伝票、建設業の安全書類（グリーンファイル）など、定型だが量の多い書類業務が現場管理者の時間を奪っています。1枚ずつは単純でも、月に数百枚となれば立派な「工数泥棒」。AIによる読み取り・整形・登録の自動化で、現場が回る速度を上げます。",
        "points": [
            ("入出庫・配送帳票の自動処理", "納品書・受領書・送り状をAIが読み取りデータ化。照合と台帳登録を自動化し、事務所の残業を減らします。"),
            ("建設業の安全書類・工事書類の効率化", "作業員名簿や安全書類の作成・チェックを半自動化。現場代理人が書類仕事に追われる状態を解消します。"),
            ("問い合わせ・配車連絡の整流化", "配送状況の問い合わせ対応や定型連絡の下書きをAI化し、電話対応の負担を軽減します。"),
        ],
        "access": "渋谷オフィスから江東区内へは電車で1本。倉庫・現場事務所への訪問にも対応します。",
        "ward_faq": ("現場が複数に分かれていても対応できますか？", "対応できます。月60時間の稼働枠の中で現地とリモートを柔軟に配分し、複数拠点の業務をまとめて設計します。拠点ごとにバラバラな帳票・ルールの統一もあわせてご提案します。"),
        "desc": "江東区のAI導入支援・AIコンサルティングなら株式会社シクミ。物流帳票や建設業の安全書類を駐在型AIコンサルが自動化。実装から内製化まで現場で支援します。",
        "neighbors": ["chuo", "sumida", "ota", "chiyoda"],
        "area_note": "豊洲・有明・東雲の湾岸オフィス、新木場・辰巳・青海の物流、木場・東陽町のオフィス、亀戸・大島・住吉の商店街、門前仲町・清澄白河まで",
        "areas": ["豊洲", "東雲", "有明", "青海", "辰巳", "枝川", "塩浜", "潮見", "木場", "東陽", "南砂", "北砂", "東砂", "新砂", "大島", "亀戸", "住吉", "猿江", "毛利", "扇橋", "石島", "千石", "海辺", "千田", "清澄", "白河", "三好", "平野", "常盤", "新大橋", "森下", "高橋", "佐賀", "福住", "深川", "冬木", "門前仲町", "富岡", "牡丹", "古石場", "越中島", "永代", "新木場", "夢の島", "若洲"],
    },
}

# ---------------------------------------------------------------- 共通パーツ
CSS_PATH = "/assets/site.css?v=20260908b"

# sitemap に含める固定ページ（エリア以外）。ページ追加時はここに足す
EXTRA_URLS = [
    "/industry/",
    "/industry/real-estate/",
    "/industry/manufacturing/",
    "/industry/construction/",
    "/industry/wholesale/",
    "/industry/logistics/",
    "/industry/healthcare/",
    "/industry/professional/",
    "/industry/retail-service/",
    "/service/consulting/",
    "/service/training/",
    "/subsidy/",
    "/column/",
    "/column/ai-consulting-cost/",
    "/column/ai-consulting-firms/",
    "/column/ai-gijiroku/",
    "/column/browser-automation/",
    "/column/excel-tenki/",
]

FIT_CHECKS = [
    "紙・FAX・メール添付で情報が届く業務が残っている",
    "同じ情報を、複数のシステムやExcelに転記している",
    "業務が特定の担当者に依存している（休むと止まる）",
    "月額SaaSの契約が増え続けている／使いこなせていない",
    "IT専任の担当者がいない、または1人しかいない",
    "AIツールを試したが、日常業務には定着しなかった",
    "部門・会社の統合で、情報の呼び名や置き場所がバラバラ",
    "何から始めるべきか分からないが、危機感はある",
]

KATA = [
    ("DOCUMENT", "文書を「探す・読む・整える」", "大量のPDF・契約書からの情報抽出／議事録・報告書の自動生成／長文資料の要約・整形・翻訳"),
    ("ANSWER", "社内のことを「即答する」", "社内規程・FAQに基づく質問応答／社内QAボット／新人教育・オンボーディングの効率化"),
    ("FORMAT", "情報を「社内フォーマットにする」", "紙・PDFの情報を社内資料・帳票へ自動整形／基幹システム入力用データへの変換／命名・様式の統一"),
    ("AGENT", "業務を「自動で動かす」", "ブラウザ上の業務の半自動化／Gmail・Drive等と連携した自動処理／定型業務のワークフロー自動化"),
]

STEPS = [
    ("STEP 0", "無料簡易診断", "オンライン・約2時間", "無料", "業務の概要を伺い、AI化の期待効果の目安をその場でご提示します。診断だけのご利用も歓迎です。"),
    ("STEP 1", "実地調査（AI化アセスメント）", "調査工数30〜90時間・約1〜3ヶ月", "個別お見積り", "現場で業務を棚卸しし、AI化ロードマップと削減効果の試算を納品。調査のみのご利用も可能です。"),
    ("STEP 2", "駐在型AI化支援", "準委任・月60時間・3〜6ヶ月", "個別お見積り", "ロードマップに沿って、コンサルタントが現場で手を動かしながらAI化を実行します。納品後のサブスクリプション費用はありません。"),
    ("STEP 3", "内製化（AI研修）", "4回×2.5時間", "助成金対象", "構築済みの自社業務フローを教材に、社員の皆さまが使い方と保守運用を習得。人材開発支援助成金で実質負担を大きく下げられます。"),
]

CASES = [
    ("不動産管理 A社（東京都）", "従業員10〜50名", "書類検索・契約書整形が手作業で、月額基幹システムのコストも負担に。",
     "書類の自動リネーム・名寄せ・1物件1ページ帳票の自動生成を構築し、現場に引き継ぎ。",
     "工数 月40時間削減 ＋ 基幹SaaS解約", "現地訪問5回×約2ヶ月で内製化まで完了"),
    ("不動産 B社（埼玉県）", "従業員10〜50名・M&Aに伴う情報統合", "契約書が紙・PDFでバラバラ。書類探しが属人化し、大量の紙データのSaaS移行が必要に。",
     "紙契約書を全件データ化し、自動リネーム・仕分け・横断検索の仕組みを構築。SaaS取込も半自動化。",
     "書類の属人化解消 ＋ PMIデータ移行完了", "現地訪問7回×約3ヶ月で内製化まで完了"),
]

COMMON_FAQS = [
    ("費用はどのくらいかかりますか？", "まず無料簡易診断（オンライン・約2時間）で削減効果の目安をご確認いただき、その結果に基づいて実地調査・駐在支援の稼働時間と体制を設計し、個別にお見積りします。各ステップの節目で「次に進むか」をご判断いただけ、納品後のサブスクリプション費用はありません。"),
    ("機密情報の扱いが不安です。", "秘密保持契約（NDA）を締結の上、データは業務目的の範囲でのみ扱います。AIツールは入力データが学習に利用されない法人向けプラン・設定を前提に構成します。"),
    ("現場社員の負担や反発はありませんか？", "ヒアリングは1名あたり30分〜1時間程度で、業務をしながら横で見せていただく観察が中心です。目的は人員削減ではなく、残業や面倒な作業をなくすこと。面倒な作業から当社が引き受けます。"),
    ("効果が出なかったら途中でやめられますか？", "契約は月単位の準委任です。無料診断・実地調査の各段階で「次に進むか」をご判断いただけます。"),
    ("ITに強い社員がいなくても内製化できますか？", "できます。研修は構築済みの自社業務フローの使い方・保守に絞るため、非エンジニアの方が対象です。"),
]

SUBSIDY_NOTE = "STEP 3のAI研修は、人材開発支援助成金「事業展開等リスキリング支援コース」の対象になる場合があります（中小企業：経費助成75%＋賃金助成1,000円/時）。受講料の約4分の3が助成されるため、実質負担は大きく下がります。2026年度（令和8年度）が最終年度で、訓練開始1ヶ月前までの申請が必要です。※受給可否・金額は申請結果により変動します。"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def mailto(subject):
    return "mailto:info@shikumi-co.jp?subject=" + quote(subject)



# ---------------------------------------------------------------- コンバージョン部品
DIAG_BODY = "無料簡易診断（オンライン・約2時間・無料）を希望します。\n\n会社名：\nご担当者名：\n業種：\n従業員数：\n気になっている業務・課題：\nご希望の日時（候補2〜3つ）：\n"
DOC_BODY = "サービス紹介資料（PDF）を希望します。\n\n会社名：\nご担当者名：\n業種：\n従業員数：\n"


def mailto_diag(ctx):
    return "mailto:info@shikumi-co.jp?subject=" + quote("無料簡易診断の申込（" + ctx + "）") + "&body=" + quote(DIAG_BODY)


def mailto_doc(ctx):
    return "mailto:info@shikumi-co.jp?subject=" + quote("サービス資料請求（" + ctx + "）") + "&body=" + quote(DOC_BODY)


TRUST = [
    ("40<small>時間/月</small>", "書類検索・転記の工数削減", "不動産管理会社（東京都）"),
    ("50<small>時間/月</small>", "残業削減・支援開始1ヶ月", "賃貸管理会社"),
    ("400<small>時間</small>", "定常業務の自動化で削減", "10名の事業部・代表の前職"),
]


def trust_strip():
    items = "".join(f'<div class="t-item"><p class="t-num">{n}</p><p class="t-label">{esc(l)}</p><p class="t-src">{esc(src)}</p></div>' for n, l, src in TRUST)
    return f'<div class="trust-strip"><p class="t-head">実績（資料記載の実測値）</p><div class="t-grid">{items}</div></div>'


def cta_dual(ctx):
    return f"""<div class="cta-dual">
    <a class="btn-main" href="{mailto_diag(ctx)}">無料簡易診断を申し込む →</a>
    <a class="btn-sub" href="{mailto_doc(ctx)}">サービス資料を請求する</a>
  </div>
  <p class="hero-meta">オンライン・約2時間・無料／診断だけのご利用も歓迎／駐在型のため同時にご支援できる社数には限りがあります</p>"""


def cta_mid(ctx, line="自社の業務にAIがどこまで効くか、まず数字で確かめませんか。"):
    return f"""
<section class="cta-mid">
  <p class="eyebrow">FREE CHECK</p>
  <p class="cta-mid-line">{esc(line)}</p>
  {cta_dual(ctx)}
</section>"""


def founder_note():
    return """
<section class="founder">
  <p class="eyebrow">FROM THE FOUNDER</p>
  <blockquote>AI導入は、外から提案する仕事ではなく、現場の中で手を動かす仕事だ。<br>——現場で得たこの確信が、シクミの原点です。</blockquote>
  <p class="f-bio"><b>石井 由哉</b>（代表取締役）文系出身・エンジニア未経験。IT上場企業で新規事業部を年商10億円規模に育てる傍ら、生成AIを自部署に持ち込み10名の事業部で約400時間の工数を削減。経理部門のAI化で外注していた業務を社内完結に。「提案書で終わらせない」を全メンバーの基準にしています。</p>
</section>"""


def sticky_cta(ctx):
    return f"""<div class="sticky-cta" role="complementary" aria-label="お問い合わせ">
  <a class="btn-main" href="{mailto_diag(ctx)}">無料診断を申し込む</a>
  <a class="btn-sub" href="{mailto_doc(ctx)}">資料請求</a>
</div>
"""


def final_cta(ctx, msg):
    return f"""
<section class="cta-box">
  <p class="eyebrow">CONTACT</p>
  <h2>まずは、無料の簡易診断から</h2>
  <p>{esc(msg)}</p>
  {cta_dual(ctx)}
  <p class="cta-mail">メール: info@shikumi-co.jp（1営業日以内にご返信します）</p>
</section>
"""

def jsonld(ward, canonical, faqs):
    import json
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "ProfessionalService",
                "name": "株式会社シクミ",
                "url": canonical,
                "email": "info@shikumi-co.jp",
                "description": f"{ward['name']}の中小企業向けAI導入支援・駐在型AIコンサルティング",
                "address": {"@type": "PostalAddress", "addressRegion": "東京都", "addressLocality": "渋谷区", "streetAddress": "桜丘町18-4 二宮ビル1F"},
                "areaServed": {"@type": "AdministrativeArea", "name": f"東京都{ward['name']}"},
                "serviceType": ["AI導入支援", "AIコンサルティング", "AI研修"],
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "株式会社シクミ", "item": BASE + "/"},
                    {"@type": "ListItem", "position": 2, "name": "東京都のAI導入支援", "item": BASE + "/area/tokyo/"},
                    {"@type": "ListItem", "position": 3, "name": f"{ward['name']}のAI導入支援", "item": canonical},
                ],
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs
                ],
            },
        ],
    }
    return json.dumps(graph, ensure_ascii=False)


def head(title, desc, canonical, ld):
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}/apple-touch-icon.png">
<meta property="og:site_name" content="株式会社シクミ">
<link rel="icon" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="stylesheet" href="{CSS_PATH}">
<script type="application/ld+json">{ld}</script>
</head>
<body>
<header class="site-head">
  <a class="brand" href="/"><span class="mark">仕</span>SHIKUMI</a>
  <nav><a href="/service/consulting/">AI導入支援</a><a href="/service/training/">AI研修</a><a href="/industry/">業種別</a><a href="/subsidy/">助成金</a><a href="/column/">コラム</a><a href="/area/tokyo/">対応エリア</a><a class="cta-s" href="{mailto('無料簡易診断の申込')}">相談する</a></nav>
</header>
"""


def footer(ward=None):
    links = ""
    if ward:
        nb = "".join(f'<a href="/area/tokyo/{n}/">{WARDS[n]["name"]}</a>' for n in ward["neighbors"])
        links = f'<div class="f-links"><span>近隣エリア:</span>{nb}<a href="/area/tokyo/">東京都エリア一覧</a></div>'
    return f"""<footer class="site-foot">
  {links}
  <div class="f-links"><span>サービス:</span><a href="/service/consulting/">生成AI導入支援（駐在型AIコンサル）</a><a href="/service/training/">AI研修</a><a href="/industry/">業種別AI導入支援</a><a href="/subsidy/">助成金のご案内</a><a href="/column/">コラム</a></div>
  <div class="f-co">
    <p class="f-name">株式会社シクミ（shikumi inc.）</p>
    <p>東京都渋谷区桜丘町18-4 二宮ビル1F ／ <a href="mailto:info@shikumi-co.jp">info@shikumi-co.jp</a></p>
    <p>事業内容: AI導入支援（駐在型AIコンサルティング／AI研修）・ITコンサルティング・システム開発</p>
    <p class="f-copy">© 2026 SHIKUMI INC. ／ <a href="/">トップへ戻る</a></p>
  </div>
</footer>
</body>
</html>
"""


def stats_section(w):
    c = CENSUS.get(w["name"])
    if not c:
        return ""
    total = c["全産業（S_公務を除く）"]
    inds = {k: v for k, v in c.items() if not k.startswith("全産業") and not k.startswith("非農林漁業")}
    top = sorted(inds.items(), key=lambda kv: -kv[1]["est"])[:3]
    def pct(n): return f"{n / total['est'] * 100:.1f}"
    top_txt = "・".join(f"{k}（{pct(v['est'])}%）" for k, v in top)
    pop = POP.get(w["name"])
    def ind_label(k):
        if k in INDUSTRY_LINKS:
            return '<a href="/industry/%s/">%s</a>' % (INDUSTRY_LINKS[k], esc(k))
        return esc(k)
    rows = "".join(
        f"<tr><td>{ind_label(k)}</td><td style='text-align:right'>{inds[k]['est']:,}</td><td style='text-align:right'>{pct(inds[k]['est'])}%</td><td style='text-align:right'>{inds[k]['emp']:,}</td></tr>"
        for k in FOCUS_INDUSTRIES if k in inds
    )
    return f"""
<section>
  <p class="eyebrow">DATA</p>
  <h2>{w['name']}の事業所データ</h2>
  <p>{w['name']}には民営事業所が<b>{total['est']:,}か所</b>、従業者が<b>{total['emp']:,}人</b>あります（令和3年経済センサス‐活動調査）。事業所数の構成は{top_txt}が上位。書類・転記・例外処理の多い業種の比重が高いエリアほど、AI化で削減できる工数は大きくなります。</p>
  <div class="three">
    <div class="card"><p class="k-label">POPULATION</p><p class="s-price">{pop:,}<span style="font-size:14px">人</span></p><p class="s-meta">人口（住民基本台帳・令和8年）</p></div>
    <div class="card"><p class="k-label">ESTABLISHMENTS</p><p class="s-price">{total['est']:,}<span style="font-size:14px">か所</span></p><p class="s-meta">民営事業所数（公務を除く）</p></div>
    <div class="card"><p class="k-label">EMPLOYEES</p><p class="s-price">{total['emp']:,}<span style="font-size:14px">人</span></p><p class="s-meta">従業者数（民営）</p></div>
  </div>
  <div class="tbl-wrap"><table class="tbl">
    <thead><tr><th>産業大分類</th><th style="text-align:right">事業所数</th><th style="text-align:right">構成比</th><th style="text-align:right">従業者数</th></tr></thead>
    <tbody>{rows}</tbody>
  </table></div>
  <p class="s-meta">出典: 総務省・経済産業省「<a href="https://www.e-stat.go.jp/stat-search/files?toukei=00200553&amp;tstat=000001145590" rel="noopener" target="_blank">令和3年経済センサス‐活動調査</a>」第24表（産業大分類・経営組織別 民営事業所数及び従業者数）、東京都「<a href="https://www.toukei.metro.tokyo.lg.jp/juukiy/jy-index.htm" rel="noopener" target="_blank">住民基本台帳による東京都の世帯と人口</a>」令和8年。当社が主に支援する業種を抜粋。</p>
</section>
"""


def section_common(ward_name):
    checks = "".join(f"<li>{esc(c)}</li>" for c in FIT_CHECKS)
    kata = "".join(
        f'<div class="card"><p class="k-label">{k}</p><h3>{esc(t)}</h3><p>{esc(b)}</p></div>' for k, t, b in KATA
    )
    steps = "".join(
        f'<div class="card step"><p class="k-label">{s}</p><h3>{esc(n)}</h3><p class="s-meta">{esc(m)}</p><p class="s-price">{esc(p)}</p><p>{esc(d)}</p></div>'
        for s, n, m, p, d in STEPS
    )
    cases = "".join(
        f'<div class="card case"><h3>{esc(t)}</h3><p class="s-meta">{esc(sz)}</p><p><b>課題:</b> {esc(c)}</p><p><b>支援:</b> {esc(s)}</p><p class="result">{esc(r)}</p><p class="s-meta">{esc(m)}</p></div>'
        for t, sz, c, s, r, m in CASES
    )
    return f"""
<section>
  <p class="eyebrow">STYLE</p>
  <h2>提案書で終わらせない。現場に入り、実装までやり切ります</h2>
  <p>株式会社シクミのAI導入支援は、提案書を納品して終わるコンサルでも、ツールを売って終わるベンダーでもありません。AIを使いこなすコンサルタントが貴社の現場に入り、部門を問わず業務を1から10までヒアリング。どこにAIが効くかを見極め、<b>現場で手を動かしながら実装し、社員の皆さまが自分たちで回せるようになるまで</b>を仕事とします。</p>
  <div class="three">
    <div class="card"><h3>現場主義</h3><p>現地に駐在し、自ら実装。「絵に描いた餅」で終わらせません。</p></div>
    <div class="card"><h3>部門横断</h3><p>バックオフィスから営業まで会社全体を見て、本当の無駄を見つけます。</p></div>
    <div class="card"><h3>内製化設計</h3><p>納品後のサブスク契約なし。社員が自走できる状態で「卒業」します。</p></div>
  </div>
</section>
{cta_mid(ward_name)}
<section>
  <p class="eyebrow">SOLUTION</p>
  <h2>現場でよく見つかる、AI化の「仕組みの型」</h2>
  <div class="grid2">{kata}</div>
</section>

<section>
  <p class="eyebrow">CASE</p>
  <h2>導入事例——現場で何が見え、何が変わったか</h2>
  <div class="grid2">{cases}</div>
</section>

<section>
  <p class="eyebrow">FLOW</p>
  <h2>進め方——各ステップの節目で「続けるか」を判断できます</h2>
  <div class="grid2">{steps}</div>
  <p class="s-meta">料金は無料診断・実地調査の結果に基づき、稼働時間・体制を設計して個別にお見積りします。納品後のサブスクリプション費用はありません。</p>
  <div class="note"><p><b>助成金のご案内:</b> {esc(SUBSIDY_NOTE)} <a href="/subsidy/">→ 助成金の詳細と負担額シミュレーター</a></p></div>
</section>
{founder_note()}
"""


def checks_section(ward_name):
    checks = "".join(f"<li>{esc(c)}</li>" for c in FIT_CHECKS)
    return f"""
<section>
  <p class="eyebrow">CHECK</p>
  <h2>こんな状態に心当たりはありませんか</h2>
  <p class="lead-s">ひとつでも当てはまれば、{esc(ward_name)}の貴社にもAI化で削減できる工数が眠っている可能性があります。</p>
  <ul class="checks">{checks}</ul>
  <div class="conclusion"><p class="c-label">WHY</p><p>共通の原因はAIの性能ではありません。<b>「業務を作り変える人」が現場にいないこと</b>です。だから私たちは、業務の作り変えにコミットするAI人材を、外から現場に入れます。</p></div>
</section>
"""


def cta(ward_name):
    return final_cta(ward_name, f"オンライン・約2時間で、貴社のAI化の期待効果の目安をご提示します。診断だけのご利用も歓迎です。{ward_name}の企業さまからのご相談をお待ちしています。")


def build_ward(slug, w):
    canonical = f"{BASE}/area/tokyo/{slug}/"
    title = f"{w['name']}のAI導入支援・AIコンサルティング｜駐在型の株式会社シクミ"
    faqs = COMMON_FAQS[:3] + [w["ward_faq"]] + COMMON_FAQS[3:]
    ld = jsonld(w, canonical, faqs)
    points = "".join(f'<div class="card"><h3>{esc(t)}</h3><p>{esc(b)}</p></div>' for t, b in w["points"])
    faq_html = "".join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in faqs)
    html = head(title, w["desc"], canonical, ld)
    html += f"""<main>
<nav class="crumbs" aria-label="パンくず"><a href="/">トップ</a> › <a href="/area/tokyo/">東京都のAI導入支援</a> › <span>{w['name']}</span></nav>

<div class="hero">
  <p class="eyebrow">AI CONSULTING IN {w['en']}</p>
  <h1>{w['name']}のAI導入支援・<br class="sp">駐在型AIコンサルティング</h1>
  <p class="lead">{esc(w['lead'])}</p>
  {trust_strip()}
  {cta_dual(w['name'])}
  <p class="hero-meta">{esc(w['access'])}</p>
</div>
{checks_section(w['name'])}
<section>
  <p class="eyebrow">LOCAL</p>
  <h2>{w['name']}の事業環境と、AIが効くポイント</h2>
  <p>{esc(w['industry'])}</p>
  <div class="three">{points}</div>
</section>
{stats_section(w)}
{section_common(w['name'])}
<section>
  <p class="eyebrow">AREA</p>
  <h2>{w['name']}の主な対応エリア</h2>
  <p>{esc(w['area_note'])}、{w['name']}内全域に対応しています。渋谷区桜丘町のオフィスから直接伺います。</p>
  <ul class="area-list">{''.join(f'<li>{esc(a)}</li>' for a in w['areas'])}</ul>
  <p class="s-meta">記載のないエリア・近隣区もお気軽にご相談ください。</p>
</section>
<section>
  <p class="eyebrow">FAQ</p>
  <h2>よくあるご質問</h2>
  <div class="faqs">{faq_html}</div>
</section>
{cta(w['name'])}
</main>
{sticky_cta(w['name'])}
"""
    html += footer(w)
    outdir = os.path.join(ROOT, "area", "tokyo", slug)
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    return canonical


def build_hub():
    canonical = f"{BASE}/area/tokyo/"
    title = "東京都のAI導入支援・AIコンサルティング 対応エリア｜株式会社シクミ"
    desc = "東京都の中小企業向けAI導入支援・駐在型AIコンサルティングなら株式会社シクミ。渋谷オフィスから23区・都内全域の現場へ直接伺い、実装から内製化まで支援。無料簡易診断受付中。"
    import json
    ld = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "ProfessionalService", "name": "株式会社シクミ", "url": canonical, "email": "info@shikumi-co.jp",
             "description": "東京都の中小企業向けAI導入支援・駐在型AIコンサルティング",
             "address": {"@type": "PostalAddress", "addressRegion": "東京都", "addressLocality": "渋谷区", "streetAddress": "桜丘町18-4 二宮ビル1F"},
             "areaServed": {"@type": "AdministrativeArea", "name": "東京都"},
             "serviceType": ["AI導入支援", "AIコンサルティング", "AI研修"]},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "株式会社シクミ", "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": "東京都のAI導入支援", "item": canonical}]},
        ],
    }, ensure_ascii=False)
    cards = "".join(
        f'<a class="card ward-card" href="/area/tokyo/{slug}/"><h3>{w["name"]}</h3><p>{esc(w["points"][0][0])} など</p><span class="more">詳しく見る →</span></a>'
        for slug, w in WARDS.items()
    )
    html = head(title, desc, canonical, ld)
    html += f"""<main>
<nav class="crumbs" aria-label="パンくず"><a href="/">トップ</a> › <span>東京都のAI導入支援</span></nav>

<div class="hero">
  <p class="eyebrow">AI CONSULTING IN TOKYO</p>
  <h1>東京都のAI導入支援・<br class="sp">駐在型AIコンサルティング</h1>
  <p class="lead">株式会社シクミは、渋谷区桜丘町のオフィスを拠点に、東京都内の中小企業の現場へ直接伺うAI導入支援を行っています。AI人材が現場に駐在し、業務のヒアリングから実装・内製化までを一気通貫で実行。ツールを売って終わりにせず、貴社が自分たちで回せる「仕組み」を残します。</p>
  {trust_strip()}
  {cta_dual('東京都')}
  <p class="hero-meta">東京都内全域対応（下記以外のエリアもご相談ください）</p>
  <p class="hero-meta">東京都の民営事業所は{CENSUS['東京都']['全産業（S_公務を除く）']['est']:,}か所・従業者{CENSUS['東京都']['全産業（S_公務を除く）']['emp']:,}人（令和3年経済センサス‐活動調査）。各区ページに区別の事業所データを掲載しています。</p>
</div>

<section>
  <p class="eyebrow">AREA</p>
  <h2>対応エリア（東京23区）</h2>
  <p class="lead-s">各エリアの産業特性に合わせた支援内容をご紹介しています。掲載のない区・市部・全国も対応します。</p>
  <div class="three">{cards}</div>
</section>
{checks_section('東京都')}
{section_common('東京都')}
{cta('東京都')}
</main>
{sticky_cta('東京都')}
"""
    html += footer()
    outdir = os.path.join(ROOT, "area", "tokyo")
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    return canonical


def build_sitemap(urls):
    items = "\n".join(
        f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls
    )
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{items}
</urlset>
"""
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)


if __name__ == "__main__":
    urls = [BASE + "/"] + [BASE + p for p in EXTRA_URLS]
    urls.append(build_hub())
    for slug, w in WARDS.items():
        urls.append(build_ward(slug, w))
    build_sitemap(urls)
    print(f"generated: hub + {len(WARDS)} wards + sitemap.xml ({len(urls)} URLs)")
