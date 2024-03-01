from tkinter import *
from tkinter import ttk
import pandas as pd
from math import *

team_data = pd.read_csv("big_5_stats.csv")
team_data.astype({"League Rank":int,"Matches Played": int,"Goals Scored": int,"Goals Against": int,"Attendance":int,"Points Per Game":float,"Win %": float,})
team_names = list(team_data["Squad"])

team1_stats = {"Squad":"Team 1","Country":"country","League Rank":0,"Matches Played":0,"Goals Scored":0,"Goals Against":0,"Points Per Game":0,"Win %":0,"Attendance":0}
team2_stats = {"Squad":"Team 1","Country":"country","League Rank":0,"Matches Played":0,"Goals Scored":0,"Goals Against":0,"Points Per Game":0,"Win %":0,"Attendance":0}
team_detail_headers = ["Squad","Country","League Rank","Goals Scored","Goals Against","Matches Played","Points Per Game","Win %","Attendance"]

best_stats = {"Goals Scored":0,"Goals Against":0,"Win %":0,"Points Per Game":0,"Attendance":0}
for detail in list(best_stats.keys()):
    if detail == "Goals Against":
        best_stats[detail]=team_data[detail].min()
    else:
        best_stats[detail]=team_data[detail].max()


def team1select(event):
    team1 = event.widget.get()
    for detail in team_detail_headers:
        team1_stats[detail] = team_data[detail].where(team_data["Squad"]==team1).dropna().values[0]
    display_team_stats(team1_stats,comparison_table1)
    points = convert_to_distance(team1_stats,100)
    team1Canvas.delete("all")
    drawPentagon(team1Canvas,100,100,100,100,100,outline_color="black",outline_width=1,fill_color="white",dash_tuple=(2,4))
    drawPentagon(team1Canvas,*points,outline_color="black",outline_width=2,fill_color="white",dash_tuple=None)
    win_percent_text = team1Canvas.create_text(centerX,centerY-110,text="Win Percentage")
    goals_for_text = team1Canvas.create_text(centerX+100,centerY,text="Goals Scored")
    goals_against_text = team1Canvas.create_text(centerX+80,centerY+95,text="Goals Against")
    poits_per_game_text = team1Canvas.create_text(centerX-80,centerY+95,text="Points Per Game")
    attendance_text = team1Canvas.create_text(centerX-100,centerY,text="Attendance")

def team2select(event):
    team2 = event.widget.get()
    for detail in team_detail_headers:
        team2_stats[detail] = team_data[detail].where(team_data["Squad"]==team2).dropna().values[0]
    display_team_stats(team2_stats,comparison_table2)
    points = convert_to_distance(team2_stats,100)
    team2Canvas.delete("all")
    drawPentagon(team2Canvas,100,100,100,100,100,outline_color="black",outline_width=1,fill_color="white",dash_tuple=(2,4))
    drawPentagon(team2Canvas,*points,outline_color="black",outline_width=2,fill_color="white",dash_tuple=None)
    win_percent_text = team2Canvas.create_text(centerX,centerY-110,text="Win Percentage")
    goals_for_text = team2Canvas.create_text(centerX+100,centerY,text="Goals Scored")
    goals_against_text = team2Canvas.create_text(centerX+80,centerY+95,text="Goals Against")
    poits_per_game_text = team2Canvas.create_text(centerX-80,centerY+95,text="Points Per Game")
    attendance_text = team2Canvas.create_text(centerX-100,centerY,text="Attendance")

def display_team_stats(team,widget):
    widget.delete(0,END)
    for detail in list(team.keys()):
        widget.insert(END,detail + ": "+ str(team[detail]))

def convert_to_distance(team,size):
    ratio_dict = team
    for detail in list(best_stats.keys()):
        if detail == "Goals Against":
            ratio_dict[detail] = best_stats[detail]/ratio_dict[detail]
        else:
            ratio_dict[detail] = ratio_dict[detail]/best_stats[detail]
    distances_list = []
    for value in list(ratio_dict.values())[4:]:
        distances_list.append(value*size)
    return distances_list

