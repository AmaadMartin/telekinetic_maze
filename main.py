# main.py

import sys
import importlib

def main():
    levels = ['end_level', 'intro_level', 'level1', 'level2', 'level3', 'level4', 'level5', 'level6', 'level7', 'level8', 'level9', 'level10']
    current_level_index = 0

    while current_level_index < len(levels):
        level_name = levels[current_level_index]
        try:
            level_module = importlib.import_module(f'levels.{level_name}.level_logic')
            level_complete = level_module.run_level()  # Assuming each level_logic.py has a run_level() function
            if level_complete:
                current_level_index += 1
            else:
                print(f"Level {current_level_index + 1} failed. Exiting.")
                sys.exit()
        except ImportError as e:
            print(f"Failed to load level {level_name}: {e}")
            sys.exit()

    print("Congratulations! You have completed all levels.")

if __name__ == '__main__':
    main()
