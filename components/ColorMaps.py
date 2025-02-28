from utils.logger import logger
from utils.logger import log_function_call  # Import decorator


color_mapping = {
    # Official Tory blue
    "Conservative and Unionist Party": "#0087DC",
    # Official Labour red
    "Labour Party": "#DC241F",
    # Official Lib Dem yellow-orange
    "Liberal Democrats": "#FDBB30",
    # Official Green Party green
    "Green Party": "#78B943",
    # SNP uses bright yellow
    "Scottish National Party (SNP)": "#FFFF00",
    # Plaid Cymru green
    "Plaid Cymru": "#3F8428",
    # Reform UK blue-cyan
    "Reform UK": "#12B6CF",
    # UKIP purple
    "UK Independence Party (UKIP)": "#70147A",
    # DUP red
    "Democratic Unionist Party (DUP)": "#D50000",
    # Sinn Féin dark green
    "Sinn Féin": "#326760",
    # UUP light blue
    "Ulster Unionist Party (UUP)": "#48A5EE",
    # SDLP green-yellow
    "Social Democratic and Labour Party (SDLP)": "#99D700",
    # Alliance gold
    "Alliance Party of Northern Ireland": "#FFD700",
    # Neutral gray for unclassified entities
    "Other": "#7f7f7f",
    # Categories for entity sizes
    "Large Entity": "#9467bd",  # Purple
    "Medium Entity": "#8c564b",  # Brown
    "Small Entity": "#e377c2",  # Pink
    "Very Small Entity": "#bcbd22",  # Olive green
    "Single Donation Entity": "#7f7f7f",  # Gray
}
