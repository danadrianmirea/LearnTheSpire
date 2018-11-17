import sys
import os

import json
import random

from card_name_to_vector import card_name_to_vector


def choice_dict_to_vectors(choice_dict):
    if choice_dict['picked'] == 'SKIP':
        return [[card_name_to_vector(card_name) for card_name in choice_dict['not_picked']], [1, 0, 0, 0]]

    else:
        choices = choice_dict['not_picked'] + [choice_dict['picked']]
        random.shuffle(choices)
        return [[card_name_to_vector(card_name) for card_name in choices], [0] + [0 if _ == choice_dict['picked'] else 1 for _ in choices]]


if __name__ == '__main__':
    if sys.platform == 'darwin':
        runs_directory = os.path.expanduser(
            '~/Library/Application Support/Steam/steamapps/common/SlayTheSpire/SlayTheSpire.app/Contents/Resources/runs')

    else:
        raise NotImplementedError


    for character_folder in os.listdir(runs_directory):
        with open('{character_folder}_TRAINING_DATA'.format(character_folder=character_folder),
                  'w') as training_data_file:
            json.dump([], training_data_file)

        for run_file in os.listdir(os.path.join(runs_directory, character_folder)):
            with open(os.path.join(runs_directory, character_folder, run_file)) as run:
                with open('{character_folder}_TRAINING_DATA'.format(character_folder=character_folder)) as training_data_file:
                    training_data = json.load(training_data_file)

                training_data += [choice_dict_to_vectors(choice_dict) for choice_dict in json.load(run)['card_choices']]

                with open('{character_folder}_TRAINING_DATA'.format(character_folder=character_folder), 'w') as training_data_file:
                    json.dump(training_data, training_data_file)
