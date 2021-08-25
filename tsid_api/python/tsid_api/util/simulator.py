import pinocchio as pin
import time
class PinocchioIntegration:
    """
    Perfect integration of the joint acceleration with pinocchio
    """
    def __init__(self, dt, model):
        self.model = model
        self.dt = dt
        self.q = None
        self.v = None

    @staticmethod
    def build_from_urdf(dt, urdf, package_path):
        robot = pin.RobotWrapper.BuildFromURDF(urdf, package_path, pin.JointModelFreeFlyer())
        return PinocchioIntegration(dt, robot.model)

    def init(self, q0, v0):
        self.q = q0
        self.v = v0

    def simulate(self, dv):
        """
        Update state by integrating the given joint acceleration
        :param dv: joint acceleration
        :return: updated wholebody configuration and joint velocity
        """
        v_mean = self.v + 0.5 * self.dt * dv
        self.v += self.dt * dv
        self.q = pin.integrate(self.model, self.q, self.dt * v_mean)
        return self.q, self.v

DT_DISPLAY = 0.01 
def display_wb(viz, q_t):
  t = q_t.min()

  while t <= q_t.max():
      t_start = time.time()
      viz.display(q_t(t))
      t += DT_DISPLAY
      elapsed = time.time() - t_start
      if elapsed > DT_DISPLAY:
          print("Warning : display not real time ! choose a greater time step for the display.")
      else:
          time.sleep(DT_DISPLAY - elapsed)
      
  # display last config if the total duration is not a multiple of the dt
  viz.display(q_t(q_t.max()))
