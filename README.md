## LDAP Auth for nginx
nginxでLDAP認証をするための.confファイルと認証用バックエンドのコンテナ  
リバースプロキシの下にあるページをCNとパスワードの認証を要求するページにリダイレクトすることができます。  
ldapwhoamiコマンドの終了ステータスで認証の成功/失敗を判定します。

### Usage
1. リポジトリをクローンします。
```
git clone https://git.3naly.xyz/minawa/LDAP_for_nginx.git
```

2. docker-compose.ymlのポートや環境変数を書き換えます。  
デフォルトのポートは8811にしています。  
```
cd LDAP_for_nginx
```

* LDAP_HOST : LDAPサーバーのホストアドレス
* LDAP_PORT : LDAPサーバーのポート
* LDAP_BASE_DN : LDAPのベースDN 
  - ou=group,dc=hoge,dc=xyz など
* REDIRECT: ログイン成功時のリダイレクト先

3. コンテナの起動
```
docker-compose up -d
```

4. nginx設定ファイルの設置  
example.confを参考にして.confファイルを作成し、/etc/nginx/conf.dに配置します。  
その後、nginxを再起動します。

```
sudo nginx -s reload
```
