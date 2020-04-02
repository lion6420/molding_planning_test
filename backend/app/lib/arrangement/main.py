from preprocessing import preprocessing
import pandas as pd
import numpy as np
from setting import *
from planning import Planning

# # Weekly Preprocessing
# p = preprocessing(path_source, path_daily_underdemand, path_basic, week, date)
# result_df = p.get_planning_input()
# result_df.to_csv(path_output + 'weekly_demand_WK' + week + '_' + date + '.csv', encoding='utf_8_sig', index=False)


# Start planning
total_weekly_planning = pd.read_csv(path_output + 'weekly_demand_WK' + week + '_' + date + '.csv')
P = Planning(total_weekly_planning)
total_weekly_planning = P.main_function()
total_weekly_planning.to_csv(path_output + 'weekly_demand_WK' + week + '_' + dateAfter + '.csv',  encoding='utf_8_sig', index=False)

# Show and output result
Factory_NWE.show_line_information()
Factory_NWE.output_daily_planning('planning_result_' + date)
