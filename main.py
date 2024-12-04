# main.py

import sys
import importlib

def main():
    levels = ['intro_level', 'level1', 'level2', 'level2_3', 'level3', 'level4', 'level4_5', 'level5', 'level6', 'level6_7', 'level7', 'level8', 'level8_9', 'level9', 'end_level']
    current_level_index = 0
    music_start_time = 0

    while current_level_index < len(levels):
        level_name = levels[current_level_index]
        try:
            level_module = importlib.import_module(f'levels.{level_name}.level_logic')
            print("start", music_start_time)
            level_complete, music_start_time = level_module.run_level(music_start_time)  # Assuming each level_logic.py has a run_level() function
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
