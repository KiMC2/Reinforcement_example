import numpy as np

class Environment():
    def __init__(self, grid_size=5, unit_coord=[0, 0], goal_coord=[4,4], obstacle_coord=[[1,2], [2,1], [0,3]]):
        # 그리드 크기
        self.grid_size = grid_size

        # 유닛 초기 지점 좌표
        self.coord = {'unit': unit_coord,
                      'goal': goal_coord,
                      'obstacle': obstacle_coord}

        self.unit_start_point = unit_coord

        self.obstacle_dir = []
        for _ in range(len(self.coord['obstacle'])):
            self.obstacle_dir.append(1)

        # 가능한 행동
        self.possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']

    def _check_boundary(self, x, y):
        return x < 0 or x >= self.grid_size or \
               y < 0 or y >= self.grid_size

    def _check_reward_and_done(self, unit_coord):
        reward = 0
        done = False

        for x, y in self.coord['obstacle']:
            if unit_coord == [x, y]:
                reward = -1

        if unit_coord == self.coord['goal']:
            reward = 100
            done = True

        return reward, done

    def _coord_to_state(self):
        state = []
        state.append(self.coord['unit'])
        state.append(self.coord['goal'])

        for coord in self.coord['obstacle']:
            state.append(coord)


        state = np.reshape(state, [1, -1])

        return state

    def move_obstacle(self):
        for index in range(len(self.coord['obstacle'])):
            x, y = self.coord['obstacle'][index]

            x += self.obstacle_dir[index]

            if x == 0:
                self.obstacle_dir[index] = 1
            elif x == self.grid_size - 1:
                self.obstacle_dir[index] = -1

            self.coord['obstacle'][index] = x, y

    def step(self, action):

        x, y = self.coord['unit']

        if action == 'UP':            y -= 1
        elif action == 'DOWN':        y += 1
        elif action == 'LEFT':        x -= 1
        elif action == 'RIGHT':       x += 1

        if not self._check_boundary(x, y):
            self.coord['unit'] = x, y

        next_state = self._coord_to_state()
        reward, done = self._check_reward_and_done([x, y])

        return next_state, reward, done

    def reset(self):

        self.coord['unit'] = self.unit_start_point

        state = self._coord_to_state()

        return state
