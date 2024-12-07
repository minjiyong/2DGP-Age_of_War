world = [[] for _ in range(4)]
collision_pairs = {}    #빈 딕셔너리 {'key' : [ [A list] [B list] ]}

def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        collision_pairs[group] = [[], []]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)

def add_object(o, depth = 0):
    world[depth].append(o)

def add_objects(ol, depth = 0):
    world[depth] += ol

def get_objects(depth=None):
    """
    특정 레이어나 전체 레이어에서 객체를 가져오는 함수.
    - depth가 None이면 모든 레이어의 객체를 반환.
    - 특정 depth 값이 주어지면 해당 레이어의 객체만 반환.
    """
    if depth is None:
        return [obj for layer in world for obj in layer]
    else:
        return world[depth] if 0 <= depth < len(world) else []


def update():
    for layer in world:
        for o in layer:
            o.update()


def render():
    for layer in world:
        for o in layer:
            o.draw()

def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]: pairs[0].remove(o)
        if o in pairs[1]: pairs[1].remove(o)

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)     #월드 리스트에서 삭제
            remove_collision_object(o)      #collision_pairs 에서 삭제
            del o           #메모리에서 객체 자체를 삭제
            return
    raise ValueError('Cannot delete non existing object')


def clear():
    for layer in world:
        layer.clear()



# fill here
def collide(a, b, attack=False):
    """
    두 객체 a와 b의 충돌을 확인하는 함수.
    - attack: True인 경우 공격 박스 기준으로 충돌 검사.
    """
    if attack:
        al, ab, ar, at = a.get_attack_bb()  # a의 공격 범위 박스
    else:
        al, ab, ar, at = a.get_bb()  # a의 피격 범위 박스

    bl, bb, br, bt = b.get_bb()  # b의 피격 범위 박스

    # 충돌하지 않는 조건들
    if ar < bl or al > br or at < bb or ab > bt:
        return False

    return True


def handle_collisions():
    """
    게임 월드에 등록된 충돌 정보를 바탕으로 실제 충돌 검사를 수행.
    """
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if a == None or b == None: return
                if collide(a, b, attack=True):  # 공격 범위 충돌 검사
                    a.handle_attack_collision(group, b)  # 공격 충돌 처리
                    b.handle_hit_collision(group, a)  # 피격 처리
                if collide(b, a, attack=True):  # 공격 범위 충돌 검사
                    a.handle_hit_collision(group, b)  # 공격 충돌 처리
                    b.handle_attack_collision(group, a)  # 피격 처리