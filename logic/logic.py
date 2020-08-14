# The module that includes every necessary library and contains the functions called by the main module.

from flask import Flask, redirect, url_for, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from domain.player import player
from game_development.game_development import game_development
from game_area.game_table import game_table
from validation.validations import validation
from exceptions.exceptions import *

from copy import deepcopy
from datetime import *
import sys

class logic(object):
    def __init__(self):
        validator = validation()
        human_visible_map = game_table()            
        computer_invisible_map = game_table()        
        computer_visible_map = game_table()
        human_invisible_map = game_table()
        human_player = player(human_visible_map, computer_invisible_map, computer_visible_map)
        computer_player = player(computer_visible_map, human_invisible_map, human_visible_map)

        self.__game_controller = game_development(validator, human_player, computer_player)
        self.__list_of_battleships = []
        self.__current_battleship = []
        self.__number_of_battleships_placed = []
        self.__steps = 0

    def __check_square_coverage(self, battleship):
        battleship_length = 0
        if battleship[0][0] == battleship[-1][0]:
            battleship_length = battleship[-1][1] - battleship[0][1] + 1
        elif battleship[0][1] == battleship[-1][1]:
            battleship_length = battleship[-1][0] - battleship[0][0] + 1
        else:
            return True
        if battleship_length == len(battleship):
            return True
        else:
            return False

    def prepare_game(self):
        self.__game_controller.reset_game()
        self.__steps = 0
        self.__list_of_battleships.clear()
        self.__current_battleship.clear()
        self.__number_of_battleships_placed.clear()

        self.__game_controller.place_random_battleships()

    def place_battleships(self, row, column):
        if row == "DONE" and column == "DONE":
            try:
                self.__current_battleship.sort()
                if self.__check_square_coverage(self.__current_battleship) == False:
                    raise InvalidBattleship("Invalid coordinates! You can only place battleship on 2, 3 or 4 squares!\n")
                self.__game_controller.place_battleship(self.__current_battleship[0][1], self.__current_battleship[0][0], self.__current_battleship[-1][1], self.__current_battleship[-1][0])
                self.__list_of_battleships.append(deepcopy(self.__current_battleship))
                self.__number_of_battleships_placed.append("new entry")
                self.__current_battleship.clear()
            except (IndexError, InvalidCoordinates, InvalidBattleship, AreaTaken) as exception_message:
                self.__current_battleship.clear()
                return jsonify({"result" : "failure", "message" : "battleship not placed"})
                
            if (len(self.__number_of_battleships_placed) == 3):
                return jsonify({"result" : "success", "message" : "all battleship placed"})
            return jsonify({"result" : "success", "message" : "battleship placed"})

        row = int(row)
        column = int(column)

        if row == 0 or column == 0:
            return jsonify({"result" : "failure", "message" : "null row or column"})

        for battleship in self.__list_of_battleships:
            if [row, column] in battleship:
                return jsonify({"result" : "failure", "message" : "square not empty"})

        if [row, column] in self.__current_battleship:
            self.__current_battleship.remove([row, column])
            return jsonify({"result" : "success", "message" : "removed from current battleship"})
        else:
            self.__current_battleship.append([row, column])
            return jsonify({"result" : "success", "message" : "appended to current battleship"})

    def advance_game(self, row, column):
        try:
            if row == 0 or column == 0:
                return jsonify({"result" : "failure", "message" : "null row or column"})

            player = "not hit"
            computer = "not hit"

            square_hit = self.__game_controller.human_shoot_square(column, row)
            if square_hit == True:
                player = "hit"

            self.__steps += 1
            if self.__game_controller.check_if_game_ended() != False:
                return jsonify({"result" : player, "message" : "human wins"})

            computer_hit = "no"
            square_hit_and_coordinates = self.__game_controller.computer_shoot_square()
            square_hit = square_hit_and_coordinates[0]
            coordinates = square_hit_and_coordinates[1]

            computer = chr(ord('A') + coordinates.get_coordinate_x - 1) + str(coordinates.get_coordinate_y)
            if square_hit == True:
                computer_hit = "yes"

            if self.__game_controller.check_if_game_ended() != False:
                return jsonify({"result" : player, "message" : computer, "computer_hit" : computer_hit, "game_ended" : "computer wins"})

            return jsonify({"result" : player, "message" : computer, "computer_hit" : computer_hit})

        except SquareAlreadyHit as exception_message:
            return jsonify({"result" : "failure", "message" : "square already hit"})

    def get_remaining_squares(self):
        return jsonify({"remaining" : self.__game_controller.get_remaining_squares()})

    @property
    def get_number_of_battleships_placed(self):
        return self.__number_of_battleships_placed

    @property
    def get_steps(self):
        return self.__steps
    