def drawPentagon(canvas,gf_distance,ga_distance,wmp_distance,ptsmp_distance,attendance_distance,outline_color,outline_width,fill_color,dash_tuple):
    gf_point = (centerX+gf_distance*cos(18*pi/180),centerY-gf_distance*sin(18*pi/180))
    ga_point = (centerX+ga_distance*cos(306*pi/180),centerY-ga_distance*sin(306*pi/180))
    wmp_point = (centerX+wmp_distance*cos(90*pi/180),centerY-wmp_distance*sin(90*pi/180))
    ptsmp_point = (centerX+ptsmp_distance*cos(234*pi/180),centerY-ptsmp_distance*sin(234*
    pi/180))
    attendance_point = (centerX+attendance_distance*cos(162*pi/180),centerY-attendance_distance*sin(162*pi/180))
    point_list = [gf_point,wmp_point,attendance_point,ptsmp_point,ga_point]
    canvas.create_polygon(*point_list,outline=outline_color,width=outline_width,fill=fill_color,dash=dash_tuple)

#Creating GUI

window = Tk()
window.geometry("900x500")
window.title("Team Comparer")
window.resizable(False,False)
window.configure(bg="white")

info_frame = Frame(window,height=100,bg="white")
title = Label(info_frame,text="Big 5 European Leagues Team Comparison", font=("Arial",25
,),bg="black", fg="white")

team_1name_label = Label(info_frame,text="Team 1 name:",bg = "white",fg="black",padx=20,
pady=30)
team_2name_label = Label(info_frame,text="Team 2 name:",bg = "white",fg="black",padx=20,
pady=30)
team_1selected = StringVar(window)
team_1selected.set("Select a team")
team_1option = ttk.Combobox(info_frame,textvariable=team_1selected,values = team_names,)
team_1option.bind("<<ComboboxSelected>>",team1select)

team_2selected = StringVar(window)
team_2selected.set("Select a team")
team_2option = ttk.Combobox(info_frame,textvariable=team_2selected,values = team_names,)
team_2option.bind("<<ComboboxSelected>>",team2select)

info_frame.pack(fill=X)
title.pack(fill=X)
team_1name_label.pack(side=LEFT)
team_1option.pack(side=LEFT)

team_2option.pack(side=RIGHT,padx=20)
team_2name_label.pack(side=RIGHT)

team1Canvas = Canvas(window,width = 275,height=350,bg="white")
team1Canvas.pack(side=LEFT,padx=10)

centerX = team1Canvas.winfo_reqwidth()/2
centerY = team1Canvas.winfo_reqheight()/2

comparison_table1 = Listbox(window,borderwidth=3,border=1,height=9,width=20)
comparison_table1.pack(side=LEFT,padx=10)
for i,value in enumerate(team_detail_headers):
    comparison_table1.insert(END,value + ": ")


team2Canvas = Canvas(window,width = 275,height=350,bg="white")
team2Canvas.pack(side=RIGHT,padx=10)

comparison_table2 = Listbox(window,borderwidth=3,border=1,height=9,width=20)
comparison_table2.pack(side=RIGHT,padx=10)
for i,value in enumerate(team_detail_headers):
    comparison_table2.insert(END,value + ": ")

drawPentagon(team1Canvas,100,100,100,100,100,outline_color="black",outline_width=1,fill_color="white",dash_tuple=(2,4))
win_percent_text = team1Canvas.create_text(centerX,centerY-110,text="Win Percentage")
goals_for_text = team1Canvas.create_text(centerX+100,centerY,text="Goals Scored")
goals_against_text = team1Canvas.create_text(centerX+80,centerY+95,text="Goals Against")
poits_per_game_text = team1Canvas.create_text(centerX-80,centerY+95,text="Points Per Game")
attendance_text = team1Canvas.create_text(centerX-100,centerY,text="Attendance")
drawPentagon(team2Canvas,100,100,100,100,100,outline_color="black",outline_width=1,fill_color="white",dash_tuple=(2,4))
win_percent_text = team2Canvas.create_text(centerX,centerY-110,text="Win Percentage")
goals_for_text = team2Canvas.create_text(centerX+100,centerY,text="Goals Scored")
goals_against_text = team2Canvas.create_text(centerX+80,centerY+95,text="Goals Against")
poits_per_game_text = team2Canvas.create_text(centerX-80,centerY+95,text="Points Per Game")
attendance_text = team2Canvas.create_text(centerX-100,centerY,text="Attendance")
mainloop()
