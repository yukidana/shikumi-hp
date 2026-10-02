/**
 * シクミHP フォーム受付（お問い合わせ／資料ダウンロード）
 *
 * 使い方
 * 1. Googleスプレッドシートを新規作成（例：シクミ_HP問い合わせ）
 * 2. 拡張機能 → Apps Script を開き、このコードを貼り付けて保存
 * 3. デプロイ → 新しいデプロイ → 種類「ウェブアプリ」
 *    - 次のユーザーとして実行：自分
 *    - アクセスできるユーザー：全員
 * 4. 発行された「ウェブアプリのURL」を HP の assets/form.js の FORM_ENDPOINT に設定
 *
 * シートは種別ごとに自動で作られます（contact / download）。
 */
var NOTIFY_TO = 'info@shikumi-co.jp, yukiya.ishii@shikumi-co.jp';
var FROM_NAME = '株式会社シクミ HP';
var DOC_URLS = {
  tool: 'https://drive.google.com/XXXXXXXX' // メール一斉送信ツール 詳細資料のURLに差し替え
};

function doPost(e) {
  try {
    var p = e.parameter || {};
    var kind = p.kind === 'download' ? 'download' : 'contact';
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sh = ss.getSheetByName(kind) || createSheet_(ss, kind);
    var now = new Date();
    var row = kind === 'download'
      ? [now, p.company || '', p.name || '', p.email || '', p.industry || '', p.doc || '', p.note || '', p.page || '']
      : [now, p.company || '', p.name || '', p.email || '', p.tel || '', p.type || '', p.body || '', p.page || ''];
    sh.appendRow(row);
    notify_(kind, p, now);
    if (kind === 'download' && p.email) sendDoc_(p);
    return out_({ ok: true });
  } catch (err) {
    return out_({ ok: false, error: String(err) });
  }
}

function doGet() { return out_({ ok: true, ping: 'shikumi-form' }); }

function createSheet_(ss, kind) {
  var sh = ss.insertSheet(kind);
  var header = kind === 'download'
    ? ['受信日時', '会社名', 'お名前', 'メール', '業種', '希望資料', 'ひとこと', '送信元ページ']
    : ['受信日時', '会社名', 'お名前', 'メール', '電話', '相談の種類', '相談内容', '送信元ページ'];
  sh.appendRow(header);
  sh.setFrozenRows(1);
  return sh;
}

function notify_(kind, p, now) {
  var label = kind === 'download' ? '資料ダウンロード' : 'お問い合わせ';
  var subject = '【HP】' + label + '：' + (p.company || '会社名なし') + ' ' + (p.name || '');
  var lines = [
    '受信日時：' + Utilities.formatDate(now, 'Asia/Tokyo', 'yyyy-MM-dd HH:mm'),
    '会社名：' + (p.company || ''),
    'お名前：' + (p.name || ''),
    'メール：' + (p.email || ''),
  ];
  if (kind === 'download') {
    lines.push('業種：' + (p.industry || ''), '希望資料：' + (p.doc || ''), 'ひとこと：' + (p.note || ''));
  } else {
    lines.push('電話：' + (p.tel || ''), '相談の種類：' + (p.type || ''), '', '相談内容：', p.body || '');
  }
  lines.push('', '送信元：' + (p.page || ''));
  MailApp.sendEmail({ to: NOTIFY_TO, subject: subject, body: lines.join('\n'), name: FROM_NAME, replyTo: p.email || '' });
}

function sendDoc_(p) {
  var url = DOC_URLS.tool;
  var body = [
    (p.name || '') + ' 様',
    '',
    '株式会社シクミです。資料のご請求ありがとうございます。',
    '以下のリンクから資料をご覧いただけます。',
    '',
    '■ メール一斉送信ツール 詳細資料',
    url,
    '',
    '資料を見て気になった点は、このメールに返信いただければ石井が直接お答えします。',
    '',
    '――――――――――――――――',
    '株式会社シクミ',
    '東京都渋谷区桜丘町18-4 二宮ビル1F',
    'info@shikumi-co.jp',
    'https://shikumi-co.jp/'
  ].join('\n');
  MailApp.sendEmail({ to: p.email, subject: '【シクミ】資料をお送りします', body: body, name: '株式会社シクミ', replyTo: 'info@shikumi-co.jp' });
}

function out_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
