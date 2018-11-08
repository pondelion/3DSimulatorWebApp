import numpy as np
from .._base_simulator import BaseSimulator
from .force import lennard_jones, gravity


class BoxCollision2D(BaseSimulator):

    def __init__(self, simulator_name):
        super().__init__(simulator_name)

    def init(self):
        self._time = 0.
        self._n_paricles = 0
        self._time_history = []
        self._positions_history = []
        self._kinetic_energy_history = []
        self._on_update_params()
        self._init_particles(scale=0.3)
        self._init_cell()
        self._kinetic_energy_history.append(self._get_kinetic_energy())
        self._positions_history.append(self._positions.reshape([-1, 3]).copy().tolist())
        self._time_history.append(self._time)

    def update(self, dt):
        """Velocity-Stormer-Verlet法で粒子の位置更新
        """
        if self._is_running is False:
            return
        self._time += dt

        next_pos = np.zeros([self._n_paricles, 3])
        f = np.zeros([self._n_paricles, 3])
        for i in range(self._n_paricles):
            # calc force_t on particle_i
            cell_id_x, cell_id_y = self._get_cell_id(self._positions[i][0], self._positions[i][1])
            particle_ids = self._get_around_particles(cell_id_x, cell_id_y)
            if i == 0:
                print('{} : {}'.format(cell_id_x, cell_id_y))
                print('particle_ids of 0 : ', particle_ids)
            for particle_id in particle_ids:
                if i == particle_id:
                    continue
                f[i] += lennard_jones(self._positions[i], self._positions[particle_id],
                                    float(self._params['epsilon']), float(self._params['sigma']))
            f[i] += gravity(self._mass[i])
            # calc next particle positions r_t+1
            pos = self._positions[i] + dt*self._velocities[i] + f[i] * dt**2 / (2.0 * self._mass[i])
            next_pos[i] = pos
        next_pos[:, 0][next_pos[:, 0] > self._domain_x_max] = self._domain_x_max
        next_pos[:, 0][next_pos[:, 0] < self._domain_x_min] = self._domain_x_min
        next_pos[:, 1][next_pos[:, 1] > self._domain_y_max] = self._domain_y_max
        next_pos[:, 1][next_pos[:, 1] < self._domain_y_min] = self._domain_y_min
        self._positions = next_pos

        # update particle_ids_cell according to updated positions
        self._init_cell()
        # print(self._particle_ids_cell)

        next_vel = np.zeros([self._n_paricles, 3])
        next_f = np.zeros([self._n_paricles, 3])
        for i in range(self._n_paricles):
            # calc force_t+1 on particle_i
            cell_id_x, cell_id_y = self._get_cell_id(self._positions[i][0], self._positions[i][1])
            particle_ids = self._get_around_particles(cell_id_x, cell_id_y)
            for particle_id in particle_ids:
                if i == particle_id:
                    continue
                next_f[i] += lennard_jones(self._positions[i], self._positions[particle_id],
                                    float(self._params['epsilon']), float(self._params['sigma']))
            next_f[i] += gravity(self._mass[i])
            # calc particle velocity v_t+1
            next_vel[i] = self._velocities[i] + (f[i] + next_f[i])*dt/(2.0*self._mass[i])
        self._velocities = next_vel

        self._positions_history.append(self._positions.reshape([-1, 3]).copy().tolist())
        self._positions_history = self._positions_history[-self._MAX_HISTORY:]
        self._time_history.append(self._time)
        self._time_history = self._time_history[-self._MAX_HISTORY:]
        self._kinetic_energy_history.append(self._get_kinetic_energy())
        self._kinetic_energy_history = self._kinetic_energy_history[-self._MAX_HISTORY:]

    def get_states(self, n=1):
        """最新状態をn個返す
        """
        states = {
            'box_positions': self._positions_history[-n:],
            'time': self._time_history[-n:],
            'kinetic_energy': self._kinetic_energy_history[-n:]
        }
        return states

    def _init_particles(self, scale=1.0, box_height=15):
        # box
        self._positions = np.array([[x, y, 0.0] for x in np.arange(int(self._params['box_dim_x'])) for y in np.arange(int(self._params['box_dim_y']))])
        self._positions -= np.array([0.5*float(self._params['box_dim_x']), 0.5*float(self._params['box_dim_y']), 0.0])
        self._positions *= scale
        self._positions += np.array([0.0, box_height, 0.0])
        self._velocities = np.array([[0.0, 0.0, 0.0] for x in np.arange(int(self._params['box_dim_x'])) for y in np.arange(int(self._params['box_dim_y']))])
        self._n_paricles += int(self._params['box_dim_x']) * int(self._params['box_dim_y'])
        self._mass = np.array([self._params['mass1']]*self._n_paricles)

    def _get_around_particles(self, cell_id_x, cell_id_y):
        """隣接セル内の粒子のIDリストを取得する
        """
        if cell_id_x == 37 and cell_id_y == 4:
            print('--asdkaufhushf')
        particle_ids = []
        for dx, dy in ((-1, 0), (0, -1), (0, 0), (1, 0), (0, 1)):
            try:
                if cell_id_x == 37 and cell_id_y == 4:
                    print('get_around : ', self._particle_ids_cell[cell_id_x+dx][cell_id_y+dy])
                particle_ids += self._particle_ids_cell[cell_id_x+dx][cell_id_y+dy].copy()
            except IndexError as e:
                pass

        return particle_ids

    def _init_cell(self):
        """セルに所属する粒子IDリストを初期化
        """
        self._particle_ids_cell = [[[] for y in range(self._cell_num_y)] for x in range(self._cell_num_x)]
        for particle_id in range(self._n_paricles):
            cell_id_x, cell_id_y = self._get_cell_id(self._positions[particle_id][0], self._positions[particle_id][1])
            try:
                self._particle_ids_cell[cell_id_x][cell_id_y].append(particle_id)
            except Exception:
                print('{} : {}'.format(cell_id_x, cell_id_y))

    def _get_cell_id(self, x, y):
        cell_id_x = int((x - self._domain_x_min) / self._cutoff_r)
        cell_id_y = int((y - self._domain_y_min) / self._cutoff_r)
        return (cell_id_x, cell_id_y)

    def _on_update_params(self):
        self._cutoff_r = float(self._params['cutoff_r'])
        self._domain_x_min = float(self._params['domain_x_min'])
        self._domain_x_max = float(self._params['domain_x_max'])
        self._domain_y_min = float(self._params['domain_y_min'])
        self._domain_y_max = float(self._params['domain_y_max'])
        self._cell_num_x = int(np.ceil((self._domain_x_max - self._domain_x_min) / self._cutoff_r)) + 1
        self._cell_num_y = int(np.ceil((self._domain_y_max - self._domain_y_min) / self._cutoff_r)) + 1
        print(self._cell_num_x)
        print(self._cell_num_y)
        self._mass = np.array([self._params['mass1']]*self._n_paricles)

    def _get_kinetic_energy(self):
        energy = 0.0
        for i in range(self._n_paricles):
            energy += 0.5 * self._mass[i] * sum(self._velocities[i]*self._velocities[i])
        return energy
