"""
Figure 3.13 of Jacques Bures
============================
"""


# %%
# Imports
# ~~~~~~~
import numpy

from PyFiberModes.fiber import get_fiber_from_delta_and_V0
from PyFiberModes import HE11, TE01, TM01, HE21, EH11, HE31, HE12
from PyFiberModes.fundamentals import get_U_parameter
from MPSPlots.render2D import SceneList


figure = SceneList(unit_size=(7, 5))
ax = figure.append_ax(
    x_label='V number',
    y_label='U number',
    show_legend=True
)


V0_list = numpy.linspace(0, 12, 50)

for mode in [HE11, TE01, TM01, HE21, EH11, HE31, HE12]:
    data_list = []
    for V0 in V0_list:
        fiber = get_fiber_from_delta_and_V0(
            delta=0.3,
            V0=V0,
            wavelength=1310e-9
        )

        data = get_U_parameter(
            fiber=fiber,
            mode=mode,
            wavelength=fiber.wavelength
        )

        data_list.append(data)

    _ = ax.add_line(x=V0_list, y=data_list, label=mode, line_width=1.5)

_ = ax.add_line(x=V0_list, y=V0_list, line_width=2, label='U = V')

_ = figure.show()