
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import configparser
import json
import time
import MissionConstructor


class HeaderFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        photo = tk.PhotoImage(file=".\\media\\header.png")
        banner = tk.Label(self, image=photo, bd = 1, relief=tk.RIDGE)
        banner.image = photo
        banner.pack(side=tk.LEFT)
        #self.header = tk.Label(self, text="IL2 BOS Cooperative Mission Generator")
        #self.header.config(font=('bold', 20))
        #self.header.pack(pady=10)

class ConfigureFrameScenario(tk.Frame):
    def __init__(self, parent, side, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        # Banner
        filepaths = {"allied":".\\media\\star.png", "axis":".\\media\\cross.png"}
        photo = tk.PhotoImage(file=filepaths[side])
        banner = tk.Label(self, image=photo, bd = 1, relief=tk.RIDGE )
        banner.image = photo
        banner.pack(side=tk.LEFT)

        # Scenarios
        self.scenarios=tk.Label(self, relief=tk.RIDGE)
        self.scenarios.pack(padx=10,  pady=10, fill=tk.X)
        self.scenario = tk.IntVar()
        scenario_config = self.parent.mission_config.scenario_c[side]
        self.scenario.set(scenario_config)

        tk.Label(self.scenarios, text="Choose a scenario: ").pack(padx=20,  pady=10, side = tk.LEFT)
        self.r1 = tk.Radiobutton(self.scenarios, text="Patrol the Front", variable = self.scenario, value = 1, indicatoron = 0, width =15, command = lambda: self.show_lines(1) )
        self.r1.pack(anchor = tk.W, side = tk.LEFT, padx=5 )
        self.r2 = tk.Radiobutton(self.scenarios, text="Escort Bombers", variable = self.scenario, value = 2, indicatoron = 0, width =15, command = lambda: self.show_lines(2) )
        self.r2.pack(anchor = tk.W, side = tk.LEFT, padx=5)
        self.r3 = tk.Radiobutton(self.scenarios, text="Ground Attack", variable = self.scenario, value = 3, indicatoron = 0, width =15, command = lambda: self.hide_lines() )
        self.r3.pack(anchor = tk.W, side = tk.LEFT, padx=5)
        self.r4 = tk.Radiobutton(self.scenarios, text=" Random ", variable = self.scenario, value = 0, indicatoron = 0, width =15, command = lambda: self.hide_lines() )
        self.r4.pack(anchor = tk.W, side = tk.LEFT, padx=5 )

        self.r3.config(state="disabled")

        # Variables
        self.fighter_type = tk.StringVar()
        self.fighter2_type = tk.StringVar()
        self.fighter_type.set(self.parent.mission_config.fighter_type_c[side])
        self.fighter2_type.set(self.parent.mission_config.fighter2_type_c[side])
        self.bomber_type = tk.StringVar()
        self.bomber_type.set(self.parent.mission_config.bomber_type_c[side])
        self.fighter_counts = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
        self.fighter_count = tk.StringVar()
        self.fighter2_count = tk.StringVar()
        self.fighter_count.set(self.parent.mission_config.fighter_count_c[side])
        self.fighter2_count.set(self.parent.mission_config.fighter2_count_c[side])
        self.bomber_counts = ["1", "2", "3", "4", "5", "6", "7", "8"]
        self.bomber_count = tk.StringVar()
        self.bomber_count.set(self.parent.mission_config.bomber_count_c[side])
        self.start_locations = ["close to", "far from"]
        self.start_location = tk.StringVar()
        self.start_location.set(self.parent.mission_config.start_location_c[side])
        self.fighter_skills = ["rookie", "regular", "veteran"]
        self.fighter_skill = tk.StringVar()
        self.fighter_skill.set(self.parent.mission_config.fighter_skill_c[side])
        self.mission_targets = ["airfield", "artillery", "armor", "train", "ammo dump", "bridge", "fuel dump", "garrison"]
        self.mission_target = tk.StringVar()
        self.mission_target.set(self.parent.mission_config.mission_target_c[side])
        self.intercept_chances = ["low", "medium", "high"]
        self.intercept_chance = tk.StringVar()
        self.intercept_chance.set(self.parent.mission_config.intercept_chance_c[side])
   
        # Line 1
        self.line_1=tk.Label(self)
        tk.Label(self.line_1, text="A group of ").pack(side=tk.LEFT)
        self.bomber_count_menu = tk.OptionMenu(self.line_1, self.bomber_count, *self.bomber_counts)
        self.bomber_count_menu["width"]=2
        self.bomber_count_menu["relief"]=tk.GROOVE
        self.bomber_count_menu.pack(side=tk.LEFT)
        tk.Label(self.line_1, text=" bombers of the type ").pack(side=tk.LEFT)
        self.bomber_menu = tk.OptionMenu(self.line_1, self.bomber_type, *self.parent.mission_config.bombers[side], command=self.change_targets)
        self.bomber_menu["relief"]=tk.GROOVE
        self.bomber_menu["width"]=12
        self.bomber_menu.pack(side=tk.LEFT)
        tk.Label(self.line_1, text=" will attack the enemy ").pack(side=tk.LEFT)
        self.mission_target_menu = tk.OptionMenu(self.line_1, self.mission_target, *self.mission_targets )
        self.mission_target_menu["relief"]=tk.GROOVE
        self.mission_target_menu["width"]=11
        self.mission_target_menu.pack(side=tk.LEFT)

        # Line 2
        self.line_2=tk.Label(self)
        tk.Label(self.line_2, text="supported by ").pack(side=tk.LEFT)
        self.fighter_menu = tk.OptionMenu(self.line_2, self.fighter_type, *self.parent.mission_config.fighters[side])
        self.fighter_menu["relief"]=tk.GROOVE
        self.fighter_menu["width"]=15
        self.fighter_menu.pack(side=tk.LEFT)
        tk.Label(self.line_2, text=" fighters with mostly ").pack(side=tk.LEFT)        
        self.fighter_skill_menu = tk.OptionMenu(self.line_2, self.fighter_skill, *self.fighter_skills )
        self.fighter_skill_menu["relief"]=tk.GROOVE
        self.fighter_skill_menu["width"]=6
        self.fighter_skill_menu.pack(side=tk.LEFT)
        tk.Label(self.line_2, text=" pilots in a flight of ").pack(side=tk.LEFT)
        self.fighter_count_menu = tk.OptionMenu(self.line_2, self.fighter_count, *self.fighter_counts)
        self.fighter_count_menu["relief"]=tk.GROOVE
        self.fighter_count_menu["width"]=2
        self.fighter_count_menu.pack(side=tk.LEFT)

        # Line 3
        self.line_3=tk.Label(self)
        tk.Label(self.line_3, text="You start ").pack(side=tk.LEFT)
        self.target_location_menu = tk.OptionMenu(self.line_3, self.start_location, *self.start_locations)
        self.target_location_menu["relief"]=tk.GROOVE
        self.target_location_menu["width"]=8
        self.target_location_menu.pack(side=tk.LEFT)
        tk.Label(self.line_3, text=" the front. Enemy activity is ").pack(side=tk.LEFT)      
        self.intercept_chance_menu = tk.OptionMenu(self.line_3, self.intercept_chance, *self.intercept_chances )
        self.intercept_chance_menu["relief"]=tk.GROOVE
        self.intercept_chance_menu["width"]=7
        self.intercept_chance_menu.pack(side=tk.LEFT)
        tk.Label(self.line_3, text=" AAA gunners are ").pack(side=tk.LEFT)
        self.AAA_level_menu = tk.OptionMenu(self.line_3, parent.mission_config.aaa_level, *parent.mission_config.aaa_levels )
        self.AAA_level_menu["relief"]=tk.GROOVE
        self.AAA_level_menu["width"]=9
        self.AAA_level_menu.pack(side=tk.LEFT)

        # Line 4
        self.line_4=tk.Label(self)
        tk.Label(self.line_4, text="A flight of ").pack(side=tk.LEFT)
        self.bomber_count_menu = tk.OptionMenu(self.line_4, self.fighter2_count, *self.bomber_counts)
        self.bomber_count_menu["relief"]=tk.GROOVE
        self.bomber_count_menu["width"]=2
        self.bomber_count_menu.pack(side=tk.LEFT)
        tk.Label(self.line_4, text=" fighters of the type ").pack(side=tk.LEFT)
        self.bomber_menu = tk.OptionMenu(self.line_4, self.fighter2_type, *self.parent.mission_config.fighters[side])
        self.bomber_menu["relief"]=tk.GROOVE
        self.bomber_menu["width"]=15
        self.bomber_menu.pack(side=tk.LEFT)
        tk.Label(self.line_4, text=" will patrol over the lines,").pack(side=tk.LEFT)

        self.all_lines = [self.line_1, self.line_2, self.line_3, self.line_4]
        self.scenario_lines = {1: [self.line_4, self.line_2, self.line_3], 2: [self.line_1, self.line_2, self.line_3], 3:[self.line_1, self.line_2, self.line_3]}
        if scenario_config == 0:
            self.hide_lines()
        else:
            self.show_lines(self.scenario.get())

    def change_targets(self, val):
        if val in ["IL-2 AM-38", "Ju 87 D-3", "Hs 129 B-2", "Bf 110 E-2"]:
            targets = ["airfield", "artillery", "armor", "garrison"]
        else:
            targets = ["airfield", "artillery", "armor", "train", "ammo dump", "bridge", "fuel dump", "garrison"]
        self.mission_target.set(targets[0])
        self.mission_target_menu['menu'].delete(0,'end')
        for choice in targets:
            self.mission_target_menu['menu'].add_command(label=choice, command=tk._setit(self.mission_target, choice))

    def hide_lines(self):
        for k in self.all_lines:
            k.pack_forget()

    def show_lines(self, scn):
        self.hide_lines()
        for k in self.scenario_lines[scn]:
            k.pack(padx=20,  pady=3)

class WeatherFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        # Banner
        photo = tk.PhotoImage(file=".\\media\\weather.png")
        banner = tk.Label(self, image=photo, bd = 1, relief=tk.RIDGE)
        banner.image = photo
        banner.pack(side=tk.LEFT)

        self.mission_date = self.parent.mission_config.date_c
        self.date_days = ["02", "04", "06", "08", "10", "12", "14", "16", "18", "20", "22", "24", "26", "28", "30"]
        self.date_day = tk.StringVar()
        self.date_day.set(self.mission_date[0:2])
        self.date_months = ["08", "09", "10", "11", "12"]
        self.date_month = tk.StringVar()
        self.date_month.set(self.mission_date[3:5])
        self.date_years = ["1942"]
        self.date_year = tk.StringVar()
        self.date_year.set(self.mission_date[6:10])
        self.mission_times = ["dawn", "morning", "noon", "afternoon", "dusk", "night"]
        self.mission_time = tk.StringVar()
        self.mission_time.set(self.parent.mission_config.mission_time_c)
        self.mission_winds = ["light", "moderate", "strong"]
        self.mission_wind = tk.StringVar()
        self.mission_wind.set(self.parent.mission_config.mission_wind_c)
        self.mission_clouds = ["no clouds", "few clouds", "medium clouds", "heavy clouds"]
        self.mission_cloud = tk.StringVar()
        self.mission_cloud.set(self.parent.mission_config.mission_cloud_c)

        # Scenarios
        self.weather_c=tk.Label(self, relief=tk.RIDGE)
        self.weather_c.pack(padx=10,  pady=10, fill=tk.X)
        self.weather = tk.IntVar()
        weather_config = self.parent.mission_config.weather_c
        self.weather.set(weather_config)

        tk.Label(self.weather_c, text="Choose weather: ").pack(padx=20,  pady=10, side = tk.LEFT)
        self.r1 = tk.Radiobutton(self.weather_c, text="Configure", variable = self.weather, value = 1, indicatoron = 0, width =10, command = lambda: self.line_w.pack(padx=20,  pady=3) )
        self.r1.pack(anchor = tk.W, side = tk.LEFT, padx=5 )
        self.r2 = tk.Radiobutton(self.weather_c, text="Random", variable = self.weather, value = 0, indicatoron = 0, width =10, command = lambda: self.line_w.pack_forget() )
        self.r2.pack(anchor = tk.W, side = tk.LEFT, padx=5 )

        tk.Label(self.weather_c, text="   The date is: ").pack(side=tk.LEFT)
        self.date_day_menu = tk.OptionMenu(self.weather_c, self.date_day, *self.date_days, command = self.update_date )
        self.date_day_menu["relief"]=tk.GROOVE
        self.date_day_menu["width"]=2
        self.date_day_menu.pack(side=tk.LEFT)
        tk.Label(self.weather_c, text=".").pack(side=tk.LEFT)
        self.date_month_menu = tk.OptionMenu(self.weather_c, self.date_month, *self.date_months, command = self.update_date )
        self.date_month_menu["relief"]=tk.GROOVE
        self.date_month_menu["width"]=2
        self.date_month_menu.pack(side=tk.LEFT)
        tk.Label(self.weather_c, text=".").pack(side=tk.LEFT)
        self.date_year_menu = tk.OptionMenu(self.weather_c, self.date_year, *self.date_years, command = self.update_date )
        self.date_year_menu["relief"]=tk.GROOVE
        self.date_year_menu["width"]=4
        self.date_year_menu.pack(side=tk.LEFT)

        # Line Weather
        self.line_w=tk.Label(self)
        self.line_w.pack(padx=20,  pady=3)
        tk.Label(self.line_w, text="It is ").pack(side=tk.LEFT)
        self.mission_time_menu = tk.OptionMenu(self.line_w, self.mission_time, *self.mission_times)
        self.mission_time_menu["relief"]=tk.GROOVE
        self.mission_time_menu["width"]=8
        self.mission_time_menu.pack(side=tk.LEFT)
        tk.Label(self.line_w, text="The winds are ").pack(side=tk.LEFT)
        self.mission_wind_menu = tk.OptionMenu(self.line_w, self.mission_wind, *self.mission_winds )
        self.mission_wind_menu["relief"]=tk.GROOVE
        self.mission_wind_menu["width"]=8
        self.mission_wind_menu.pack(side=tk.LEFT)
        tk.Label(self.line_w, text=" and the sky has ").pack(side=tk.LEFT)
        self.mission_cloud_menu = tk.OptionMenu(self.line_w, self.mission_cloud, *self.mission_clouds )
        self.mission_cloud_menu["relief"]=tk.GROOVE
        self.mission_cloud_menu["width"]=13
        self.mission_cloud_menu.pack(side=tk.LEFT)

        if weather_config == 0:
            self.line_w.pack_forget()

    def update_date(self, var):
        self.mission_date = self.date_day.get() + "." + self.date_month.get() + "." + self.date_year.get()


class ActionFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.set_path = tk.Button(self, text="Set IL2 game folder", command=self.set_path, relief=tk.GROOVE, bd=4, width =15)
        self.set_path.pack(side=tk.LEFT, expand=1, padx=5, pady=10)
        tk.Label(self, text="Fly as: ").pack(side=tk.LEFT)
        self.side = tk.IntVar()
        self.side.set(int(self.parent.mission_config.side_c))
        self.r1 = tk.Radiobutton(self, text="Allied", variable = self.side, value = 1, indicatoron = 0, width =10)
        self.r1.pack(anchor = tk.W, side = tk.LEFT, padx=5 )
        self.r2 = tk.Radiobutton(self, text="Axis", variable = self.side, value = 2, indicatoron = 0, width =10 )
        self.r2.pack(anchor = tk.W, side = tk.LEFT, padx=5)
        self.r3 = tk.Radiobutton(self, text="Both", variable = self.side, value = 0, indicatoron = 0, width =10 )
        self.r3.pack(anchor = tk.W, side = tk.LEFT, padx=5)
        self.create_mission = tk.Button(self, text="Create Mission", width=15, command=self.create_mission, relief=tk.GROOVE, bd=4)
        self.create_mission.pack(side=tk.RIGHT, expand=1, padx=5, pady=10)
    
    def set_path(self):
        self.parent.mission_config.il2_path = filedialog.askdirectory()
        if self.parent.mission_config.il2_path != "":
            self.parent.status_frame.status.configure(text="IL2 game folder: "+ self.parent.mission_config.il2_path)
            self.parent.mission_config.config['DEFAULT']['il2_path'] = self.parent.mission_config.il2_path
            self.parent.mission_config.write_config()
    
    def create_mission(self):
        if self.parent.mission_config.il2_path != "":
            self.parent.mission_config.write_config()
            self.create_mission["text"] = "Please wait..."
            self.create_mission.config(state="disabled")
            self.create_mission.update()
            try:
                il2_path = self.parent.mission_config.il2_path
                mission_name = self.parent.mission_config.mission_name
                template_path = self.parent.mission_config.template_path
                template_name = self.parent.mission_config.template_name
                msbin = self.parent.mission_config.create_msbin
                date = self.parent.weather_frame.mission_date
                MissionConstructor.GenerateMission( mission_name, template_path, template_name, date, msbin )
                messagebox.showinfo("Info", "Mission has been generated!")
            except:
                messagebox.showerror("Error", "Could not generate mission!")
            self.create_mission["text"] = "Create Mission"
            self.create_mission.config(state="active")
        else:
            messagebox.showerror("Error", "No IL2 game folder set!")
    def change_side(self):
        print ("changing sides")

class StatusFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.status_message = "IL2 game folder: " + self.parent.mission_config.il2_path
        self.status = tk.Label(self, text=self.status_message, bd=2, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

class MissionConfig():
    def __init__(self, parent):
        self.load_config()
        self.parent = parent
        self.aaa_levels = ["harmless", "competent", "dangerous"]
        self.aaa_level = tk.StringVar()
        self.aaa_level.set(self.aaa_level_c) 

    def load_config(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.il2_path = self.config['DEFAULT']['il2_path']
        self.mission_name = self.config['DEFAULT']['mission_name']
        self.template_path = self.config['DEFAULT']['template_path']
        self.template_name = self.config['DEFAULT']['template_name']
        self.create_msbin = {"0": False, "1": True}[self.config['DEFAULT']['create_msbin']]
        self.mission_time_c = self.config['MISSION']['mission_time']
        self.mission_wind_c = self.config['MISSION']['mission_wind']
        self.mission_cloud_c = self.config['MISSION']['mission_cloud']
        self.side_c = self.config['MISSION']['side']
        self.weather_c = int(self.config['MISSION']['weather'])
        self.date_c = self.config['MISSION']['date']
        self.aaa_level_c = self.config['MISSION']['aaa_gunners']
        self.scenario_c = {}
        self.fighter_type_c = {}
        self.fighter2_type_c = {}
        self.bomber_type_c = {}
        self.fighter_count_c = {}
        self.fighter2_count_c = {}
        self.bomber_count_c = {}
        self.start_location_c = {}
        self.fighter_skill_c = {}
        self.mission_target_c = {}
        self.intercept_chance_c = {}

        for side in ["allied", "axis"]:
            self.scenario_c[side] = int(self.config['MISSION']['scenario_' + side])
            self.fighter_type_c[side] = self.config['MISSION']['fighter_type_' + side]
            self.fighter2_type_c[side] = self.config['MISSION']['fighter2_type_' + side]
            self.bomber_type_c[side] = self.config['MISSION']['bomber_type_' + side]
            self.fighter_count_c[side] = self.config['MISSION']['fighter_count_' + side]
            self.fighter2_count_c[side] = self.config['MISSION']['fighter2_count_' + side]
            self.bomber_count_c[side] = self.config['MISSION']['bomber_count_' + side]
            self.start_location_c[side] = self.config['MISSION']['start_location_' + side]
            self.fighter_skill_c[side] = self.config['MISSION']['fighter_skill_' + side]
            self.mission_target_c[side] = self.config['MISSION']['mission_target_' + side]
            self.intercept_chance_c[side] = self.config['MISSION']['intercept_chance_' + side]
        self.fighters_red = self.config['PLANES']['fighters_allied']
        self.fighters_blue = self.config['PLANES']['fighters_axis']
        self.bombers_red = self.config['PLANES']['bombers_allied']
        self.bombers_blue = self.config['PLANES']['bombers_axis']
        self.attackers_red = self.config['PLANES']['attackers_allied']
        self.attackers_blue = self.config['PLANES']['attackers_axis']
        self.fighters_allied = list(json.loads(self.fighters_red.replace("'", "\"")))
        self.fighters_axis = list(json.loads(self.fighters_blue.replace("'", "\"")))
        self.bombers_allied = list(json.loads(self.bombers_red.replace("'", "\"")))
        self.bombers_axis = list(json.loads(self.bombers_blue.replace("'", "\"")))
        self.attackers_allied = list(json.loads(self.attackers_red.replace("'", "\"")))
        self.attackers_axis = list(json.loads(self.attackers_blue.replace("'", "\"")))
        self.fighters = { "allied": self.fighters_allied, "axis": self.fighters_axis}
        self.bombers = { "allied": self.bombers_allied, "axis": self.bombers_axis}
        self.attackers = { "allied": self.attackers_allied, "axis": self.attackers_axis}

    def write_config(self):
        self.config['MISSION']['side'] = str(self.parent.action_frame.side.get())
        self.config['MISSION']['weather'] = str(self.parent.weather_frame.weather.get())
        self.config['MISSION']['date'] = str(self.parent.weather_frame.mission_date)
        for side in ["allied", "axis"]:
            self.config['MISSION']['scenario_' + side] = str(self.parent.configure_frame_scenario[side].scenario.get())
            self.config['MISSION']['fighter_type_' + side] = self.parent.configure_frame_scenario[side].fighter_type.get()
            self.config['MISSION']['fighter2_type_' + side] = self.parent.configure_frame_scenario[side].fighter2_type.get()
            self.config['MISSION']['bomber_type_' + side] = self.parent.configure_frame_scenario[side].bomber_type.get()
            self.config['MISSION']['fighter_count_' + side] = self.parent.configure_frame_scenario[side].fighter_count.get()
            self.config['MISSION']['fighter2_count_' + side] = self.parent.configure_frame_scenario[side].fighter2_count.get()
            self.config['MISSION']['bomber_count_' + side] = self.parent.configure_frame_scenario[side].bomber_count.get()
            self.config['MISSION']['start_location_' + side] = self.parent.configure_frame_scenario[side].start_location.get()
            self.config['MISSION']['fighter_skill_' + side] = self.parent.configure_frame_scenario[side].fighter_skill.get()
            self.config['MISSION']['mission_target_' + side] = self.parent.configure_frame_scenario[side].mission_target.get()
            self.config['MISSION']['intercept_chance_' + side] = self.parent.configure_frame_scenario[side].intercept_chance.get()
        self.config['MISSION']['aaa_gunners'] = self.aaa_level.get() 
        self.config['MISSION']['mission_time'] = self.parent.weather_frame.mission_time.get()
        self.config['MISSION']['mission_wind'] = self.parent.weather_frame.mission_wind.get()
        self.config['MISSION']['mission_cloud'] = self.parent.weather_frame.mission_cloud.get()

        with open("config.ini", "w" ) as configfile:
            self.config.write(configfile)

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.mission_config = MissionConfig(self)
        self.parent = parent # necessary?
        self.header_frame = HeaderFrame(self)
        self.header_frame.pack()
        self.configure_frame_scenario = {}
        for side in ["allied","axis"]:
            self.configure_frame_scenario[side] = ConfigureFrameScenario(self, side, bd = 1, relief=tk.SUNKEN)
            self.configure_frame_scenario[side].pack(fill=tk.X, padx=8, pady=8)
        self.weather_frame = WeatherFrame(self, bd = 1, relief=tk.SUNKEN)
        self.action_frame = ActionFrame(self, bd = 1, relief=tk.SUNKEN)
        self.status_frame = StatusFrame(self, bd = 1, relief=tk.SUNKEN )

        self.weather_frame.pack(fill=tk.X, padx=8, pady=8)
        self.action_frame.pack(fill=tk.X, padx=8, pady=8)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)


if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.minsize(width=720, height=400)
    root.maxsize(width=720, height=720)
    root.title("Coop Mission Creator for IL2 BOX")
    root.mainloop()
