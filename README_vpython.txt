Web VPython 3.2

scene = canvas(width = 0, height = 0, resizable = False)

readme = wtext(text="""
DC Motor README

User Controls
- There is a green button called "Run" in the top left corner. If you press the run button, the simulation will start. Simultaneously, the text will become "Pause" and the button will turn red. Then, you can press the button again to pause.
- To the right of the Run button is the red "Reset" button, which resets the simulation and parameters back to the default configuration.
- To the right of the reset button is the "Slowmo" button, which toggles running the simulation in slow mode. This slows down the simulation by a factor of the RPS unless the RPS < 1, in which case slow mode does nothing.
    - When the button says Slowmo, the simulation is running in normal mode, and vice versa

Parameters
- Rotational inertia slider controls the rotational inertia of each loop of wire.
- The magnetic field slider adjusts the magnitude of the magnetic field produced by the external magnets.
- The source voltage slider controls the amount of voltage produced by the voltage source. 
- The resistance per turn slider changes the resistance in EACH turn of an armature loop. This means that the  total resistance of the armature depends on the number of turns.  
- The number of loops slider controls the number of coils in the armature.
- The number of turns slider adjusts the number of turns in each armature coil/loop.
- The load torque slider changes the magnitude of the load torque on the motor.


Toggles
The following motor simulation elements can be toggled on/off in the UI:
- The magnetic field from external magnets (two purple arrows on the top and bottom)
- The electromagnet pole indicators (red/blue rectangles inside loop)
- The Lorentz force acting on the current loop (two black arrows protruding out the left and right ends of the loop)

Physics
The motor's angular velocity is determined by a differential equation derived from \\(\tau = I\\frac{d\\omega}{dt}\\). The torque on an armature loop is determined by angle and angular velocity-dependent quantities such as the back EMF and Lorentz force. Thus, we used the 2nd order Runge-Kutta method to approximate the motor's motion.

At each timestep \\(t\\), we first computed \\(\\frac{d\\omega}{dt}\\) from the current motor state \\((\\theta, \\omega)\\). Then, \\(\\omega\\) and \\(\\frac{d\\omega}{dt}\\) were used to update \\(\\theta\\) and \\(\\omega\\) over half a timestep (\\(\Delta t / 2\\)). The angular acceleration is then recomputed at this midpoint state (\\(\\theta_{mid}, \\omega_{mid}\\)), and the resulting value is used to update both \\(\\omega\\) and \\(\\theta\\) over the full timestep.

Graphs
- Motor RPM vs time
- The current in the loop vs time
- The back-emf vs time
- The net torque produced by the motor vs time
"""
)


MathJax.Hub.Queue(["Typeset",MathJax.Hub])