# import packages
from pystoned import CQER
from pystoned.constant import CET_ADDI, FUN_PROD, OPT_LOCAL, RTS_VRS
from pystoned import dataset as dataset

# import the GHG example data
data = dataset.load_GHG_abatement_cost(x_select=['HRSN', 'CPNK', 'GHG'], y_select=['VALK'])
print(len(data.x))
'''
# calculate the quantile model
model = CQER.CQR(y=data.y, x=data.x, tau=0.5, z=None, cet=CET_ADDI, fun=FUN_PROD, rts=RTS_VRS)
model.optimize(OPT_LOCAL)

# display estimated alpha and beta
model.display_alpha()
model.display_beta()

# display estimated residuals
model.display_positive_residual()
model.display_negative_residual()
'''