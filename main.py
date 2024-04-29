import pygame
from pygame.locals import *
import sys


# ブロック描写用
def map_make(map_data, screen, map_now, size):
    block_y = 0
    block_x = 0
    while block_y < 20:
        while block_x < 200:
            if map_data[block_y][block_x] == 1:
                pygame.draw.rect(screen, (0, 0, 255), Rect(map_now + (size * block_x), (size * block_y), size, size))
            elif map_data[block_y][block_x] == 2:
                pygame.draw.rect(screen, (255, 0, 0), Rect(map_now + (size * block_x), (size * block_y), size, size))
            block_x += 1
        block_y += 1
        block_x = 0


# 当たり判定
def map_check(map_data, x_now, y_now, next_x, next_y, size):
    x_arr = x_now / size
    y_arr = y_now / size
    return map_data[int(y_arr + next_y)][int(x_arr + next_x)]


# リスタート状態
def restart(setup):
    map_now = setup[0]
    player_x_now = setup[1]
    player_y_now = setup[2]
    up_or_down = setup[3]
    jump = setup[4]
    return map_now, player_x_now, player_y_now, up_or_down, jump


def main():
    # 各変数初期化
    (w, h) = (1000, 520)  # 画面サイズ
    map_now = 0  # 背景初期座標
    player_x_now = 400  # プレイヤー初期座標　縦
    player_y_now = 200  # プレイヤー初期座標　横
    x_save = 400  # スペース入力時のx座標の保存
    block = 1  # ブロック
    death = 2  # 死亡
    jump = False  # ジャンプの状態　bool型
    box_size = 26  # アイテム、ボックスのサイズ 正方形
    player_direction = 1  # プレイヤー進行方向　(奇数:右向き 偶数:左向き)
    stage_setup = [0, 400, 200, 1, False]  # 初期マップデータ、キャラクター状態
    pygame.init()  # pygame初期化
    pygame.display.set_mode((w, h))  # window呼び出し
    pygame.display.set_caption("main")  # windowタイトル
    screen = pygame.display.get_surface()  # windowの定義（多分）

    # テキストデータからの当たり判定の読み込み
    tmp = open('map.txt', 'r')
    map_data = []
    while True:
        data_y = tmp.readline()
        if data_y == '':
            break
        data_in = data_y.split()
        data_x = [int(i) for i in data_in]
        map_data.append(data_x)

    while True:
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, w, h))  # マップの表示
        map_make(map_data, screen, map_now, box_size)  # ブロックの表示
        pressed_key = pygame.key.get_pressed()  # キー入力条件分岐

        # キー入力　left
        if pressed_key[K_a]:
            if int(map_check(map_data, player_y_now - map_now + box_size / 2, player_x_now, -1, 0, box_size)) != 1:
                if map_now < 0 and player_y_now == 366:
                    map_now += 1
                elif player_y_now > 5:
                    player_y_now -= 1
                player_direction = 2

        # キー入力　right
        if pressed_key[K_d]:
            if int(map_check(map_data, player_y_now - map_now - box_size / 2, player_x_now, 1, 0, box_size)) != block:
                if map_now > -4100 and player_y_now == 366:
                    map_now -= 1
                elif player_y_now < 990:
                    player_y_now += 1
            player_direction = 1

        # スペース入力の際にジャンプ状態に
        if pressed_key[K_SPACE]:
            if not jump:
                # 落下時のジャンプを防止
                if x_save == player_x_now:
                    if map_check(map_data, player_y_now - map_now, player_x_now - box_size / 2,
                                 0, 1, box_size) == block:
                        jump = True

        # 足元にブロックないときに落下
        if not jump:
            # 落下
            if map_check(map_data, player_y_now - map_now,
                         player_x_now - box_size / 2, 0, 1, box_size) != block:
                if map_check(map_data, player_y_now - map_now,
                             player_x_now - box_size / 2, 0, 1, box_size) != block:
                    player_x_now += 1
            # 着地時に高さのデータを保存
            if map_check(map_data, player_y_now - map_now, player_x_now - box_size / 2, 0, 1, box_size) == block:
                x_save = player_x_now

        # 上方向のジャンプ処理
        if jump:
            player_x_now -= 1
            if x_save - player_x_now > 150:
                jump = False
            if map_check(map_data, player_y_now - map_now,
                         player_x_now + box_size / 2, 0, -1, box_size) == 1:
                if map_check(map_data, player_y_now - map_now,
                             player_x_now + box_size / 2, 0, -1, box_size) == 1:
                    jump = False

        # 死亡時のリセット判定
        if map_check(map_data, player_y_now - map_now, player_x_now, 0, 0, box_size) == death:
            map_now, player_x_now, player_y_now, up_or_down, jump = restart(stage_setup)

        # 円を描画
        if player_direction == 1:
            pygame.draw.circle(screen, (0, 255, 0), (player_y_now, player_x_now), box_size / 2)
        elif player_direction == 2:
            pygame.draw.circle(screen, (0, 255, 0), (player_y_now, player_x_now), box_size / 2)

        pygame.display.update()  # 画面更新
        pygame.time.wait(1)  # 更新時間間隔

        # イベント処理
        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                tmp_y, tmp_x = event.pos
            if event.type == QUIT:  # 画面の閉じるボタンを押したとき
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:  # キーを押したとき
                if event.key == K_ESCAPE:  # ESCキーなら終了
                    pygame.quit()
                    sys.exit()


if __name__ == "__main__":
    main()
