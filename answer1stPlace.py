import sys
from math import sqrt, pow
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.



class vector_pod(object):
    def __init__(self, coord = None):
        if coord:
            self.x = coord[0]
            self.y = coord[1]
        else:
            self.x = 0
            self.y = 0

    def norm(self):
        return sqrt(pow(self.x,2)+pow(self.y,2))

    def set(self, coord):
        self.x = coord[0]
        self.y = coord[1]

    def __str__(self):
        return "x={} y={} norm={}".format(self.x, self.y, self.norm())

    def __add__(self, other):
        return (vector_pod((self.x+other.x, self.y+other.y)))

    def __sub__(self, other):
        return (vector_pod((other.x - self.x, other.y - self.y)))

    def __mul__(self, other):
        return (vector_pod((int(self.x*other) , int(self.y*other))))

    def dist(self, other):
        return (other - self).norm()

    def next_speed(self, thrust):
        return self*((self.norm()+thrust)*.9/self.norm())




class pod(object):
    def __init__(self):
        self.flag = False
        self.pos = vector_pod()
        self.velocity = vector_pod()
        self.strategy = None

    def set(self, coord):
        self.pos.set(coord[0:2])
        self.velocity.set(coord[2:4])
        self.flag = coord[4]

    def next_turn(self):
        return self.pos+self.velocity

    def __str__(self):
        return "pos = {} velocity = {}".format(self.pos, self.velocity)


    def results(self):
        return self.strategy.compute(self)




class flag(object):
    def __init__(self):
        self.pod = None
        self.pos = vector_pod()
        self.velocity = vector_pod()

    def set_pos(self, coord):
        self.pos.set(coord)
        if self.is_captured() is False:
            self.pod = None

    def set_vel(self, velocity):
        self.velocity.set(velocity)

    @property
    def true_pos(self):
        if self.pod:
            return self.pod.pos
        else:
            return self.pos

    @property
    def true_velo(self):
        if self.pod:
            return self.pod.velocity
        else:
            return self.velocity

    def is_captured(self):
        return self.pos.x == -1 and self.pos.y == -1

    def __str__(self):
        return "pos = {} velocity = {}".format(self.true_pos, self.true_velo)


enemy_flag = flag()
our_flag = flag()

our_pods = [pod (), pod ()]
enemy_pods = [pod (), pod ()]

our_camp = vector_pod()
turn_number = 1


class strategy_def(object):
    def compute(self, pod):
        need_to_boost = our_flag.pod
        if not our_flag.pod:
            best_pod = min(enemy_pods, key=lambda x: (x.pos+x.velocity).dist(our_flag.pos))
            tmp_pos = (best_pod.pos + our_flag.pos)*0.5
            return "{} {} {}".format(tmp_pos.x, tmp_pos.y , 100)
        else:
            futur_enemy_pos = our_flag.pod.next_turn()
            futur_self_pos = pod.next_turn()
            if (futur_enemy_pos.dist(futur_self_pos) > 900 and futur_enemy_pos.dist(futur_self_pos) < 1300):
                need_to_boost = True
            return "{} {} {}".format(our_flag.true_pos.x+our_flag.true_velo.next_speed(100).x, our_flag.true_pos.y+our_flag.true_velo.next_speed(100).y , "BOOST" if need_to_boost else 100)


class strategy_atk(object):
    def compute(self, pod):
        need_to_boost = True
        if pod.flag:
            best_pod = min(enemy_pods, key=lambda x: (x.pos+x.velocity).dist(pod.pos))
            futur_enemy_pos = best_pod.next_turn()
            futur_self_pos = pod.next_turn()
            if (futur_enemy_pos.dist(futur_self_pos) < 900):
                need_to_boost = True
            return "{} {} {}".format(pod.pos.x+pod.velocity.x, pod.pos.y, "BOOST" if need_to_boost else 100)
        else:
            return "{} {} {}".format(enemy_flag.true_pos.x - pod.velocity.x, enemy_flag.true_pos.y - pod.velocity.y ,"BOOST")


def full_print():
    for i in [our_flag]+ our_pods +[enemy_flag]+ enemy_pods:
        print >> sys.stderr, i

our_pods[0].strategy = strategy_def()
our_pods[1].strategy = strategy_atk()

# game loop
while True:
    our_flag.set_pos([int(i) for i in raw_input().split()])
    enemy_flag.set_pos([int(i) for i in raw_input().split()])
    for i in our_pods:
        i.set([int(j) for j in raw_input().split()])
        if i.flag:
            enemy_flag.pod = i
    for i in enemy_pods:
        i.set([int(j) for j in raw_input().split()])
        if i.flag:
            our_flag.pod = i
    full_print()

    if not our_flag.pod:
        our_camp = 0 if our_flag.pos.x ==1000 else 9999

    our_pods[0].strategy = strategy_def()
    our_pods[1].strategy = strategy_def()

    if enemy_flag.pod:
        enemy_flag.pod.strategy=strategy_atk()
    else:
        best_pod = max(our_pods, key=lambda x: x.pos.dist(our_flag.true_pos+our_flag.true_velo))
        print >> sys.stderr, best_pod
        best_pod.strategy=strategy_atk()


    for i in our_pods:
        print i.results()

    #for i in xrange(2):

        # Write an action using print
        # To debug: print >> sys.stderr, "Debug messages..."