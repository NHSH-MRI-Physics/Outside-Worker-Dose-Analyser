import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
import plotly.graph_objects as go
from itertools import accumulate
import pandas as pd
import io
import FileAnalysis

st.set_page_config(
    page_title="Boardwide Dose Statistics", 
    page_icon="📊"
)

st.title("Boardwide Dose Statistics")

if st.session_state["uploaded_data"] == None:
    st.warning("Please upload a file first from the Staff Dose Analyser File Selection Page.")
    st.stop()


Boards = []
for staff in st.session_state["uploaded_data"].staff.values():
    for dose in staff.doses:
        if dose.Employer not in Boards:
            Boards.append(dose.Employer)
selected_board = st.selectbox("Select a Board", Boards)

Years  = ["All Years"]
for staff in st.session_state["uploaded_data"].staff.values():
    for dose in staff.doses:
        if dose.Employer == selected_board:
            if dose.EndDate.year not in Years:
                Years.append(dose.EndDate.year)
selected_year = st.selectbox("Select a year", Years)

badge_type_names = [badge.name for badge in FileAnalysis.BadgeType]
badge_type_names.insert(0, "All Badge Types")
selected_Badge_Type = st.selectbox("Select a Badge Type", badge_type_names)

for staff in st.session_state["uploaded_data"].staff.values():
    for dose in staff.doses:
        if dose.Employer == selected_board:
            if dose.EndDate.year not in Years:
                Years.append(dose.EndDate.year)

def GetDoseData(board,year=None,badgetype=None):
    DoseData = []
    Dates = []
    DoseObjects = []
    for staff in st.session_state["uploaded_data"].staff.values(): #First filter by date
        for dose in staff.doses:
            #Filter by year
            if year == None:
                if dose.Employer == board:
                    DoseData.append(dose.Dose)
                    Dates.append(dose.EndDate)
                    DoseObjects.append(dose)
            else:
                if dose.Employer == board and dose.EndDate.year == year:
                    DoseData.append(dose.Dose)
                    Dates.append(dose.EndDate)
                    DoseObjects.append(dose)

    if badgetype != None: #then filter by badge type
        filtered_data = []
        for i in range(len(DoseData)):
            if DoseObjects[i].Badge.value == badge_type_names.index(badgetype):
                filtered_data.append((Dates[i], DoseData[i]))
        Dates, DoseData = zip(*filtered_data) if filtered_data else ([], [])
        Dates = list(Dates)
        DoseData = list(DoseData)

                
    UniqueDates = list(set(Dates))
    SummedDose = []
    for UniqueDate in UniqueDates:
        SummedDose.append(0)
        for i in range(len(Dates)):
            if Dates[i] == UniqueDate:
                SummedDose[-1] += DoseData[i]

    if len(UniqueDates) > 0:
        sorted_data = sorted(zip(UniqueDates, SummedDose), key=lambda x: x[0])  # Sort by Dates
        UniqueDates, SummedDose = zip(*sorted_data)  # Unpack sorted data back into separate lists
    else:
        UniqueDates = []
        SummedDose = []
   
    return UniqueDates,SummedDose

if selected_year == "All Years":
    selected_year = None

if selected_Badge_Type == "All Badge Types":
    selected_Badge_Type = None

# Get data for the selected board
Dates, DoseData = GetDoseData(selected_board,selected_year,selected_Badge_Type)

titleBadgeType = selected_Badge_Type
if titleBadgeType == None:
    titleBadgeType = "All Badge Types"
else:
    titleBadgeType = selected_Badge_Type + " badge"

# Plot the data
if Dates and DoseData:
    fig = go.Figure(data=[
        go.Scatter(x=Dates, y=DoseData, marker_color="skyblue",mode="markers",hoverinfo="x+y")
    ])

    for x, y in zip(Dates, DoseData):
        fig.add_trace(go.Scatter(
            x=[x, x],
            y=[0, y],
            mode="lines",
            line=dict(color="gray"),
            showlegend=False,
            hoverinfo="skip"
        ))




    fig.update_layout(
        title=f"Dose Data for {selected_board} for {titleBadgeType}" ,
        title_x=0.3,  # Center the title
        xaxis_title="Date",
        yaxis_title="Dose (mSv)",
        plot_bgcolor="black",  # Set background color to black
        paper_bgcolor="black",  # Set outer background color to black
        font=dict(color="white"),  # Set text color to white
        bargap=0.2,  # Set a valid value for bargap (e.g., 0.2),
        showlegend=False 
    )
    # Display the plot in Streamlit
    st.plotly_chart(fig, use_container_width = True)
