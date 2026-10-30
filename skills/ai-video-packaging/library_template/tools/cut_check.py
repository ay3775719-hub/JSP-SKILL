# AI 剪辑包装 Skill · 作者：大象学长（全网同名）· CC BY-NC 4.0
# 查剪辑点前后的「脏帧」：首帧尾帧不干净（少效果、跳一下、闪一下）
# 原理：相邻两帧画面差。一个干净的硬切只在切点那一帧变一次；切点前后 1–3 帧内又变一大下 = 脏帧。
# 用法：python3 cut_check.py 渲染.mp4 渲染起帧 [切点帧 ...]   （切点不写就只按画面差找「连着两次大变化」）
import subprocess, sys

W, H = 96, 54


def frames(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-vf', f'scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'],
                         capture_output=True, check=True).stdout
    n = W * H
    return [raw[i:i + n] for i in range(0, len(raw) - n + 1, n)]


def check(path, start, cuts=(), big=18.0, near=3):
    f = frames(path)
    d = [sum(abs(x - y) for x, y in zip(a, b)) / (W * H) for a, b in zip(f, f[1:])]   # d[i] = 第 i 帧 → 第 i+1 帧的变化
    jumps = [i + 1 for i in range(len(d)) if d[i] >= big]    # 发生大变化的帧（相对渲染起点）
    out = []
    for j in jumps:                                          # 两次大变化挨得太近：中间那几帧就是脏帧
        close = [k for k in jumps if 0 < k - j <= near]
        if close: out.append((start + j, start + close[0], round(d[j - 1], 1), round(d[close[0] - 1], 1)))
    off = [(c, min(abs(c - (start + j)) for j in jumps)) for c in cuts if jumps]
    off = [(c, k) for c, k in off if 0 < k <= near]          # 切点附近有大变化，但不在切点上：效果早 / 晚了几帧
    return out, off


if __name__ == '__main__':
    p, s = sys.argv[1], int(sys.argv[2])
    pairs, off = check(p, s, [int(x) for x in sys.argv[3:]])
    for a, b, da, db in pairs: print('脏帧：%d 变一次（%.1f），%d 又变一次（%.1f）' % (a, da, b, db))
    for c, k in off: print('切点 %d：最近的大变化差了 %d 帧' % (c, k))
    if not pairs and not off: print('干净')
