
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
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

class MapFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        photo = tk.PhotoImage(file=".\\media\\maps.png")
        banner = tk.Label(self, image=photo, bd = 1, relief=tk.RIDGE)
        banner.image = photo
        banner.pack(side=tk.LEFT)

        # Maps
        self.maps=tk.Label(self, relief=tk.RIDGE)
        self.maps.pack(padx=10,  pady=5, fill=tk.X)
        self.mission_map = tk.StringVar()
        self.mission_map.set(self.parent.mission_config.mission_map)

        tk.Label(self.maps, text="Choose a map:      ").pack(padx=20,  pady=10, side = tk.LEFT)
        self.r3 = tk.Radiobutton(self.maps, text="Moscow", variable = self.mission_map, value = "Moscow", indicatoron = 0, width =15, command = self.reset_map )
        self.r3.pack(anchor = tk.W, side = tk.LEFT, padx=5)
        self.r1 = tk.Radiobutton(self.maps, text="Stalingrad", variable = self.mission_map, value = "Stalingrad", indicatoron = 0, width =15, command = self.reset_map )
        self.r1.pack(anchor = tk.W, side = tk.LEFT, padx=5 )
        self.r2 = tk.Radiobutton(self.maps, text="Kuban", variable = self.mission_map, value = "Kuban", indicatoron = 0, width =15, command = self.reset_map )
        self.r2.pack(anchor = tk.W, side = tk.LEFT, padx=5)
        #self.r3.config(state=tk.DISABLED)

    def reset_map(self):
        for side in ["allied", "axis"]:
            self.parent.configure_frame_scenario[side].init_config(self.mission_map.get(), side)
            self.parent.configure_frame_scenario[side].reset_lines()