else:
    st.write("No dose data available for the selected board.")


# Plot the Cummultive data
if Dates and DoseData:
    fig = go.Figure(data=[
        go.Scatter(
            x=Dates, 
            y=list(accumulate(DoseData)), 
            marker_color="skyblue", 
            mode="lines+markers", 
            hoverinfo="x+y", 
            fill='tozeroy',  # Shade the area below the line
            fillcolor="rgba(135, 206, 250, 0.3)"  # Light blue with transparency
        )
    ])

    fig.update_layout(
        title=f"Cummulitive Dose Data for {titleBadgeType}" ,
        title_x=0.3,  # Center the title
        xaxis_title="Date",
        yaxis_title="Dose (mSv)",
        plot_bgcolor="black",  # Set background color to black
        paper_bgcolor="black",  # Set outer background color to black
        font=dict(color="white"),  # Set text color to white
        bargap=0.2,  # Set a valid value for bargap (e.g., 0.2),
        showlegend=False 
    )
    # Display the plot in Streamlit
    st.plotly_chart(fig, use_container_width = True)
else:
    st.write("No Cummulative dose data available for the selected board.")


def Getdf(Board,badgetype=None):

    Years  = ["All Years"]
    for staff in st.session_state["uploaded_data"].staff.values():
        for dose in staff.doses:
            if dose.Employer == Board:
                if dose.EndDate.year not in Years:
                    Years.append(dose.EndDate.year)

    Data = {}
    for year in Years:
        if year == "All Years":
            year = None
        if badgetype == "All Badge Types":
            badgetype = None

        Dates, DoseData = GetDoseData(Board,year,badgetype)

        if year == None:
            year = "All Years"
        if badgetype == None:
            badgetype = "All Badge Types"

        Data[year] = [sum(DoseData),0.0]

    numeric_years = [year for year in Years if year != "All Years"]
    numeric_years = sorted(numeric_years)  
    Data[numeric_years[0]][1] = Data[numeric_years[0]][0]

    for i in range(1, len(numeric_years)):
        Data[numeric_years[i]][1] = Data[numeric_years[i-1]][1] + Data[numeric_years[i]][0]

    Data["All Years"][1] = Data[numeric_years[-1]][1]

    # Convert to DataFrame with multiple columns
    df = pd.DataFrame.from_dict(Data, orient="index", columns=["Total Dose (mSv)", "Cumulative Dose (mSv)"])
    df.index.name = "Year"  # Set the index name
    df = df.reset_index()  # Reset the index to make "Year" a column

    # Round the values to 2 decimal points
    df["Total Dose (mSv)"] = df["Total Dose (mSv)"].round(2)
    df["Cumulative Dose (mSv)"] = df["Cumulative Dose (mSv)"].round(2)
    return df

#Make Table for dose 
st.write("Dose Data Summary for " + selected_board + " with " +titleBadgeType)
df = Getdf(selected_board,selected_Badge_Type)
st.markdown(
    df.style.format({"Total Dose (mSv)": "{:.2f}", "Cumulative Dose (mSv)": "{:.2f}"}).hide(axis="index").to_html(),
    unsafe_allow_html=True
)

def GetLowDoseEntries(board,year=None,badgetype=None):
    DoseEntries=[]
    for staff in st.session_state["uploaded_data"].staff.values(): #First filter by date
        for dose in staff.doses:
            #Filter by year and employer
            if year == None:
                if dose.Employer == board:
                    if dose.DoseBelowDetection== True:
                        DoseEntries.append( [staff,dose] )
            else:
                if dose.Employer == board and dose.EndDate.year == year:
                    if dose.DoseBelowDetection== True:
                        DoseEntries.append( [staff,dose] )

    if badgetype == "All Badge Types":
            badgetype = None

    if badgetype != None: #then filter by badge type
        filtered_data = []
        for i in range(len(DoseEntries)):
            if DoseEntries[i][1].Badge.value == badge_type_names.index(badgetype):
                filtered_data.append(DoseEntries[i])
        DoseEntries = filtered_data
        #DoseEntries = list(DoseEntries)

    

    Data = {}
    Data["Email"] = []
    Data["Name"] = []
    Data["Badge Type"] = []
    Data["End Date"] = []
    Data["Employer"] = []
    for entry in DoseEntries:
        Data["Email"].append(entry[0].email)
        Data["Name"].append(entry[0].name)
        Data["Badge Type"].append(FileAnalysis.BadgeType(entry[1].Badge.value).name)
        Data["End Date"].append(entry[1].EndDate.strftime("%d-%m-%Y"))
        Data["Employer"].append(entry[1].Employer)
    return Data

