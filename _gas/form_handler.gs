/**
 * シクミHP フォーム受付（お問い合わせ／資料ダウンロード）— メール通知のみ版
 *
 * 使い方
 * 1. https://script.google.com/ を開き「新しいプロジェクト」
 * 2. このコードを貼り付けて保存（プロジェクト名は「シクミHPフォーム」など）
 * 3. 右上「デプロイ」→「新しいデプロイ」→ 種類「ウェブアプリ」
 *    - 次のユーザーとして実行：自分
 *    - アクセスできるユーザー：全員
 *    → 初回は権限の承認画面が出るので許可する
 * 4. 発行された「ウェブアプリのURL」（…/exec）を HP の assets/form.js の FORM_ENDPOINT に設定
 */
var NOTIFY_TO = 'info@shikumi-co.jp, yukiya.ishii@shikumi-co.jp';
var FROM_NAME = '株式会社シクミ HP';
var DOC_URLS = {
  tool: 'https://drive.google.com/XXXXXXXX' // メール一斉送信ツール 詳細資料のリンク共有URLに差し替え
};

function doPost(e) {
  try {
    var p = e.parameter || {};
    var kind = p.kind === 'download' ? 'download' : 'contact';
    notify_(kind, p, new Date());
    if (kind === 'download' && p.email) sendDoc_(p);
    return out_({ ok: true });
  } catch (err) {
    return out_({ ok: false, error: String(err) });
  }
}

function doGet() { return out_({ ok: true, ping: 'shikumi-form' }); }

function notify_(kind, p, now) {
  var label = kind === 'download' ? '資料ダウンロード' : 'お問い合わせ';
  var subject = '【HP】' + label + '：' + (p.company || '会社名なし') + ' ' + (p.name || '');
  var lines = [
    '受信日時：' + Utilities.formatDate(now, 'Asia/Tokyo', 'yyyy-MM-dd HH:mm'),
    '会社名：' + (p.company || ''),
    'お名前：' + (p.name || ''),
    'メール：' + (p.email || '')
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
  var body = [
    (p.name || '') + ' 様',
    '',
    '株式会社シクミです。資料のご請求ありがとうございます。',
    '以下のリンクから資料をご覧いただけます。',
    '',
    '■ メール一斉送信ツール 詳細資料',
    DOC_URLS.tool,
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