class ConfigureFrameScenario(tk.Frame):
    def __init__(self, parent, mission_map, side, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.init_config(mission_map, side)
        self.show = True

        # Show Banner
        filepaths = {"allied":".\\media\\star.png", "axis":".\\media\\cross.png"}
        photo = tk.PhotoImage(file=filepaths[side])
        banner = tk.Button(self, image=photo, bd = 1, relief=tk.RIDGE, command = lambda: self.toggle_lines())
        banner.image = photo
        banner.pack(side=tk.LEFT)

        # Scenarios
        self.scenarios=tk.Label(self, relief=tk.RIDGE)
        self.scenarios.pack(padx=10,  pady=5, fill=tk.X)
        self.scenario = tk.IntVar()
        scenario_config = self.parent.mission_config.scenario_c[side]
        self.scenario.set(scenario_config)

        tk.Label(self.scenarios, text="Choose a scenario: ").pack(padx=20,  pady=10, side = tk.LEFT)
        self.r1 = tk.Radiobutton(self.scenarios, text="Patrol the Front", variable = self.scenario, value = 1, indicatoron = 0, width =15, command = lambda: self.reset_lines() )
        self.r1.pack(anchor = tk.W, side = tk.LEFT, padx=5 )
        self.r2 = tk.Radiobutton(self.scenarios, text="Escort Bombers", variable = self.scenario, value = 2, indicatoron = 0, width =15, command = lambda: self.reset_lines() )
        self.r2.pack(anchor = tk.W, side = tk.LEFT, padx=5)
        self.r3 = tk.Radiobutton(self.scenarios, text="Ground Attack", variable = self.scenario, value = 3, indicatoron = 0, width =15, command = lambda: self.reset_lines() )
        self.r3.pack(anchor = tk.W, side = tk.LEFT, padx=5)
        self.r4 = tk.Radiobutton(self.scenarios, text=" Random ", variable = self.scenario, value = 0, indicatoron = 0, width =15, command = lambda: self.hide_lines() )
        self.r4.pack(anchor = tk.W, side = tk.LEFT, padx=5 )

        # Variables
        self.fighter_type = tk.StringVar()
        self.fighter2_type = tk.StringVar()
        self.bomber_type = tk.StringVar()
        self.attacker_type = tk.StringVar()
        self.fighter_count = tk.StringVar()
        self.fighter2_count = tk.StringVar()
        self.bomber_count = tk.StringVar()
        self.start_location = tk.StringVar()
        self.fighter_skill = tk.StringVar()
        self.mission_target = tk.StringVar()
        self.intercept_chance = tk.StringVar()

        # Iitialize
        self.fighter_type.set(self.parent.mission_config.fighter_type_c[side])
        self.fighter2_type.set(self.parent.mission_config.fighter2_type_c[side])
        self.bomber_type.set(self.parent.mission_config.bomber_type_c[side])
        self.attacker_type.set(self.parent.mission_config.attacker_type_c[side])
        self.mission_target.set(self.parent.mission_config.mission_target_c[side])

        self.intercept_chances = ["low", "medium", "high"]
        self.intercept_chance.set(self.parent.mission_config.intercept_chance_c[side])
        self.fighter_counts = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
        self.fighter_count.set(self.parent.mission_config.fighter_count_c[side])
        self.fighter2_count.set(self.parent.mission_config.fighter2_count_c[side])
        self.bomber_counts = ["1", "2", "3", "4", "5", "6", "7", "8"]
        self.bomber_count.set(self.parent.mission_config.bomber_count_c[side])
        self.start_locations = ["close to", "not far behind", "far from"]
        self.start_location.set(self.parent.mission_config.start_location_c[side])
        self.fighter_skills = ["rookie", "regular", "veteran"]
        self.fighter_skill.set(self.parent.mission_config.fighter_skill_c[side])

        # Line 1
        self.line_1=tk.Label(self)
        tk.Label(self.line_1, text="Blue flight with ").pack(side=tk.LEFT)
        self.bomber_count_menu = tk.OptionMenu(self.line_1, self.bomber_count, *self.bomber_counts)
        self.bomber_count_menu["width"]=2
        self.bomber_count_menu["relief"]=tk.GROOVE
        self.bomber_count_menu.pack(side=tk.LEFT)
        tk.Label(self.line_1, text=" bombers of the type ").pack(side=tk.LEFT)
        self.bomber_menu = tk.OptionMenu(self.line_1, self.bomber_type, *self.bombers)
        self.bomber_menu["relief"]=tk.GROOVE
        self.bomber_menu["width"]=12
        self.bomber_menu.pack(side=tk.LEFT)
        tk.Label(self.line_1, text=" will bomb the enemy ").pack(side=tk.LEFT)
        self.mission_target_high_menu = tk.OptionMenu(self.line_1, self.mission_target, *self.mission_targets_high )
        self.mission_target_high_menu["relief"]=tk.GROOVE
        self.mission_target_high_menu["width"]=11
        self.mission_target_high_menu.pack(side=tk.LEFT)

        # Line 2
        self.line_2=tk.Label(self)
        tk.Label(self.line_2, text="supported by ").pack(side=tk.LEFT)
        self.fighter_menu = tk.OptionMenu(self.line_2, self.fighter_type, *self.fighters)
        self.fighter_menu["relief"]=tk.GROOVE
        self.fighter_menu["width"]=15
        self.fighter_menu.pack(side=tk.LEFT)
        tk.Label(self.line_2, text=" in Red flight with mostly ").pack(side=tk.LEFT)        
        self.fighter_skill_menu = tk.OptionMenu(self.line_2, self.fighter_skill, *self.fighter_skills )
        self.fighter_skill_menu["relief"]=tk.GROOVE
        self.fighter_skill_menu["width"]=6
        self.fighter_skill_menu.pack(side=tk.LEFT)
        tk.Label(self.line_2, text=" pilots in a group of ").pack(side=tk.LEFT)
        self.fighter_count_menu = tk.OptionMenu(self.line_2, self.fighter_count, *self.fighter_counts)
        self.fighter_count_menu["relief"]=tk.GROOVE
        self.fighter_count_menu["width"]=2
        self.fighter_count_menu.pack(side=tk.LEFT)

        # Line 3
        self.line_3=tk.Label(self)
        tk.Label(self.line_3, text="Your airfield is ").pack(side=tk.LEFT)
        self.target_location_menu = tk.OptionMenu(self.line_3, self.start_location, *self.start_locations)
        self.target_location_menu["relief"]=tk.GROOVE
        self.target_location_menu["width"]=12
        self.target_location_menu.pack(side=tk.LEFT)
        tk.Label(self.line_3, text=" the front lines.  The aircraft will start from the ").pack(side=tk.LEFT)      
        self.intercept_chance_menu = tk.OptionMenu(self.line_3, parent.mission_config.plane_start, *parent.mission_config.plane_starts )
        self.intercept_chance_menu["relief"]=tk.GROOVE
        self.intercept_chance_menu["width"]=11
        self.intercept_chance_menu.pack(side=tk.LEFT)

        # Line 6
        self.line_6=tk.Label(self)
        tk.Label(self.line_6, text="Enemy air activity is ").pack(side=tk.LEFT)      
        self.intercept_chance_menu = tk.OptionMenu(self.line_6, self.intercept_chance, *self.intercept_chances )
        self.intercept_chance_menu["relief"]=tk.GROOVE
        self.intercept_chance_menu["width"]=7
        self.intercept_chance_menu.pack(side=tk.LEFT)
        tk.Label(self.line_6, text=" The AAA gunners are ").pack(side=tk.LEFT)
        self.AAA_level_menu = tk.OptionMenu(self.line_6, parent.mission_config.aaa_level, *parent.mission_config.aaa_levels )
        self.AAA_level_menu["relief"]=tk.GROOVE
        self.AAA_level_menu["width"]=9
        self.AAA_level_menu.pack(side=tk.LEFT)

        # Line 4
        self.line_4=tk.Label(self)
        tk.Label(self.line_4, text="Blue flight with ").pack(side=tk.LEFT)
        self.bomber_count_menu = tk.OptionMenu(self.line_4, self.fighter2_count, *self.bomber_counts)
        self.bomber_count_menu["relief"]=tk.GROOVE
        self.bomber_count_menu["width"]=2
        self.bomber_count_menu.pack(side=tk.LEFT)
        tk.Label(self.line_4, text=" fighters of the type ").pack(side=tk.LEFT)
        self.fighterbomber_menu = tk.OptionMenu(self.line_4, self.fighter2_type, *self.fighters)
        self.fighterbomber_menu["relief"]=tk.GROOVE
        self.fighterbomber_menu["width"]=15
        self.fighterbomber_menu.pack(side=tk.LEFT)
        tk.Label(self.line_4, text=" will patrol over the lines,").pack(side=tk.LEFT)

        # Line 5
        self.line_5=tk.Label(self)
        tk.Label(self.line_5, text="Blue flight with ").pack(side=tk.LEFT)
        self.bomber_count_menu = tk.OptionMenu(self.line_5, self.bomber_count, *self.bomber_counts)
        self.bomber_count_menu["width"]=2
        self.bomber_count_menu["relief"]=tk.GROOVE
        self.bomber_count_menu.pack(side=tk.LEFT)
        tk.Label(self.line_5, text=" aircraft of the type ").pack(side=tk.LEFT)
        self.attacker_menu = tk.OptionMenu(self.line_5, self.attacker_type, *self.attackers)
        self.attacker_menu["relief"]=tk.GROOVE
        self.attacker_menu["width"]=15
        self.attacker_menu.pack(side=tk.LEFT)
        tk.Label(self.line_5, text=" will attack the enemy ").pack(side=tk.LEFT)
        self.mission_target_low_menu = tk.OptionMenu(self.line_5, self.mission_target, *self.mission_targets_low )
        self.mission_target_low_menu["relief"]=tk.GROOVE
        self.mission_target_low_menu["width"]=11
        self.mission_target_low_menu.pack(side=tk.LEFT)

        self.all_lines = [self.line_1, self.line_2, self.line_3, self.line_4, self.line_5, self.line_6]
        self.targets = {0: self.mission_targets_low, 1: self.mission_targets_low, 2: self.mission_targets_high, 3: self.mission_targets_low}
        self.scenario_lines = {1: [self.line_4, self.line_2, self.line_3, self.line_6], 2: [self.line_1, self.line_2, self.line_3, self.line_6], 3:[self.line_5, self.line_2, self.line_3, self.line_6]}
        if scenario_config == 0:
            self.hide_lines()
        else:
            self.show_lines()

    def init_config(self, mission_map, side):
        self.fighters = self.parent.mission_config.fighters[mission_map][side]
        self.bombers = self.parent.mission_config.bombers[mission_map][side]
        self.attackers = self.parent.mission_config.attackers[mission_map][side]
        self.mission_targets_low = self.parent.mission_config.targets_low[mission_map]
        self.mission_targets_high = self.parent.mission_config.targets_high[mission_map]

    def hide_lines(self):
        for k in self.all_lines:
            k.pack_forget()

    def show_lines(self):
        self.hide_lines()
        scn = self.scenario.get()
        if scn != 0:
            for k in self.scenario_lines[scn]:
                k.pack(padx=20)

    def toggle_lines(self):
        if self.show:
            self.hide_lines()
            self.show = False
        else:
            self.show_lines()
            self.show = True

    def reset_lines(self):
        self.show = True
        self.mission_target.set(self.targets[self.scenario.get()][0])
        self.fighter_type.set(self.fighters[0])
        self.bomber_type.set(self.bombers[0])
        self.fighter2_type.set(self.fighters[0])
        self.attacker_type.set(self.attackers[0])
        self.mission_target_low_menu['menu'].delete(0, 'end')
        self.mission_target_high_menu['menu'].delete(0, 'end')
        self.fighter_menu['menu'].delete(0, 'end')
        self.bomber_menu['menu'].delete(0, 'end')
        self.attacker_menu['menu'].delete(0, 'end')
        self.fighterbomber_menu['menu'].delete(0, 'end')
        for choice in self.mission_targets_low:
            self.mission_target_low_menu['menu'].add_command(label=choice, command=tk._setit( self.mission_target, choice))
        for choice in self.mission_targets_high:
            self.mission_target_high_menu['menu'].add_command(label=choice, command=tk._setit( self.mission_target, choice))
        for choice in self.fighters:
            self.fighter_menu['menu'].add_command(label=choice, command=tk._setit( self.fighter_type, choice))
        for choice in self.bombers:
            self.bomber_menu['menu'].add_command(label=choice, command=tk._setit( self.bomber_type, choice))
        for choice in self.attackers:
            self.attacker_menu['menu'].add_command(label=choice, command=tk._setit( self.attacker_type, choice))
        for choice in self.fighters:
            self.fighterbomber_menu['menu'].add_command(label=choice, command=tk._setit( self.fighter2_type, choice))
        self.show_lines()

class WeatherFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.show = True

        # Banner
        photo = tk.PhotoImage(file=".\\media\\weather.png")
        banner = tk.Button(self, image=photo, bd = 1, relief=tk.RIDGE, command = lambda: self.toggle_lines())
        banner.image = photo
        banner.pack(side=tk.LEFT)

        self.mission_date = self.parent.mission_config.date_c
        self.date_days = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"]
        self.date_day = tk.StringVar()
        self.date_day.set(self.mission_date[0:2])
        self.date_months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
        self.date_month = tk.StringVar()
        self.date_month.set(self.mission_date[3:5])
        self.date_years = ["1941", "1942", "1943"]
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
        self.weather_c.pack(padx=10,  pady=5, fill=tk.X)
        self.weather = tk.IntVar()
        weather_config = self.parent.mission_config.weather_c
        self.weather.set(weather_config)

        tk.Label(self.weather_c, text="Choose weather: ").pack(padx=20,  pady=10, side = tk.LEFT)
        self.r1 = tk.Radiobutton(self.weather_c, text="Configure", variable = self.weather, value = 1, indicatoron = 0, width =10, command = lambda: self.show_lines() )
        self.r1.pack(anchor = tk.W, side = tk.LEFT, padx=5 )
        self.r2 = tk.Radiobutton(self.weather_c, text="Random", variable = self.weather, value = 0, indicatoron = 0, width =10, command = lambda: self.hide_lines() )
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

    def hide_lines(self):
        self.line_w.pack_forget()

    def show_lines(self):
        #self.hide_lines()
        if self.weather.get() != 0:
            self.line_w.pack(padx=20,  pady=3)
            self.show = True

    def toggle_lines(self):
        if self.show:
            self.hide_lines()
            self.show = False
        else:
            self.show_lines()
            self.show = True

    def update_date(self, var):
        self.mission_date = self.date_day.get() + "." + self.date_month.get() + "." + self.date_year.get()

class ModeFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.show = True

        photo = tk.PhotoImage(file=".\\media\\mode.png")
        banner = tk.Button(self, image=photo, bd = 1, relief=tk.RIDGE, command = lambda: self.toggle_lines())
        banner.image = photo
        banner.pack(side=tk.LEFT)

        # Modes
        self.mode=tk.Label(self, relief=tk.RIDGE)
        self.mode.pack(padx=10, pady=5, fill=tk.X)
        self.game_type = tk.StringVar()
        self.game_type.set(self.parent.mission_config.game_type_c)
        self.player_slot = tk.StringVar()
        self.player_slot.set(self.parent.mission_config.player_slot_c)
        self.player_slots = ["Blue leader", "Blue wingman", "Blue rear", "Red leader", "Red wingman", "Red rear"]

        tk.Label(self.mode, text="Choose a game type:            ").pack(padx=20,  pady=10, side = tk.LEFT)
        self.r1 = tk.Radiobutton(self.mode, text="Single Mission", variable = self.game_type, value = "single", indicatoron = 0, width =15, command = self.show_single)
        self.r1.pack(anchor = tk.W, side = tk.LEFT, padx=5 )
        self.r2 = tk.Radiobutton(self.mode, text="Cooperative", variable = self.game_type, value = "cooperative", indicatoron = 0, width =15, command = self.show_coop )
        self.r2.pack(anchor = tk.W, side = tk.LEFT, padx=5)

        self.line_s = tk.Label(self)
        self.line_s.pack(padx=20, pady=1)
        tk.Label(self.line_s, text="           You will fly for ").pack(side=tk.LEFT, pady=7)
        self.side = tk.IntVar()
        self.side.set(int(self.parent.mission_config.side_c))
        self.r3 = tk.Radiobutton(self.line_s, text="Allied", variable = self.side, value = 1, indicatoron = 0, width =10)
        self.r3.pack(anchor = tk.W, side = tk.LEFT, padx=5 )
        self.r4 = tk.Radiobutton(self.line_s, text="Axis", variable = self.side, value = 2, indicatoron = 0, width =10 )
        self.r4.pack(anchor = tk.W, side = tk.LEFT, padx=5)
        self.r5 = tk.Radiobutton(self.line_s, text="Both", variable = self.side, value = 0, indicatoron = 0, width =10 )
        self.r5.pack(anchor = tk.W, side = tk.LEFT, padx=5)

        self.line_1=tk.Label(self.line_s)
        self.line_1.pack(side=tk.LEFT, padx=10)
        tk.Label(self.line_1, text="as ").pack(side=tk.LEFT)
        self.player_slot_menu = tk.OptionMenu(self.line_1, self.player_slot, *self.player_slots)
        self.player_slot_menu["width"]=16
        self.player_slot_menu["relief"]=tk.GROOVE
        self.player_slot_menu.pack(padx=5)

        if self.game_type.get() == "cooperative":
            self.show_coop()
        else:
            self.show_single()

    def show_coop(self):
        self.player_slot_menu.config(state=tk.DISABLED)
        self.r5.config(state=tk.ACTIVE)
 
    def show_single(self):
        if self.side.get() == 0:
            self.side.set(1)
        self.player_slot_menu.config(state=tk.ACTIVE)
        self.r5.config(state=tk.DISABLED)

    def toggle_lines(self):
        if self.show:
            self.line_s.pack_forget()
            self.show = False
        else:
            self.line_s.pack(padx=20, pady=1)
            self.show = True

class ActionFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.set_path = tk.Button(self, text="Set IL2 game folder", command=self.set_path, relief=tk.GROOVE, bd=4, width =15)
        self.set_path.pack(side=tk.LEFT, expand=1, padx=5, pady=10)
        self.button_commit=tk.Button(self, height=1, width=40, text="Mission Name:  " + self.parent.mission_config.mission_name, command=self.retrieve_input, relief=tk.GROOVE, bd=4)
        self.button_commit.pack(side=tk.LEFT)
        self.create_mission = tk.Button(self, text="Create Mission", width=15, command=self.create_mission, relief=tk.GROOVE, bd=4)
        self.create_mission.pack(side=tk.RIGHT, expand=1, padx=5, pady=10)

    def retrieve_input(self):
        s = tk.simpledialog.askstring("Change Mission Name ", "Enter new name:                           " ,initialvalue=self.parent.mission_config.mission_name)
        if not s:
            return()
        passed = True
        for i in s:
            if i in "/\\<>;:\"|?*.,\'":
                passed = False
                break
        if passed:
            self.parent.mission_config.mission_name = s
            self.button_commit.configure(text="Mission Name:  " + self.parent.mission_config.mission_name)
            print(self.parent.mission_config.mission_name)
        else:
            self.bell()
            print("Syntax error!")

    def set_path(self):
        self.parent.mission_config.il2_path = filedialog.askdirectory()
        if self.parent.mission_config.il2_path != "":
            self.parent.mission_config.il2_path = self.parent.mission_config.il2_path.replace("/","\\")
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
                date = self.parent.weather_frame.mission_date
                MissionConstructor.GenerateMission( mission_name, template_path, date)
                messagebox.showinfo("Info", "Mission has been generated!")
            except:
                messagebox.showerror("Error", "Could not generate mission!")
            self.create_mission["text"] = "Create Mission"
            self.create_mission.config(state="active")
        else:
            messagebox.showerror("Error", "No IL2 game folder set!")

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
        self.plane_starts = ["runway", "parking area"]
        self.plane_start = tk.StringVar()
        self.plane_start.set(self.plane_start_c)
        self.aaa_level = tk.StringVar()
        self.aaa_level.set(self.aaa_level_c) 

    def load_config(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.il2_path = self.config['DEFAULT']['il2_path']
        self.mission_name = self.config['DEFAULT']['mission_name']
        self.template_path = self.config['DEFAULT']['template_path']
        self.mission_maps = dict(json.loads(self.config['DEFAULT']['maps']))
        self.mission_map = self.config['MISSION']['map']
        self.game_type_c = self.config['MISSION']['game_type']
        self.player_slot_c = self.config['MISSION']['player_slot']
        self.mission_time_c = self.config['MISSION']['mission_time']
        self.mission_wind_c = self.config['MISSION']['mission_wind']
        self.mission_cloud_c = self.config['MISSION']['mission_cloud']
        self.side_c = self.config['MISSION']['side']
        self.weather_c = int(self.config['MISSION']['weather'])
        self.date_c = self.config['MISSION']['date']
        self.plane_start_c = self.config['MISSION']['plane_start']
        self.aaa_level_c = self.config['MISSION']['aaa_gunners']
        self.scenario_c = {}
        self.fighter_type_c = {}
        self.fighter2_type_c = {}
        self.bomber_type_c = {}
        self.attacker_type_c = {}
        self.fighter_count_c = {}
        self.fighter2_count_c = {}
        self.bomber_count_c = {}
        self.start_location_c = {}
        self.fighter_skill_c = {}
        self.mission_target_c = {}
        self.intercept_chance_c = {}
        self.fighters = {}
        self.bombers = {}
        self.attackers = {}
        self.targets_high = {}
        self.targets_low = {}

        for side in ["allied", "axis"]:
            self.scenario_c[side] = int(self.config['MISSION']['scenario_' + side])
            self.fighter_type_c[side] = self.config['MISSION']['fighter_type_' + side]
            self.fighter2_type_c[side] = self.config['MISSION']['fighter2_type_' + side]
            self.bomber_type_c[side] = self.config['MISSION']['bomber_type_' + side]
            self.attacker_type_c[side] = self.config['MISSION']['attacker_type_' + side]
            self.fighter_count_c[side] = self.config['MISSION']['fighter_count_' + side]
            self.fighter2_count_c[side] = self.config['MISSION']['fighter2_count_' + side]
            self.bomber_count_c[side] = self.config['MISSION']['bomber_count_' + side]
            self.start_location_c[side] = self.config['MISSION']['start_location_' + side]
            self.fighter_skill_c[side] = self.config['MISSION']['fighter_skill_' + side]
            self.mission_target_c[side] = self.config['MISSION']['mission_target_' + side]
            self.intercept_chance_c[side] = self.config['MISSION']['intercept_chance_' + side]
        
        for m in self.mission_maps.keys():
            self.fighters_allied = list(json.loads(self.config[m]['fighters_allied']))
            self.fighters_axis = list(json.loads(self.config[m]['fighters_axis']))
            self.bombers_allied = list(json.loads(self.config[m]['bombers_allied']))
            self.bombers_axis = list(json.loads(self.config[m]['bombers_axis']))
            self.attackers_allied = list(json.loads(self.config[m]['attackers_allied']))
            self.attackers_axis = list(json.loads(self.config[m]['attackers_axis']))
            self.targets_high[m] = list(json.loads(self.config[m]['targets_high']))
            self.targets_low[m] = list(json.loads(self.config[m]['targets_low']))
            self.fighters[m] = { "allied": self.fighters_allied, "axis": self.fighters_axis}
            self.bombers[m] = { "allied": self.bombers_allied, "axis": self.bombers_axis}
            self.attackers[m] = { "allied": self.attackers_allied, "axis": self.attackers_axis}

    def write_config(self):
        self.config['MISSION']['map'] = self.parent.map_frame.mission_map.get()
        self.config['DEFAULT']['mission_name'] = self.mission_name
        self.config['MISSION']['game_type'] = self.parent.mode_frame.game_type.get()
        self.config['MISSION']['player_slot'] = self.parent.mode_frame.player_slot.get()
        self.config['MISSION']['side'] = str(self.parent.mode_frame.side.get())
        self.config['MISSION']['weather'] = str(self.parent.weather_frame.weather.get())
        self.config['MISSION']['date'] = str(self.parent.weather_frame.mission_date)
        for side in ["allied", "axis"]:
            self.config['MISSION']['scenario_' + side] = str(self.parent.configure_frame_scenario[side].scenario.get())
            self.config['MISSION']['fighter_type_' + side] = self.parent.configure_frame_scenario[side].fighter_type.get()
            self.config['MISSION']['fighter2_type_' + side] = self.parent.configure_frame_scenario[side].fighter2_type.get()
            self.config['MISSION']['bomber_type_' + side] = self.parent.configure_frame_scenario[side].bomber_type.get()
            self.config['MISSION']['attacker_type_' + side] = self.parent.configure_frame_scenario[side].attacker_type.get()
            self.config['MISSION']['fighter_count_' + side] = self.parent.configure_frame_scenario[side].fighter_count.get()
            self.config['MISSION']['fighter2_count_' + side] = self.parent.configure_frame_scenario[side].fighter2_count.get()
            self.config['MISSION']['bomber_count_' + side] = self.parent.configure_frame_scenario[side].bomber_count.get()
            self.config['MISSION']['start_location_' + side] = self.parent.configure_frame_scenario[side].start_location.get()
            self.config['MISSION']['fighter_skill_' + side] = self.parent.configure_frame_scenario[side].fighter_skill.get()
            self.config['MISSION']['mission_target_' + side] = self.parent.configure_frame_scenario[side].mission_target.get()
            self.config['MISSION']['intercept_chance_' + side] = self.parent.configure_frame_scenario[side].intercept_chance.get()
        self.config['MISSION']['plane_start'] = self.plane_start.get()
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
        self.header_frame = HeaderFrame(self)
        self.header_frame.pack()
        self.mode_frame = ModeFrame(self, bd = 1, relief=tk.SUNKEN)
        self.mode_frame.pack(fill=tk.X, padx=8, pady=8)
        self.map_frame = MapFrame(self, bd = 1, relief=tk.SUNKEN)
        self.map_frame.pack(fill=tk.X, padx=8, pady=8)
        self.configure_frame_scenario = {}
        for side in ["allied","axis"]:
            self.configure_frame_scenario[side] = ConfigureFrameScenario(self, self.mission_config.mission_map, side, bd = 1, relief=tk.SUNKEN)
            self.configure_frame_scenario[side].pack(fill=tk.X, padx=8, pady=8)
        self.weather_frame = WeatherFrame(self, bd = 1, relief=tk.SUNKEN)
        self.weather_frame.pack(fill=tk.X, padx=8, pady=8)
        self.status_frame = StatusFrame(self, bd = 1, relief=tk.SUNKEN)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.action_frame = ActionFrame(self, bd = 1, relief=tk.SUNKEN)
        self.action_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=8, pady=8)


    def reload_config(self):
        self.mission_config.write_config()
        self.mission_config.load_config()
        self.configure_frame_scenario["allied"].destroy()
        self.configure_frame_scenario["axis"].destroy()
        for side in ["allied","axis"]:
            self.configure_frame_scenario[side] = ConfigureFrameScenario(self, self.mission_config.mission_map, side, bd = 1, relief=tk.SUNKEN)
            self.configure_frame_scenario[side].pack(fill=tk.X, padx=8, pady=8)

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

if __name__ == "__main__":
    root = tk.Tk()
    '''
    #Scrollbar stuff
    canvas = tk.Canvas(root, borderwidth=0)
    frame = tk.Frame(canvas)
    vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0,0), window=frame, anchor="nw")
    frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

    MainApplication(frame).pack(side="top", fill="both", expand=True)
    root.minsize(width=750, height=490)
    root.maxsize(width=750, height=890)
    '''

    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.minsize(width=720, height=490)
    root.maxsize(width=720, height=890)
    root.title("IL2 Great Battles Easy Mission Creator v13")
    root.mainloop()
