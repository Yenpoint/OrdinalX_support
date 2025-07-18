# OrdinalX NFT API サービス - サンプルコード

このリポジトリには、BSVブロックチェーン上のOrdinalX NFT APIサービスと連携するためのPythonサンプルコードが含まれています。BSV送金、NFT作成、NFT送信、NFT焼却などの様々な操作をPaymailアドレス経由で実行する方法を示しています。

## 機能

- **BSV送金**: 任意のPaymailアドレスにBSVを送金
- **NFT作成**: カスタムコンテンツでNFTを作成
- **NFT送信**: PaymailアドレスにNFTを送信
- **NFT焼却**: NFTを永続的に破棄
- **認証**: CSRF保護付きのJWTベース認証
- **セッション管理**: 適切なHTTPセッション処理

## 前提条件

- Python 3.x
- OrdinalX API認証情報
- 十分な残高のあるBSVウォレット

## インストール

1. リポジトリをクローンします：
```bash
git clone https://github.com/Yenpoint/OrdinalX_support.git
cd OrdinalX_support/sample
```

2. 仮想環境を作成します：
```bash
python3 -m venv .venv
```

3. 仮想環境をアクティベートします：
```bash
# Linux/macOS
source .venv/bin/activ.envate

# Windows
.venv\Scripts\activate
```

4. 依存関係をインストールします：
```bash
pip install -r requirements.txt
```

5. `.env.example`ファイルをコピーして`.env`ファイルを作成し、環境変数を設定します：
```bash
cp .env.example .env
```

`.env`ファイルを編集して、実際の認証情報を設定してください：
```bash
ORDINALX_SERVER_FQDN=your-server-hostname
ORDINALX_USERNAME=your-username
ORDINALX_PASSWORD=your-password
```

## 使用方法

### Paymail経由でBSVを送金

任意のPaymailアドレスにBSVを送金：

```bash
python send_bsv_paymail.py -d recipient@paymail.com -a 1000
```

オプション:
- `-d, --destination`: 送金先Paymailアドレス（デフォルト: jo7ueb@handcash.io）
- `-a, --amount`: サトシ単位での送金額（デフォルト: 22）
- `-v, --verbose`: 詳細ログを有効化

### NFT作成

カスタムコンテンツでNFTを作成：

```bash
python create_nft.py -f image.png -d recipient@paymail.com
```

オプション:
- `-f, --file`: NFTコンテンツファイルのパス（デフォルト: yenpoint_logo.png）
- `-d, --destination`: 送信先Paymailアドレス（オプション、未指定時は作成者宛）
- `-v, --verbose`: 詳細ログを有効化

### Paymail経由でNFTを送信

既存のNFTをPaymailアドレスに送信：

```bash
python send_nft_paymail.py -d recipient@paymail.com -o <nft_origin>
```

オプション:
- `-d, --destination`: 送信先Paymailアドレス（必須）
- `-o, --origin`: NFTのオリジン識別子（必須）
- `-v, --verbose`: 詳細ログを有効化

### NFT焼却

NFTを永続的に破棄：

```bash
python burn_nft.py -o <nft_origin>
```

オプション:
- `-o, --origin`: 焼却するNFTのオリジン識別子（必須）
- `-v, --verbose`: 詳細ログを有効化

## アーキテクチャ

### コアコンポーネント

- **`utils.py`**: 認証とセッション管理のためのコアユーティリティ
  - `load_environment()`: .envファイルから環境変数を読み込み
  - `open_session()`: CSRFトークン付きHTTPセッションを確立
  - `get_jwt_token(session)`: 認証してJWTトークンを取得

### 認証フロー

1. `load_environment()`で環境変数を読み込み
2. `open_session()`でセッションを作成しCSRFトークンを取得
3. `get_jwt_token(session)`でJWTトークンを取得
4. JWTトークンを使用して認証済みAPI呼び出しを実行

### APIエンドポイント

- **BSV送金**: `POST /api/v1/bsv/paymail/send`
- **NFT作成**: `POST /api/v1/nft/create`
- **NFT送信**: `POST /api/v1/nft/paymail/send`
- **NFT焼却**: `POST /api/v1/nft/burn`

## エラーハンドリング

すべてのスクリプトには適切なエラーハンドリングとログ機能が含まれています：
- HTTPステータスコードによる成功/失敗チェック
- 詳細なエラーメッセージをログ出力
- 成功時にはトランザクションIDを提供
- ブロックチェーンエクスプローラー（whatsonchain.com）へのリンクを含む

## 依存関係

- `requests`: API呼び出し用HTTPライブラリ
- `python-dotenv`: 環境変数管理

## ライセンス

このプロジェクトは教育目的および統合目的のサンプルコードとして提供されています。

## サポート

API仕様書やサポートについては、OrdinalX NFT APIのSwaggerを参照するか、GitHub issueにてお問い合わせください。