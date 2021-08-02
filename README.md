# dog_sample

DOGを操作するためのGUIアプリのサンプルプログラムです。
GUIアプリを作るためにPySimpleGUIというモジュールを使用しています。
Pythonや音声合成に必要なパッケージをまとめるためにDockerを使用しています。

# インストール方法
Githubから本リポジトリをクローンし、その後、Dockerイメージを作ります。コマンドは次の通り：
```
git clone https://github.com/social-robotics-lab/dog_sample.git
cd dog_sample
docker build -t dog_sample .
```

DockerでGUIアプリを表示をさせるには、VcXsrv[https://sourceforge.net/projects/vcxsrv/]というソフトをインストールし、Xlaunchを起動しておく必要があります。

# 実行の仕方
Xlaunchを起動しておきます。実行時の設定はすべてデフォルトでOKです。
Xlaunchを起動すると、タスクトレイに「X」みたいなのが表示されます。一度起動したら、PCを再起動するまでは起動しっぱなしになります。


Dockerイメージからコンテナを作成して実行します。
コンテナ内でサンプルプログラムを実行します。
コマンドは次の通り：
```
docker run --rm -it --name dog_sample --mount type=bind,source="$(pwd)"/src,target=/tmp dog_sample /bin/bash
python3 sample.py --host DOGのIP
```