LowDoseEntries = GetLowDoseEntries(selected_board,selected_year,selected_Badge_Type)
dfLowDose = pd.DataFrame(LowDoseEntries)

st.divider()
st.write("Undetectably Low Dose Entries")
st.dataframe(dfLowDose)  # Interactive table
st.divider()

def GetOtherBadgeDoseEntries(board,year=None):
    DoseEntries=[]
    for staff in st.session_state["uploaded_data"].staff.values(): #First filter by date
        for dose in staff.doses:
            #Filter by year and employer
            if year == None:
                if dose.Employer == board:
                    DoseEntries.append( [staff,dose] )
            else:
                if dose.Employer == board and dose.EndDate.year == year:
                    DoseEntries.append( [staff,dose] )


        filtered_data = []
        for i in range(len(DoseEntries)):            
            if DoseEntries[i][1].Badge.value == badge_type_names.index("OtherType"):
                filtered_data.append(DoseEntries[i])
        DoseEntries = filtered_data

    Data = {}
    Data["Email"] = []
    Data["Name"] = []
    Data["Badge Type"] = []
    Data["Custom Badge"] = []
    Data ["Dose Entry (mSv)"] = []
    Data["End Date"] = []
    Data["Employer"] = []
    for entry in DoseEntries:
        Data["Email"].append(entry[0].email)
        Data["Name"].append(entry[0].name)
        Data["Badge Type"].append(FileAnalysis.BadgeType(entry[1].Badge.value).name)
        Data["End Date"].append(entry[1].EndDate.strftime("%d-%m-%Y"))
        Data["Employer"].append(entry[1].Employer)
        Data["Dose Entry (mSv)"].append(entry[1].Dose)
        Data["Custom Badge"].append(entry[1].CustomBadge)
    return Data

st.write("Other Badge Entries")
OtherBadgeEntries = GetOtherBadgeDoseEntries(selected_board,selected_year)
dfOtherBadges = pd.DataFrame(OtherBadgeEntries)
st.dataframe(dfOtherBadges)  # Interactive table

st.divider()
#Prep the excel data

#StatsPerBadge[Badge][type of data][board]
StatsPerBadge = {}
boards = list(set(Boards))
for badge in badge_type_names:
    
    dfsDoseStats = []
    dfsLowDoseStats = []
    dfsCustomBadgeStats = []
    for board in boards:
        dfsDoseStats.append(Getdf(board,badge))
        LowDoseEntries = GetLowDoseEntries(board,None,badge)
        dfsLowDoseStats.append( pd.DataFrame(LowDoseEntries))
    StatsPerBadge[badge] = [dfsDoseStats, dfsLowDoseStats]

for board in boards:
    OtherBadgeEntries = GetOtherBadgeDoseEntries(board,selected_year)
    dfsCustomBadgeStats.append(pd.DataFrame(OtherBadgeEntries))

# Create an in-memory buffer
output = io.BytesIO()
with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
    for i in range(len(boards)):
        worksheet = writer.book.add_worksheet(boards[i])
        rowcounter=0
        for badge in badge_type_names:
            worksheet.write(rowcounter, 0, badge)
            rowcounter+=1

            worksheet.write(rowcounter, 0, "Overal Stats")
            rowcounter+=1
            StatsPerBadge[badge][0][i].to_excel(writer, index=False, sheet_name=boards[i],startrow=rowcounter)
            rowcounter += len(StatsPerBadge[badge][0][i]) + 2

            worksheet.write(rowcounter, 0, "Undetectably Low Dose Entries")
            rowcounter+=1
            StatsPerBadge[badge][1][i].to_excel(writer, index=False, sheet_name=boards[i],startrow=rowcounter)
            rowcounter += len(StatsPerBadge[badge][1][i]) + 2

        worksheet.write(rowcounter, 0, "Other Badge Entries")
        rowcounter+=1
        dfsCustomBadgeStats[i].to_excel(writer, index=False, sheet_name=boards[i],startrow=rowcounter)
        rowcounter += len(dfsCustomBadgeStats[i]) + 4
    writer._save()
    

# Set the buffer's position to the beginning
output.seek(0)

# Create a download button
st.download_button(
    label="Dump to Excel",
    data=output,
    file_name="Board_Dose_Data.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)