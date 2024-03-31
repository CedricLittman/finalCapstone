"""ANSI print functions"""
def pr_red_on_yellow(line): print("\033[43;91m {} \033[00m" .format(line))
def pr_bg_red(line): print("\033[41m {} \033[43;91m" .format(line))
def pr_continuous_red(): print("\033[91m")
def pr_bg_yellow_continuous(): print("\033[43;91m")
def pr_reset(): print("\033[0m")

# Set up screen and text colours
pr_bg_yellow_continuous()

# Clear screen
def clear_screen():
    import os
    os.system('cls||clear')