/* シクミHP フォーム送信（お問い合わせ／資料DL）
   GASのウェブアプリURLを FORM_ENDPOINT に設定すると、スプレッドシート記録＋通知メールになります。
   未設定の間は、入力内容を本文に入れたメール作成画面（info@shikumi-co.jp 宛）を開きます。 */
(function () {
  var FORM_ENDPOINT = '';
  var LABELS = { company: '会社名', name: 'お名前', email: 'メール', tel: '電話', industry: '業種', doc: '希望資料', note: 'ひとこと', type: '相談の種類', body: '相談内容' };
  document.querySelectorAll('form.form').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var fd = new FormData(f);
      fd.append('page', location.href);
      var kind = fd.get('kind') === 'download' ? '資料ダウンロード希望' : 'お問い合わせ';
      if (!FORM_ENDPOINT) {
        var lines = [];
        fd.forEach(function (v, k) { if (LABELS[k]) lines.push(LABELS[k] + '：' + v); });
        var href = 'mailto:info@shikumi-co.jp?subject=' + encodeURIComponent('【HP】' + kind) + '&body=' + encodeURIComponent(lines.join('\n') + '\n\n送信元：' + location.href);
        window.location.href = href;
        f.setAttribute('data-sent', '1');
        return;
      }
      var btn = f.querySelector('button[type="submit"]');
      if (btn) btn.disabled = true;
      fetch(FORM_ENDPOINT, { method: 'POST', mode: 'no-cors', body: fd })
        .then(function () { f.setAttribute('data-sent', '1'); })
        .catch(function () { f.setAttribute('data-sent', '2'); })
        .then(function () { if (btn) btn.disabled = false; });
    });
  });
})();
