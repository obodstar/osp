def screen(self):
        # print(f"      {Back.RED} OSP {Style.RESET_ALL}        ")
        # print(f"        {Back.BLUE} Created By Obod {Style.RESET_ALL}         ")
        # print(f"            {Back.WHITE} Version : 3.0 {Style.RESET_ALL}            ")
        # print()
        # print("+-------------------------------------+")

    
        # Define the text and color
        green = "\033[92m"  # ANSI escape code for light green
        reset = "\033[0m"   # ANSI escape code to reset color
        border_char = "*"  # Character for the border

        # Define the ASCII art and details
        osp_art = [
            " #####   #####   ###### ",
            "#     #  #       #     #",
            "#     #  #       #     #",
            "#     #  #####   ###### ",
            "#     #       #  #      ",
            "#     #       #  #      ",
            " #####   #####   #      "
        ]

        details = [
            "OSP (Obod Star Pinterest)",
            "Created By Obod Star",
            "Version: 3.0"
        ]

        # Determine the width for centering
        width = 40
        border_width = width + 2  # Extra width for border

        # Print the top border
        print(green + border_char * border_width + reset)

        # Print the ASCII art with color, centered, and bordered
        for line in osp_art:
            print(green + border_char + line.center(width) + border_char + reset)

        # Print a border line between ASCII art and details
        print(green + border_char * border_width + reset)

        # Print the details with color, centered, and bordered
        for detail in details:
            print(green + border_char + detail.center(width) + border_char + reset)

        # Print the bottom border
        print(green + border_char * border_width + reset)

screen()